import streamlit as st
from core import database
from datetime import datetime

# Configure page (must be first)
st.set_page_config(page_title="Campus Problem Solver", page_icon="🎓", layout="wide")

from core.utils import load_css
load_css()

# Ensure DB is ready
database.init_db()

# Sidebar Navigation (Streamlit standard is to auto-discover pages in pages/ folder)
st.sidebar.success("Select a page above.")
st.sidebar.caption("© Campus Problem Solver Suite")

# Home / Landing page
st.markdown("""
<div class="hackathon-hero">
    <h1 style="font-size: 3.5rem; margin-bottom: 0;">🎓 Campus Solver AI</h1>
    <p style="color: #a4b0be; font-size: 1.2rem; margin-top: 10px;">Next-Generation Automated Incident Routing & Analytics</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1.5, 1])

with col1:
    st.markdown("""
    <div style="background: rgba(255,255,255,0.02); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
        <h3>⚙️ The AI Workflow</h3>
        <p><b>1. Contextual Submission:</b> Multi-modal input capturing text & images.</p>
        <p><b>2. LLM Classification:</b> Powered by Gemini, the system autonomously understands intent.</p>
        <p><b>3. Semantic Routing:</b> Problems are instantly dispatched to the exact campus authority.</p>
        <p><b>4. Real-time Tracking:</b> Full visibility over the resolution lifecycle.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>Live Analytics</h3>", unsafe_allow_html=True)
    problems = database.get_all_problems()
    
    today = datetime.now().date()
    submitted_today = sum(1 for p in problems if datetime.fromisoformat(p["submitted_at"]).date() == today)
    resolved_today = sum(1 for p in problems if p["status"] == "Resolved" and datetime.fromisoformat(p["updated_at"]).date() == today)
    
    st.metric("Incidents Logged (Today)", submitted_today)
    st.metric("Incidents Resolved", resolved_today)

st.markdown("---")
st.info("👈 Initialize a new incident from the Sidebar or view global tracking metrics.")
