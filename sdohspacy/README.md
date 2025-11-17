# Rule-based SDoH Clinical Text Extraction Pipeline

A Python pipeline for extracting seven SDoH domain categories and 23 subcategories from clinical notes using MedSpaCy and other NLP techniques.

## 🎯 Overview

This pipeline extracts SDoH mentions from clinical notes, including:
- Social resources and connection
- General financial status
- Food security
- Health insurance status
- Housing conditions
- Employment status
- Physical activity

The pipeline uses [MedSpaCy](https://github.com/medspacy/medspacy) for clinical NLP processing and implements the [ConText algorithm](https://www.sciencedirect.com/science/article/pii/S1532046409000744) for determining negation, experiencer, and temporal Status.

## 💻 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/bwang482/SDoH_Extraction.git
    cd sdohspacy
    ```

2. **Create a virtual environment** (recommended)
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 📚 Usage

1. **Configure the pipeline**:
   Edit `config.py` to set your data paths and pipeline parameters.

2. **Prepare your data**:
   Place your clinical notes CSV files in the configured data directory `data_dir`.

3. **Run the pipeline**:
   ```bash
   cd src
   python pipeline.py
   ```

