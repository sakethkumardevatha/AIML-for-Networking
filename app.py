import streamlit as st
import joblib

# Load the model pipeline (which includes vectorizer + model)
@st.cache_resource
def load_model():
    return joblib.load("model/sqli_detector.pkl")

model = load_model()

st.set_page_config(page_title="SQL Injection Detection", layout="centered")

st.markdown("## 🛡 SQL Injection Detection App")
st.markdown("This AI-powered app checks SQL queries or URLs for possible SQL Injection threats.\n\n"
            "🚩 **Red** means Malicious\n"
            "✅ **Green** means Safe")

user_input = st.text_area("🔍 Enter one or more SQL queries or URLs (one per line):")

if user_input:
    inputs = [line.strip() for line in user_input.strip().split('\n') if line.strip()]
    if inputs:
        preds = model.predict(inputs)
        probs = model.predict_proba(inputs)

        st.markdown("### 🔎 Analysis Results")
        for i, query in enumerate(inputs):
            label = preds[i]
            confidence = probs[i][label] * 100
            st.write(f"**Query {i+1}:** `{query}`")
            st.write(f"**Prediction:** {'🔴 Malicious' if label == 1 else '✅ Safe'}")
            st.write(f"**Confidence:** {confidence:.2f} %")
            st.markdown("---")
