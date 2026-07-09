import os
import pandas as pd
import random

DATA_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(DATA_DIR, 'spam.csv')

# Load existing data
data = pd.read_csv(CSV_PATH, encoding='latin-1')
data.columns = ['label', 'message']

print("Original distribution:")
print(data['label'].value_counts())

# New spam messages - targeted and adversarial
new_spam = [
    # Obfuscated text
    "C.o.n.g.r.a.t.s! You have w.o.n a l.o.t.t.e.r.y of 1,00,000 rupees. C.l.a.i.m now!",
    "W.i.n.n.e.r! Your mobile number has been selected for a cash prize. Send details to claim.",
    "P.a.y.m.e.n.t required urgently. Your account will be suspended if not paid within 24 hours.",
    "F.r.e.e gift card worth 5000 rupees. Click here to redeem: [link]",
    "V.i.p customer alert: Exclusive offer for you. Limited time only.",

    # Social engineering
    "Urgent help needed! My wallet was stolen, send 2000 rupees to this UPI ID: friend@paytm",
    "Family emergency: Mom is in hospital, need money for treatment. Please send 5000 ASAP.",
    "Stuck in traffic accident, phone battery low. Send help to this number: 9876543210",
    "Lost my phone, can't access bank. Transfer 10000 to this account for emergency.",
    "Friend in trouble abroad, needs bail money. Send 15000 rupees immediately.",

    # Local India context
    "MSEB Electricity Board: Your bill payment is overdue. Pay 2500 rupees or face disconnection.",
    "KYC Update Required: Your Aadhaar linked account needs verification. Call 1800-XXX-XXXX",
    "Maharashtra State Electricity: Pending bill of 1800 rupees. Pay online to avoid penalty.",
    "Job from Home: Earn 30000/month working 2 hours daily. WhatsApp your resume to +91-XXXXXX",
    "Work from Home Opportunity: No experience needed. High salary. Send CV to this number.",
    "Online Earning: Make 50000 rupees monthly from home. Free training provided.",
    "Part Time Job: Flexible hours, good pay. Contact for details.",

    # More variations
    "Bank Alert: Unusual activity detected. Verify your account now.",
    "Credit Card Limit Increased: Congratulations! Your limit is now 50000 rupees.",
    "Loan Approved: Instant loan of 20000 rupees available. Apply now.",
    "Insurance Claim: Your policy has matured. Claim 25000 rupees today.",
    "Investment Opportunity: Double your money in 30 days. Guaranteed returns.",
]

# Augment spam by creating variations
augmented_spam = []
for msg in new_spam:
    augmented_spam.append(msg)
    # Replace amounts
    for amount in ['1000', '2000', '5000', '10000', '25000']:
        new_msg = msg.replace('2000', amount).replace('5000', amount).replace('10000', amount).replace('25000', amount).replace('15000', amount)
        if new_msg != msg:
            augmented_spam.append(new_msg)
    # Replace banks
    for bank in ['SBI', 'HDFC', 'ICICI', 'Axis', 'PNB']:
        new_msg = msg.replace('SBI', bank).replace('HDFC', bank).replace('ICICI', bank)
        if new_msg != msg:
            augmented_spam.append(new_msg)

# Oversample existing spam
existing_spam = data[data['label'] == 'spam']['message'].tolist()
for msg in existing_spam:
    # Create 2 variations each
    words = msg.split()
    if len(words) > 5:
        # Replace some words
        variations = []
        variations.append(msg.replace('Free', 'Complimentary').replace('free', 'complimentary'))
        variations.append(msg.replace('win', 'claim').replace('Win', 'Claim'))
        variations.append(msg.replace('prize', 'reward').replace('Prize', 'Reward'))
        augmented_spam.extend(variations)

# New ham messages - tricky ham
new_ham = [
    # Legit bank messages
    "SBI Alert: Your account balance is 1500 rupees. Login to check details.",
    "HDFC Bank: Transaction of 500 rupees debited from your account. Ref: XXXX1234",
    "ICICI: Credit of 2000 rupees received. Available balance: 5000 rupees.",
    "Axis Bank: Your KYC is updated successfully. Thank you for banking with us.",
    "PNB: Bill payment of 1200 rupees processed successfully.",

    # Urgent but legit money mentions
    "Hey, can you send 300 rupees for the movie tickets? I'll return tomorrow.",
    "Dinner bill split: Your share is 450 rupees. Pay to UPI: friend@paytm",
    "Movie tickets cost 800, I paid 400, you pay 400. Thanks!",
    "Group lunch: Total 1500, each pays 300. Send to me.",
    "Party contribution: 200 rupees per person. Transfer to organizer.",

    # Other legit
    "Your Amazon order has been delivered. Track your package.",
    "Flipkart: Your order is out for delivery. Expected by 7 PM.",
    "Meeting reminder: Team meeting at 3 PM tomorrow.",
    "Doctor appointment confirmed for 10 AM. Please arrive 15 mins early.",
    "Flight booking confirmed. PNR: ABC123. Check-in opens 24 hours before.",
]

# Augment ham similarly
augmented_ham = []
for msg in new_ham:
    augmented_ham.append(msg)
    # Variations
    for amount in ['200', '300', '400', '500', '800']:
        new_msg = msg.replace('300', amount).replace('500', amount).replace('200', amount)
        if new_msg != msg:
            augmented_ham.append(new_msg)
    for bank in ['SBI', 'HDFC', 'ICICI', 'Axis', 'PNB']:
        new_msg = msg.replace('SBI', bank).replace('HDFC', bank)
        if new_msg != msg:
            augmented_ham.append(new_msg)

# Oversample existing ham a bit
existing_ham = data[data['label'] == 'ham']['message'].sample(500).tolist()  # Sample 500
augmented_ham.extend(existing_ham)

# Create new dataframes
new_spam_df = pd.DataFrame({'label': 'spam', 'message': augmented_spam})
new_ham_df = pd.DataFrame({'label': 'ham', 'message': augmented_ham})

# Combine
updated_data = pd.concat([data, new_spam_df, new_ham_df], ignore_index=True)

print("Updated distribution:")
print(updated_data['label'].value_counts())

# Save back
updated_data.columns = ['v1', 'v2']
updated_data.to_csv("spam.csv", index=False, encoding='utf-8')

print("CSV updated with targeted data!")