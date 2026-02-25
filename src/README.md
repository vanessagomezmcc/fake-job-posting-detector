#  Fake Job Posting Fraud Detector

A machine learning web application that detects fraudulent job postings using Natural Language Processing (NLP) and Logistic Regression.

🔗 **Live App:** https://fake-job-posting-detector-vanessagomezmc.streamlit.app/

---

## Overview

Online job fraud is a growing problem. This project builds a production-ready fraud detection system that:

- Analyzes job posting text
- Estimates fraud probability
- Classifies risk levels (High / Medium / Likely Legitimate)
- Provides transparency on how predictions are made
- Validates input to ensure it resembles a real job description

The model is deployed as an interactive web app using **Streamlit**.

---

## Machine Learning Approach

### 1 Text Processing
- TF-IDF Vectorization
- 1–2 gram feature extraction
- English stopword removal
- Max 5000 features

### 2 Model
- Logistic Regression
- Class imbalance handled via `class_weight="balanced"`
- Solver: `saga`
- Optimized convergence settings

### 3 Threshold Optimization
Instead of default 0.50 classification, the decision threshold was optimized using F1-score across multiple probability cutoffs.

**Optimized threshold:** `0.67`

This significantly improved fraud detection balance.

---

## Model Performance (Test Set)

- Fraud Recall: ~90%
- Fraud Precision: ~65%
- PR-AUC: ~0.89
- Strong performance on imbalanced fraud data

This means:
- The model detects most fraudulent postings
- Some legitimate postings may be flagged for manual review
- Optimized for safety-first detection

---

## Features

### ✔ Fraud Probability Score
Outputs a probability from 0–1.

### ✔ Risk Classification
- High Risk (≥ 0.67)
- Medium Risk (0.40 – 0.66)
- Likely Legitimate (< 0.40)

### ✔ Input Validation Layer
Prevents non-job inputs (e.g., "immediately") from being analyzed by requiring:
- Minimum length
- Job-related keywords
- Structured sentence patterns

### ✔ Transparency Section
Explains:
- What probability means
- How thresholds are calibrated
- Model performance metrics
- Limitations and disclaimer

---

## Tech Stack

- Python
- Streamlit
- Scikit-learn
- TF-IDF (NLP)
- Logistic Regression
- Pandas / NumPy
- SciPy

---

## 📂 Project Structure

fake-job-posting-detector/
│
├── src/
│ ├── app.py
│ └── model.pkl
│
├── requirements.txt
└── README.md
---

## Running Locally

1. Clone the repository
git clone (https://github.com/vanessagomezmcc/fake-job-posting-detector.git)
cd fake-job-posting-detector

2. Create virtual environment
python -m venv venv
source venv/bin/activate # Mac/Linux
venv\Scripts\activate # Windows


3. Install dependencies
pip install -r requirements.txt

4. Run the app
(https://fake-job-posting-detector-vanessagomezmc.streamlit.app/)


---

## Important Disclaimer

This system is designed as a decision-support tool.

- It should not automatically reject candidates.
- High-risk results should trigger manual review.
- Fraud detection models may produce false positives or false negatives.

---

## What This Project Demonstrates

- NLP feature engineering
- Handling imbalanced datasets
- Precision–Recall evaluation
- Threshold optimization
- Production ML deployment
- Model transparency practices
- Responsible AI considerations
- Streamlit application development

---

## Future Improvements

- SHAP explanations for feature interpretability
- Highlight suspicious words in UI
- Add structured metadata features (salary, remote, etc.)
- Add second-stage classifier
- Deploy with Docker
- Custom domain hosting

---

## Author

Vanessa Gomez  
https://www.linkedin.com/in/vanessa-gomez-miselem/

---

##  If You Like This Project
Give it a star and feel free to connect!
