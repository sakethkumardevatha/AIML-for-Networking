import streamlit as st
import joblib
import urllib.parse
import re

# Load the trained model
@st.cache_resource
def load_model():
    return joblib.load("model/sqli_detector.pkl")

model = load_model()

# Extract payload from query or URL
def extract_payload(raw_input):
    if "?" in raw_input:
        parsed = urllib.parse.urlparse(raw_input)
        query_params = urllib.parse.parse_qs(parsed.query)
        payload = " ".join([" ".join(v) for v in query_params.values()])
    else:
        payload = raw_input
    return urllib.parse.unquote(payload).lower().strip()

# Rule-based pattern detection
def is_obviously_malicious(payload):
    patterns = [
        r"union\s+select",
        r"drop\s+table",
        r"--",
        r";",
        r"or\s+1=1",
        r"admin'\s*--",
        r"'1'='1",
        r"sleep\(",
        r"shutdown",
        r"insert\s+into",
        r"alter\s+table"
    ]
    return any(re.search(p, payload, re.IGNORECASE) for p in patterns)

# Final prediction function
def check_input(raw_input):
    payload = extract_payload(raw_input)
    
    if is_obviously_malicious(payload):
        result = "🔴 Malicious"
        confidence = 0.99
    else:
        prediction = model.predict([payload])[0]
        confidence = model.predict_proba([payload])[0][prediction]
        result = "🔴 Malicious" if prediction == 1 else "🟢 Safe"
    
    return payload, result, confidence

# ✅ Streamlit UI
st.set_page_config(page_title="SQL Injection Detector", page_icon="🛡")

st.title("🛡 SQL Injection Detection App")
st.write(
    """
    This AI + Rule-Based app checks if a given SQL query or URL input is likely to contain a SQL Injection attack.  
    - 🚩 *Red means Malicious*  
    - ✅ *Green means Safe*  
    """
)

query = st.text_area("🔍 Enter SQL query or URL:")

if st.button("Check Now"):
    if query.strip():
        payload, result, confidence = check_input(query)
        
        st.subheader("🔎 Analysis Result")
        st.write(f"*Extracted Payload:* {payload}")
        st.write(f"*Prediction:* {result}")
        st.write(f"*Confidence:* {confidence:.2%}")
        
        if result == "🔴 Malicious":
            st.error("⚠ Possible SQL Injection detected!")
        else:
            st.success("✅ No obvious SQL Injection found.")
    else:
        st.warning("Please enter a valid SQL query or URL above.")

st.caption("Built with Streamlit | No API keys needed | Local use only ✅")
