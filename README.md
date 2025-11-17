# Extracting social determinants of health (SDoH) from electronic health records (EHR)

## 🎯 Overview
This repository provides both rule-based and prompt-based approaches for extracting SDoH factors from clinical text.

The SDoH classification schema encompasses seven domains below, six social and one behavioral (physical activity):
- Social resources and connection
- General financial status
- Food security
- Health insurance status
- Housing conditions
- Employment status
- Physical activity

## SDoHSpacy
A [rule-based pipeline](./sdohspacy/) for extracting SDoH domain categories and subcategories.

## Prompts for SDoH Extraction
[Zero-shot prompt (strict)](./prompts/prompts_strict.py)

[Zero-shot prompt (balanced)](./prompts/prompts_balanced.py)

[Zero-shot prompt (liberal)](./prompts/prompts_liberal.py)

[Few-shot prompt template](./prompts/few-shot_prompt.py)

## Annotation guidelines
[Annotation guidelines](./annotation_guideline/)

## MEDLINE N-Gram Embeddings
**Download Link**: [MEDLINE N-Gram SentenceBERT (MPNet) Embeddings](https://www.dropbox.com/scl/fi/4bey4rljjy9mdmsl1ris8/paraphrase-mpnet-base-v2_nGramSet.npy?rlkey=rcc5tx4sxjgxn6hn65vgkv8pg&dl=0)

**Specifications**:
- **Model**: Sentence-Transformers/paraphrase-mpnet-base-v2
- **Coverage**: 1-5 grams from MEDLINE corpus
- **Dimension**: 768-dimensional dense vectors
- **Format**: NumPy array format
- **Size**: Approximately 87 GB


## 📚 Citation

```bibtex
@article{wang2025sdoh,
    title = {Extracting social determinants of health from electronic healthrecords: development and comparison of rule-based and largelanguage models-based methods},
    year = {2025},
    url = {TBD}
}
```