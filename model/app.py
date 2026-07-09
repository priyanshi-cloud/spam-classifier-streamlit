import os
import sys
import csv
import datetime
import streamlit as st

# Ensure the model directory is on sys.path so local modules can be imported reliably
ROOT_DIR = os.path.dirname(__file__)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from detector import predict_message

# Feedback file (appends user feedback)
FEEDBACK_CSV = os.path.join(ROOT_DIR, "feedback.csv")

# Example/demo messages visitors can load quickly
EXAMPLES = {
    "-- choose an example --": "",
    "Lottery / Prize Scam": "Congratulations! You won a lottery of 1,00,000 rupees. Claim now!",
    "Urgent Bank Alert": "Urgent: Your account will be suspended in 24 hours. Verify now: http://fake-bank.example/verify",
    "Job Offer (Spam)": "Work from home: Earn 50000/month. No experience needed. Apply now!",
    "Legit Bank Notification": "SBI Alert: Your balance is 2500 rupees.",
}

# ---------------- PAGE SETUP ---------------- #
st.set_page_config(page_title="AI Scam Detector", page_icon="🚨", layout="centered")

# ---------------- CUSTOM UI ---------------- #
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

/* Glass container */
.block-container {
    background: rgba(255, 255, 255, 0.05);
    padding: 2rem;
    border-radius: 20px;
    backdrop-filter: blur(12px);
}

/* Text area */
textarea {
    background-color: rgba(255,255,255,0.1) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 10px !important;
}

/* Button */
button[kind="primary"] {
    background: linear-gradient(90deg, #ff4b4b, #ff6b6b);
    border-radius: 12px;
    font-weight: bold;
    color: white;
}

/* Headings */
h1, h2, h3 {
    color: #f8fafc;
}

/* Divider */
hr {
    border: 1px solid rgba(255,255,255,0.1);
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #
st.title("🚨 AI Scam & Manipulation Detector")
st.markdown("### 🔍 Analyze Messages Like a Digital Detective")

st.divider()

# ---------------- THEME SELECTOR ---------------- #
theme = st.sidebar.selectbox("Theme", ["Default", "Ocean", "Sunset"], index=0)

_BG = {
    "Default": "linear-gradient(135deg, #0f172a, #1e293b)",
    "Ocean": "linear-gradient(135deg, #09203f, #537895)",
    "Sunset": "linear-gradient(135deg, #ff7a7a, #ffb86b)",
}

# Override background based on selection
st.markdown(f"<style>.stApp{{background: {_BG.get(theme)}; color: white;}}</style>", unsafe_allow_html=True)

# ---------------- EXAMPLES / INPUT ---------------- #
st.sidebar.markdown("### Examples")
example_key = st.sidebar.selectbox("Pick an example to load", list(EXAMPLES.keys()))
if st.sidebar.button("Load example") and example_key in EXAMPLES:
    st.session_state['msg'] = EXAMPLES[example_key]
if st.sidebar.button("Clear input"):
    st.session_state['msg'] = ""

if 'msg' not in st.session_state:
    st.session_state['msg'] = ""

msg = st.text_area("✍️ Enter Message", value=st.session_state.get('msg', ''), key='msg', height=150, placeholder="Paste suspicious message here...")

# Quick demo dataset viewer
with st.expander("Demo messages / dataset examples"):
    for name, text in EXAMPLES.items():
        if name != "-- choose an example --":
            st.markdown(f"**{name}**: {text}")

# ---------------- BUTTON / PREDICTION ---------------- #
if st.button("🔍 Scan Message", use_container_width=True):
    if st.session_state['msg'].strip() == "":
        st.warning("Please enter a message!")
    else:
        pred, prob, psych, unrealistic, link_flag = predict_message(st.session_state['msg'])

        # ---------------- RESULT ---------------- #
        st.markdown("### 🚦 Result")

        if pred == 1:
            st.error("🚨 Scam Message Detected")

        elif unrealistic:
            st.error("🚨 Unrealistic amount detected — likely a scam!")

        elif link_flag:
            st.warning("⚠️ Contains link or redirection — be cautious!")

        elif prob > 0.4 or len(psych) >= 2:
            st.warning("⚠️ Suspicious Message Detected")

        else:
            st.success("✅ Safe Message")

        # ---------------- PROBABILITY / CONFIDENCE METER ---------------- #
        st.markdown("### 📊 Scam Probability")
        st.metric("Confidence", f"{int(prob*100)}%")
        st.progress(int(prob * 100))
        st.write(f"**Confidence Score:** {prob:.2f}")

        # ---------------- RISK LEVEL ---------------- #
        st.markdown("### 🎯 Risk Level")

        if prob > 0.7 or unrealistic:
            st.error("High Risk 🚨")
        elif prob > 0.4:
            st.warning("Medium Risk ⚠️")
        else:
            st.success("Low Risk ✅")

        # ---------------- PSYCHOLOGY ---------------- #
        st.markdown("### 🧠 Psychological Triggers")

        if psych:
            cols = st.columns(len(psych))
            for i, p in enumerate(psych):
                cols[i].info(p)
        else:
            st.write("No manipulation detected")

        # ---------------- EXPLANATION ---------------- #
        st.markdown("### 🤖 AI Explanation")

        if pred == 1:
            st.write("This message matches patterns commonly found in scam messages.")

        if unrealistic:
            st.write("The message contains an unrealistic amount, which is a strong scam indicator.")

        if "Greed" in psych:
            st.write("• It tries to attract you using money or rewards.")

        if "Authority" in psych:
            st.write("• It pretends to be from a trusted source like a bank or organization.")

        if "Urgency" in psych:
            st.write("• It creates urgency to make you act quickly.")

        if "Fear" in psych:
            st.write("• It uses fear to manipulate your decision.")

        # ---------------- SAFETY ADVICE ---------------- #
        st.markdown("### 🛡️ Safety Advice")

        if pred == 1 or unrealistic or len(psych) >= 2:
            st.warning("Do NOT share personal details, OTP, or bank information.")
            st.warning("Avoid clicking unknown links.")
        else:
            st.info("No immediate threat detected, but always stay cautious.")

        # ---------------- FEEDBACK FORM ---------------- #
        st.markdown("---")
        st.markdown("### 📝 Help improve the model — give feedback")
        with st.form("feedback_form"):
            was_correct = st.radio("Was the prediction correct?", ("Yes", "No"))
            comments = st.text_area("Comments (optional)")
            submit_fb = st.form_submit_button("Submit feedback")
            if submit_fb:
                # append feedback to CSV
                row = [datetime.datetime.utcnow().isoformat(), st.session_state['msg'], pred, float(prob), was_correct, comments]
                write_header = not os.path.exists(FEEDBACK_CSV)
                with open(FEEDBACK_CSV, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    if write_header:
                        writer.writerow(["timestamp_utc", "message", "pred", "prob", "was_correct", "comments"])
                    writer.writerow(row)
                st.success("Thanks — your feedback has been recorded.")

# ---------------- FOOTER ---------------- #
st.divider()
st.caption("🧠 Built with Machine Learning + Psychological Analysis | 🔍 Digital Safety Tool")
