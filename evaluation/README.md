# Evaluation

MUGEN uses an LLM-as-a-judge protocol for automatic evaluation. Following the paper, the default judge is `claude-haiku-4-5-20251001` with `temperature=0`, which reaches 99% agreement with human annotators on a 400-sample audit. The judge script and prompt live in `llm_judge.py`.

## Setup

```bash
pip install -r ../requirements.txt
export ANTHROPIC_API_KEY=<your_key>
```

## Step 1 — Generate predictions

Run your model on every MUGEN task (the 35 datasets under [MUGEN-Benchmark](https://huggingface.co/MUGEN-Benchmark)) and lay out the predictions like this:

```
<prediction_dir>/
├── <task_name_1>/
│   └── output.json
├── <task_name_2>/
│   └── output.json
└── ...
```

Each `output.json` is a list of samples, one per question:

```json
[
    {
        "id": 0,
        "instruction": "<the original instruction shown to the model>",
        "answer": "(B)",
        "response": "<the raw model output>"
    },
    ...
]
```

Field reference:

- `id` — row id from the HuggingFace dataset (optional but recommended for debugging).
- `instruction` — the instruction string from the HuggingFace row.
- `answer` — the ground-truth option, e.g. `(A)` … `(E)`.
- `response` — your model's free-form output.

Task directory names should match the HuggingFace dataset names (e.g. `Keyword_Spotting`, `Emotion_Recognition`). The judge iterates over every subdirectory of `prediction_dir`, so any folder without `output.json` is skipped.

## Step 2 — Run the LLM judge

```bash
python llm_judge.py \
    --prediction_dir <prediction_dir> \
    --pred_name output.json \
    --output_dir <judged_dir> \
    --output_name llm_judge_results.json
```

For each task the script writes `<judged_dir>/<task_name>/llm_judge_results.json`, which is the input list augmented with the judge fields:

```json
[
    {
        "id": 0,
        "instruction": "...",
        "answer": "(B)",
        "response": "...",
        "Explanation": "<judge's brief reasoning>",
        "Judgement": "correct"
    },
    ...
]
```

Per-task accuracy is printed during the run. If `Judgement` cannot be parsed for some samples, their ids are printed under `Invalid judgements for IDs:` — please re-judge or manually fix those entries before reporting numbers.

## Notes

- The judge prompt assumes one and only one correct option. Selecting no option, multiple options, or hedging is counted as incorrect — see the `EVAL_PROMPT_TEMPLATE` in `llm_judge.py` for the exact rubric.
- Audio index references such as "Audio 1" / "the second clip" are mapped to `(A)` / `(B)` and judged accordingly, so your model's response does not need to be a literal `(X)` letter.
- We recommend keeping `temperature=0` and the exact judge model in the script for reproducibility with the numbers reported in the paper.
