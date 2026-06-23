# MUGEN: Evaluating and Improving Multi-audio Understanding of Large Audio-Language Models

### The official GitHub page of the paper "MUGEN: Evaluating and Improving Multi-audio Understanding of Large Audio-Language Models"
- Authors: Chih-Kai Yang\*, Yun-Shao Tsai\*, Yu-Kai Guo†, Ping-Le Tsai†, Yen-Ting Piao‡, Hung-Wei Chen‡, Ting-Lin Hsiao‡, Yun-Man Hsu‡, Ke-Han Lu, Hung-yi Lee  (\*†‡Equal Contribution)
- Affiliation: National Taiwan University · NTU AI Center of Research Excellence (NTU AI-CoRE)
- Paper link: https://arxiv.org/abs/2603.09714

## Overview

<div align="center">
  <img src="figures/Figure.png" alt="Overview of MUGEN and the detailed task distribution across the seven evaluation dimensions." width="1000"/>
</div>

## Abstract

**TL;DR: We propose MUGEN, a benchmark for multi-audio understanding in LALMs, and show that current models, including proprietary ones, degrade sharply as the number of concurrent audio inputs grows.**

While multi-audio understanding is critical for large audio-language models (LALMs), it remains underexplored. We introduce MUGEN, a comprehensive benchmark evaluating this capability across speech, general audio, and music. Our experiments reveal consistent weaknesses in multi-audio settings, and performance degrades sharply as the number of concurrent audio inputs increases, identifying input scaling as a fundamental bottleneck. We further investigate training-free strategies and observe that Audio-Permutational Self-Consistency (APSC), which diversifies the order of audio candidates, helps models form more robust aggregated predictions, yielding up to 6.28% accuracy gains. Combining this permutation strategy with Chain-of-Thought further improves performance to 6.74%. These results expose blind spots in current LALMs and provide a foundation for evaluating complex auditory comprehension.

**Key findings**
- LALMs perform substantially better on semantic tasks than on non-semantic ones, exposing an uneven capability distribution.
- Accuracy declines steadily as the number of concurrent audio candidates increases — input scaling is a systematic bottleneck.
- Chain-of-Thought alone fails to resolve auditory perception bottlenecks; Audio-Permutational Self-Consistency (APSC) yields the largest gains, especially when combined with CoT.

## News

- Our paper is now available on [arXiv](https://arxiv.org/abs/2603.09714).
- Our dataset is released on HuggingFace! All 35 tasks are available at [MUGEN-Benchmark](https://huggingface.co/MUGEN-Benchmark).

## Benchmark

MUGEN contains 9,250 audio clips across **35 tasks** organized into **7 evaluation dimensions**: Semantics & Pragmatics, Speaker & Demographics, Affective & Paralinguistic State, Temporal Awareness, Acoustic Scene & Event Analysis, Music Analysis, and Compositional Acoustic Reasoning. Each question is formulated as 5-way multiple choice over candidate audio clips; ten tasks additionally include a reference audio for reference-conditioned comparison.

See `data/README.md` for the data schema and `evaluation/README.md` for the LLM-judge protocol.

## Baselines

- DeSTA2.5-Audio
- Qwen2.5-Omni-7B
- Audio Flamingo 3
- Voxtral-Mini-3B, Voxtral-Small-24B
- Phi-4-Multimodal-Instruct
- Gemini-3-pro (Low / High thinking levels)
- Cascade baseline: Whisper-large-v3 + Gemini-3-pro (ASR + LLM)

Open-source models are run with vLLM under greedy decoding (Voxtral uses the authors' recommended `temperature=0.2, top_p=0.95`; Gemini-3-pro uses `temperature=1`).

## Leaderboard

Accuracy (%) on MUGEN across seven dimensions: Semantics & Pragmatics (S&P), Speaker & Demographics (S&D), Affective & Paralinguistic (A&P), Temporal Awareness (TA), Acoustic Scene & Event Analysis (AS&E), Music Analysis (MA), and Compositional Acoustic Reasoning (CA). Overall is the micro-average over all tasks. "Low" / "High" denote the thinking levels of Gemini. Best within each group in **bold**.

| Model | S&P | S&D | A&P | TA | AS&E | MA | CA | Overall |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| | | | | <div align="left">*Open-source LALMs*</div> | | | | |
| DeSTA2.5-Audio | 46.67 | 22.00 | 21.75 | 17.20 | 30.40 | 18.00 | **28.40** | 24.91 |
| Qwen2.5-Omni | **70.00** | 12.00 | **32.50** | 15.20 | 10.80 | **53.20** | 18.00 | **28.69** |
| Audio Flamingo 3 | 25.33 | 22.50 | 15.00 | 21.20 | 23.20 | 1.20 | 19.20 | 17.43 |
| Voxtral-Mini-3B | 59.33 | 25.50 | 30.00 | 20.00 | 22.40 | 24.80 | 23.60 | 27.83 |
| Voxtral-Small-24B | 64.67 | **27.50** | **32.50** | 22.80 | 22.40 | 25.60 | 16.80 | 28.63 |
| Phi-4-Multimodal-Instruct | 52.00 | 21.00 | 21.00 | **28.00** | **24.80** | 24.80 | 24.80 | 26.29 |
| | | | | <div align="left">*Proprietary LALM*</div>| | | | |
| Gemini-3-pro (Low) | 89.33 | 68.00 | 77.00 | 48.00 | 55.60 | **69.60** | 69.20 | 67.66 |
| Gemini-3-pro (High) | **90.67** | **71.50** | **77.50** | **53.60** | **56.80** | 68.40 | **72.80** | **69.60** |
| | | | | <div align="left">*Cascaded systems*</div> | | | | |
| ASR + LLM (Low) | 75.33 | **20.00** | 27.00 | **28.80** | **26.40** | 26.00 | 18.00 | 29.09 |
| ASR + LLM (High) | **82.67** | 16.50 | **27.75** | **28.80** | 26.00 | 26.00 | **22.40** | **30.06** |

## Citation

If you find MUGEN helpful, please consider citing our paper:

```bibtex
@article{yang2026mugen,
    title={MUGEN: Evaluating and Improving Multi-audio Understanding of Large Audio-Language Models},
    author={Yang, Chih-Kai and Tsai, Yun-Shao and Guo, Yu-Kai and Tsai, Ping-Le and Piao, Yen-Ting and Chen, Hung-Wei and Hsiao, Ting-Lin and Hsu, Yun-Man and Lu, Ke-Han and Lee, Hung-yi},
    journal={arXiv preprint arXiv:2603.09714},
    year={2026}
}
```
