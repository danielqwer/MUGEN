from anthropic import Anthropic
import re
import os
import json
from argparse import ArgumentParser, Namespace
from pathlib import Path

SYSTEM_PROMPT = """You are a good judge. You will be given a question, a ground truth answer and a model generated response. 
                You have to determine whether the model generated answer is correct based on the ground truth answer."""
                
EVAL_PROMPT_TEMPLATE = '''
You will be given a question, a ground truth answer, and a model-generated response.
Your task is to determine whether the model-generated response is correct.

IMPORTANT:
- The answer options correspond to audio clips.
- You do NOT have access to the audio content.
- Therefore, correctness must be judged ONLY based on whether the model selects the same option as the ground truth.

Answer format and equivalence rules:

1. There is one and only one correct option.
   - If the model does not select any option, the answer is incorrect.
   - If the model selects more than one option, the answer is incorrect.

2. A model response is considered as selecting an option if it clearly refers to EXACTLY ONE of the following:
   - An option letter: (A), (B), (C), (D), etc.
   - An audio index that unambiguously maps to a single option, e.g.:
     - "Audio 1" → (A)
     - "Audio 2" → (B)
     - "The first audio" → (A)
     - "The second clip" → (B)

3. The following cases must be judged as INCORRECT:
   - The model chooses no option, no audio index, and no ordinal reference.
   - The model chooses multiple options or multiple audios (e.g., "(A) and (B)", "Audio 1 and Audio 2").
   - The model answer is ambiguous or hedging between options.

4. If the model selects exactly one option:
   - It is CORRECT if the selected option matches the ground truth option.
   - It is INCORRECT otherwise.

Examples:

Question: Which audio best matches the speaker's emotion?
Options: (A) <Audio 1> (B) <Audio 2> (C) <Audio 3> (D) <Audio 4>
Ground truth answer: (B)

Model response: "I choose (B)." → CORRECT  
Model response: "Audio 2." → CORRECT  
Model response: "The second audio clip." → CORRECT  
Model response: "(A)." → INCORRECT  
Model response: "Audio 1 and Audio 2." → INCORRECT  
Model response: "The emotion sounds happy." → INCORRECT (no option selected)

Now judge the following case:

Question: [QUESTION]
Ground truth answer: [GROUND_TRUTH_ANSWER]
Model generated response: [MODEL_GENERATED_RESPONSE]

Carefully follow the rules above and return your judgement in the following format:

Explanation: <brief and explicit reasoning referring to the option alignment>
Judgement: <"correct" or "incorrect">
'''

def parse_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument("--prediction_dir", '-p', type=str, default="voxtral_mini_results/", help="Directory containing prediction files")
    parser.add_argument("--pred_name", type=str, default="output.json", help="File name of the prediction file to evaluate")
    parser.add_argument("--output_name", '-o', type=str, default="llm_judge_results.json", help="File name to save the evaluation results")
    parser.add_argument("--output_dir", type=str, default="voxtral_mini_judged/", help="Directory to save judged results")
    
    return parser.parse_args()


def extract_judgement(text):
    pattern = r"Explanation: (.*?)\nJudgement: (.*?)(?:\n\n|$)"
    match = re.search(pattern, text, re.DOTALL)

    if match:
        explanation = match.group(1)
        judgement = match.group(2)
    else:
        explanation = "No extracted explanation"
        judgement = "No extracted judgement"
    
    results = {"Explanation": explanation, "Judgement": judgement}
    return results

def read_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def evaluate_sample(sample):
    """
    Evaluate a single sample using the Anthropic Claude model.
    sample: A dictionary containing at least 'instruction' (the original instruction), 'response' (the model prediction), and 'answer' (the ground truth answer).
    """
    client = Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
    
    prompt = EVAL_PROMPT_TEMPLATE.replace("[QUESTION]", sample["instruction"])\
        .replace("[GROUND_TRUTH_ANSWER]", sample["answer"])\
        .replace("[MODEL_GENERATED_RESPONSE]", sample["response"])
        
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    
    parsed_result = extract_judgement(message.content[0].text)
    return parsed_result

def evaluate_task(data):
    """
    Evaluate all samples in a task.
    data: A list of samples, each sample is a dictionary.
    """
    results = []
    for sample in data:
        eval_result = evaluate_sample(sample)
        combined_result = {k:v for k,v in sample.items()}
        combined_result.update(eval_result)
        results.append(combined_result)
    return results

def calculate_accuracy(judged_results):
    correct_count = 0
    incorrect_count = 0
    total_count = 0
    invalid_ids = []
    for k in range(len(judged_results)):
        if judged_results[k]['Judgement'].lower().strip() == 'correct':
            correct_count += 1
        elif judged_results[k]['Judgement'].lower().strip() == 'incorrect':
            incorrect_count += 1
        else:
            print(f"Invalid judgement for key: {k}")
            invalid_ids.append(judged_results[k].get('id', f'index_{k}'))
        total_count += 1
    
    accuracy = correct_count / total_count if total_count > 0 else 0
    return accuracy, correct_count, incorrect_count, total_count, invalid_ids

if __name__ == "__main__":
    args = parse_args()
    input_dir = Path(args.prediction_dir)
    output_dir = Path(args.output_dir)

    for task_dir in input_dir.iterdir():
        print(f"Processing task directory: {task_dir}")
        if not task_dir.is_dir():
            continue

        task_id = task_dir.name
        input_json = task_dir / args.pred_name

        if not input_json.exists():
            continue

        # load
        data = read_json(input_json)

        # process
        try:
            processed = evaluate_task(data)
            # calculate accuracy
            accuracy, correct_count, incorrect_count, total_count, invalid_ids = calculate_accuracy(processed)
            print(f"Task: {task_id} | Accuracy: {(accuracy)*100:.2f}% ({correct_count}/{total_count})")
            
            if len(invalid_ids) > 0:
                print(f"Invalid judgements for IDs: {invalid_ids}")
            
            # save
            out_task_dir = output_dir / task_id
            out_task_dir.mkdir(parents=True, exist_ok=True)

            out_json = out_task_dir / args.output_name
            with open(out_json, "w", encoding="utf-8") as f:
                json.dump(processed, f, ensure_ascii=False, indent=4)

            print(f"[OK] {task_id}")
            
        except Exception as e:
            print(f"[ERROR] {task_id}: {e}")
            continue

        


