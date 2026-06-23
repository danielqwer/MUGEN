# Dataset

MUGEN is hosted on HuggingFace under the [MUGEN-Benchmark](https://huggingface.co/MUGEN-Benchmark) organization. The benchmark contains **35 tasks** (1,750 problems / 9,250 audio clips) organized into **7 evaluation dimensions** of multi-audio understanding. Mean audio duration is 8.60±8.79 s.

## Tasks by dimension

Following Figure 1 of the paper, the 35 tasks are distributed as follows. Names below are the HuggingFace dataset names; for some tasks the paper uses slightly different display names (e.g. "Target Speaker Extraction" → `Cocktail_Party_Extraction`, "SNR Assessment" → `Signal_to_Noise_Comparison`, "Spatiotemporal Attribute Selection" → `Max_Attribute_Selection`).

### Semantics & Pragmatics (3 tasks · 150 problems)
- `Keyword_Spotting`
- `Intent_Classification`
- `Language_Identification`

### Speaker & Demographics (4 tasks · 200 problems)
- `Speaker_Verification`
- `Gender_Classification`
- `Accent_Identification`
- `Dysarthria_Detection`

### Affective & Paralinguistic State (8 tasks · 400 problems)
- `Emotion_Recognition`
- `Emotion_Intensity_Comparison`
- `Pitch_Level_Distinction`
- `Vocal_Effort_Recognition`
- `Vocal_Fry_Detection`
- `Disfluency_Detection`
- `Prosodic_Stress_Matching`
- `Prosody_Semantic_Mismatch`

### Temporal Awareness (5 tasks · 250 problems)
- `Duration_Extremes_Extraction`
- `Duration_Ordinal_Selection`
- `Duration_Precise_Selection`
- `Speaking_Rate_Extremes`
- `Ordinal_Speaking_Rate`

### Acoustic Scene & Event Analysis (5 tasks · 250 problems)
- `Noise_Environment_Classification`
- `Interruption_Detection`
- `Speech_Concurrent_Event_Detection`
- `Cocktail_Party_Extraction`
- `Signal_to_Noise_Comparison`

### Music Analysis (5 tasks · 250 problems)
- `Music_Tagging`
- `Genre_Classification`
- `Key_Detection`
- `Instrument_Classification`
- `Vocal_Technique_Detection`

### Compositional Acoustic Reasoning (5 tasks · 250 problems)
- `Gender_Emotion_Filtering`
- `Accent_Tempo_Filtering`
- `Specific_Speaker_State`
- `Negative_Constraint_Filtering`
- `Max_Attribute_Selection`

## Per-row schema

Every task is a 5-way multiple-choice problem (audio-as-option).

| Field | Type | Notes |
|-------|------|-------|
| `id` | int32 | Row identifier within the split. Not present on every task. |
| `instruction` | string | Textual constraint shown to the model. |
| `answer` | string | Ground-truth option, one of `(A)`–`(E)`. |
| `audio1` … `audio5` | audio | The five candidate audio clips. |
| `reference_audio` | audio | **Only on the 10 reference-audio tasks** (see below). The reference that conditions the question. |
| `metadata` | struct | Present on a few tasks (e.g. target attributes used to construct the question). |

### Reference-audio tasks (10)

For these tasks the model must compare each candidate against a `reference_audio`:

- `Accent_Identification`
- `Emotion_Recognition`
- `Gender_Classification`
- `Intent_Classification`
- `Language_Identification`
- `Noise_Environment_Classification`
- `Speaker_Verification`
- `Specific_Speaker_State`
- `Speech_Concurrent_Event_Detection`
- `Vocal_Effort_Recognition`

## Splits

Each task ships four 50-row splits (`test`, `test_2`, `test_3`, `test_4`) and a `default` subset combining all 200 rows.

## Loading a task

```python
from datasets import load_dataset

ds = load_dataset("MUGEN-Benchmark/Keyword_Spotting", split="default")
print(ds[0]["instruction"], ds[0]["answer"])

# Reference-audio task
ds = load_dataset("MUGEN-Benchmark/Speaker_Verification", split="default")
print(ds[0]["reference_audio"]["array"].shape)
```

> See `../evaluation/README.md` for the prediction format expected by the LLM judge.
