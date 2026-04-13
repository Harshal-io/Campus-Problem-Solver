import streamlit as st
import uuid
import os
import time
from datetime import datetime
from core import database, classifier, router
from core.utils import load_css

st.set_page_config(page_title="Submit a Problem", page_icon="🎓", layout="wide")
load_css()

st.title("🎓 Submit a Campus Problem")
st.subheader("Automated Multi-Agent Routing Flow")

os.makedirs("uploads", exist_ok=True)

with st.form("submission_form"):
    st.markdown("### Student Verification")
    col1, col2 = st.columns(2)
    with col1:
        reg_no = st.text_input("Registration Number")
    with col2:
        email = st.text_input("College Email", placeholder="student@iiitranchi.ac.in")
        
    st.markdown("### Incident Details")
    description = st.text_area("Incident Description", placeholder="Feed context to the AI...")
    user_urgency = st.selectbox("Urgency Level", ["LOW", "MEDIUM", "HIGH", "CRITICAL"], index=1)
    image = st.file_uploader("Upload visual evidence (optional)", type=["jpg", "jpeg", "png"])
    submit_button = st.form_submit_button("Engage AI Pipeline")
    
if submit_button:
    if not description.strip() or not reg_no.strip() or not email.strip():
        st.error("All fields (Registration Number, Email, and Description) are required.")
    elif not email.lower().endswith("@iiitranchi.ac.in"):
        st.error("Authentication Error: Only official @iiitranchi.ac.in domains are permitted.")
    else:
        # Emergency Override Protocol
        desc_lower = description.lower()
        distress_keywords = ["fire", "short circuit", "injury", "blood", "accident", "emergency", "danger"]
        if any(keyword in desc_lower for keyword in distress_keywords):
            user_urgency = "CRITICAL"
            st.warning("⚠️ CRITICAL DISTRESS DETECTED - Auto-escalated urgency to CRITICAL.")

        # Pre-checks
        tracking_id = str(uuid.uuid4())[:8].upper()
        image_path = None
        if image:
            image_path = os.path.join("uploads", f"{tracking_id}_{image.name}")
            with open(image_path, "wb") as f:
                f.write(image.getbuffer())

        with st.spinner("Processing with AI Pipeline..."):
            # ─── REAL AI INFERENCE HAPPENS HERE ───
            result = classifier.classify(description.strip(), image_path)
            
            # Pull rich data
            urgency = user_urgency
            entities = ", ".join(result.get("entities", []))
            sentiment = result.get("sentiment", "NEUTRAL")
            reasoning = result.get("reasoning", "Standard routing active.")
            category = result.get("category", "Other")
            confidence = result.get("confidence", 0.0)
            latency = result.get("latency_ms", "N/A")
            
            # DB & Router insertion
            database.insert_problem(tracking_id, description.strip(), reg_no.strip(), email.strip(), urgency, image_path)
            department = router.route_problem(tracking_id, category, confidence)
            st.session_state["tracking_id"] = tracking_id

        st.success("Issue successfully analyzed and routed.")
        
        st.markdown("### Submission Details")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Tracking ID:** {tracking_id}")
            st.write(f"**Classification:** {category}")
            st.write(f"**Urgency:** {urgency}")
        with col2:
            st.write(f"**Assigned Department:** {department}")
            st.write(f"**Entities Detected:** {entities if entities else 'None'}")
        
        # Finish with metrics
        st.write("")
        st.progress(confidence, text=f"Calibration Confidence Score: {int(confidence*100)}%")
        st.caption("🔒 Security Note: Save your Tracking ID to monitor the resolution lifecycle.")
