import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, 'spam.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'vectorizer.pkl')

# Load data
data = pd.read_csv(CSV_PATH, encoding='latin-1')

# Keep only required columns
data = data[['v1', 'v2']]
data = data.rename(columns={"v1": "label", "v2": "message"})

# Convert labels to numbers
data['label'] = data['label'].map({'ham': 0, 'spam': 1})

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    data['message'], data['label'], test_size=0.2, random_state=42
)

# Improved Vectorizer 🔥
vectorizer = TfidfVectorizer(
    stop_words='english',
    ngram_range=(1,2),   # bigrams (very important)
    max_features=5000
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Better model 🔥
model = LogisticRegression(max_iter=1000)

model.fit(X_train_vec, y_train)

# Accuracy
accuracy = model.score(X_test_vec, y_test)
print(f"Model Accuracy: {accuracy:.2f}")

# Save model
pickle.dump(model, open("model/model.pkl", "wb"))
pickle.dump(vectorizer, open("model/vectorizer.pkl", "wb"))

print("Model trained and saved successfully!")
