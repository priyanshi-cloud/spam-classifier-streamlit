# AI Scam & Manipulation Detector

A Streamlit-powered scam detection app that combines machine learning with psychological signal analysis to flag suspicious messages.

## What it does

- Detects scam and phishing-like text content
- Scores message risk with a probability value
- Identifies manipulation triggers like urgency, fear, greed, authority, and links
- Provides safety advice and a clear risk level
- Runs in a browser via a Streamlit UI

## Project structure

- `model/app.py` — Streamlit web interface
- `model/detector.py` — prediction engine and heuristic analysis
- `model/train.py` — training pipeline using TF-IDF and Logistic Regression
- `model/augment_data.py` — data augmentation and spam/ham expansion
- `model/fix_csv.py` — CSV cleanup and normalization helper
- `model/check.py` — validation helper for `spam.csv`
- `inference.py` — standalone prediction example script
- `model/spam.csv` — training dataset
- `model/model.pkl` — saved trained model
- `model/vectorizer.pkl` — saved TF-IDF vectorizer

## Prerequisites

- Python 3.10+ or compatible
- `pip` for installing dependencies

## Recommended dependencies

```bash
pip install streamlit pandas scikit-learn
```

## Run locally

From the repository root:

```bash
cd "C:\Users\PRIYA\OneDrive\Documents\scam analysis"
streamlit run model/app.py
```

Then open the displayed URL, for example:

- `http://localhost:8501`
- `http://localhost:8502`

## How it works

1. The user enters a message into the Streamlit interface.
2. `model/detector.py` loads the saved model and vectorizer.
3. The text is scored with the trained classifier.
4. Heuristics scan for links, unrealistic amounts, and psychological triggers.
5. Results are displayed with risk level, probability, and safety advice.

## Notes

- The model is trained on the dataset in `model/spam.csv`.
- `model/train.py` produces `model/model.pkl` and `model/vectorizer.pkl`.
- `model/augment_data.py` is used to expand the training data with additional examples.


## Live Demo

You can try the live demo of the app on Streamlit Cloud:

https://spam-classifier-app-nekmtjiyr4zbdn3p3rvxfz.streamlit.app/

Open the link to interact with the deployed model and UI.
