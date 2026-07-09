import os
import sys
import streamlit as st

# Ensure the model directory is on sys.path so local modules can be imported reliably
ROOT_DIR = os.path.dirname(__file__)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from detector import predict_message

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

# ---------------- INPUT ---------------- #
msg = st.text_area("✍️ Enter Message", height=150, placeholder="Paste suspicious message here...")

# ---------------- BUTTON ---------------- #
if st.button("🔍 Scan Message", use_container_width=True):

    if msg.strip() == "":
        st.warning("Please enter a message!")
    else:
        pred, prob, psych, unrealistic, link_flag = predict_message(msg)

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

        # ---------------- PROBABILITY ---------------- #
        st.markdown("### 📊 Scam Probability")
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

# ---------------- FOOTER ---------------- #
st.divider()
st.caption("🧠 Built with Machine Learning + Psychological Analysis | 🔍 Digital Safety Tool")
