import os
import pickle
import re

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'vectorizer.pkl')

# Load saved model and vectorizer
model = pickle.load(open(MODEL_PATH, "rb"))
vectorizer = pickle.load(open(VECTORIZER_PATH, "rb"))

# Psychological keywords
urgency = ["urgent", "now", "immediately", "asap"]
fear = ["blocked", "suspended", "legal action", "warning"]
greed = ["win", "free", "prize", "money", "offer", "jackpot", "reward"]

authority = ["bank", "rbi", "government", "official", "account", "otp", "verify"]


# Detect psychological manipulation
def detect_psychology(message):
    message = message.lower()
    found = []

    for word in urgency:
        if word in message:
            found.append("Urgency")

    for word in fear:
        if word in message:
            found.append("Fear")

    for word in greed:
        if word in message:
            found.append("Greed")

    for word in authority:
        if word in message:
            found.append("Authority")

    return list(set(found))


def detect_link(message):
    lower = message.lower()
    return "http" in lower or "www" in lower or "click here" in lower


def detect_unrealistic_amount(message):
    numbers = re.findall(r'\d+', message)

    for num in numbers:
        if len(num) > 7:   # very large number
            return True

    return False


# Predict message
def predict_message(message):
    msg_vector = vectorizer.transform([message])

    prediction = model.predict(msg_vector)[0]
    probability = model.predict_proba(msg_vector)[0][1]

    psychology = detect_psychology(message)
    unrealistic = detect_unrealistic_amount(message)
    link_flag = detect_link(message)

    return prediction, probability, psychology, unrealistic, link_flag


# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    msg = input("Enter message: ")

    pred, prob, psych, unrealistic, link_flag = predict_message(msg)

    # Result
    if pred == 1:
        print("⚠️ Potential scam/spam message")
    else:
        print("✅ Low-risk message")

    print(f"Suspicion score: {prob:.2f}")
    print("Psychological Triggers:", psych)

    # Smart warning (your USP 🔥)
    if pred == 0 and (len(psych) >= 2 or prob > 0.3):
        print("⚠️ Suspicious message (psychological manipulation detected)")
