import pickle

# Load your saved model and vectorizer
model = pickle.load(open('model/model.pkl', 'rb'))
vectorizer = pickle.load(open('model/vectorizer.pkl', 'rb'))

def check_message(msg):
    data = vectorizer.transform([msg])
    prediction = model.predict(data)
    return "SCAM" if prediction == 1 else "SAFE"

# Test it with a real-world tricky one
print(check_message("Your electricity bill is due. Pay now to avoid cutoff."))

# Test with more examples
test_messages = [
    "Congratulations! You won a lottery of 1,00,000 rupees. Claim now!",
    "Urgent: Your account will be suspended. Verify now.",
    "Hey, can you send 500 rupees for dinner? I'll pay you back.",
    "Job from home: Earn 50000/month. No experience needed.",
    "SBI Alert: Your balance is 2500 rupees.",
]

for msg in test_messages:
    result = check_message(msg)
    print(f"Message: {msg[:50]}... -> {result}")