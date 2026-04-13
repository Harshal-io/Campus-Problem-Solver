import streamlit as st
import pandas as pd
import os
from core import database
from core.utils import load_css

st.set_page_config(page_title="Admin Dashboard", page_icon="🛠️", layout="wide")
load_css()

st.title("🛠️ Admin Dashboard")

# Basic Password Authentication
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
if not ADMIN_PASSWORD:
    try:
        ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "admin123")  # fallback for testing
    except:
        ADMIN_PASSWORD = "admin123"

if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

if not st.session_state["admin_logged_in"]:
    st.info("Please log in to manage campus problems.")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if pwd == ADMIN_PASSWORD:
            st.session_state["admin_logged_in"] = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()

# Admin is logged in below this line
st.success("Logged in as Administrator")
st.markdown("---")

problems = database.get_all_problems()
df = pd.DataFrame(problems)

if df.empty:
    st.write("No problems have been submitted yet.")
    st.stop()

# --- Metrics Header ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Problems", len(df))
col2.metric("In Progress", len(df[df["status"] == "In Progress"]))
col3.metric("Resolved", len(df[df["status"] == "Resolved"]))

st.markdown("---")

# --- EMERGENCY DISTRESS RADAR ---
distress_df = df[df["urgency"] == "CRITICAL"] if "urgency" in df.columns else pd.DataFrame()
if not distress_df.empty:
    st.error("🚨 **CRITICAL DISTRESS ACTIVE** 🚨 Requires Immediate Intervention")
    for _, row in distress_df.iterrows():
        with st.expander(f"EMERGENCY: {row['id']} - {row['category']} (Author: {row.get('reg_no', 'Unknown')})", expanded=True):
            st.error(f"**Contact:** {row.get('email', 'Unknown')}\n\n**Description:** {row['description']}")
            
st.markdown("---")

# --- Interactive Filter ---
st.subheader("Filter Problems")
f_col1, f_col2 = st.columns(2)
departments = ["All"] + sorted(df["department"].unique().tolist())
statuses = ["All"] + sorted(df["status"].unique().tolist())

with f_col1:
    selected_dept = st.selectbox("Department", departments)
with f_col2:
    selected_status = st.selectbox("Status", statuses)

# Apply filters
filtered_df = df.copy()
if selected_dept != "All":
    filtered_df = filtered_df[filtered_df["department"] == selected_dept]
if selected_status != "All":
    filtered_df = filtered_df[filtered_df["status"] == selected_status]

# --- Main Dashboard List ---
st.subheader("Action Center")

for _, row in filtered_df.iterrows():
    # Expandable card for each problem
    urgency_tag = f"[{row.get('urgency', 'MEDIUM')}]"
    with st.expander(f"[{row['status']}] {urgency_tag} {row['id']} - {row['category']} (Assigned to: {row['department']})"):
        st.caption(f"**Author:** {row.get('reg_no', 'N/A')} | **Email:** {row.get('email', 'N/A')}")
        st.write(f"**Description:** {row['description']}")
        if pd.notnull(row['confidence']):
            st.caption(f"AI Classification Confidence: {int(row['confidence']*100)}%")
            
        st.write(f"**Submitted Date:** {row['submitted_at']}")
        
        if 'image_path' in row and pd.notnull(row['image_path']) and str(row['image_path']).strip():
            if os.path.exists(row['image_path']):
                st.image(row['image_path'], caption="Attached Evidence", use_container_width=True)
            else:
                st.error("Attached image file could not be found on disk.")
                
        # Form to update status
        with st.form(key=f"update_form_{row['id']}"):
            new_status = st.selectbox("Update Status", ["Submitted", "In Progress", "Resolved"], 
                                      index=["Submitted", "In Progress", "Resolved"].index(row['status']))
            new_note = st.text_area("Resolution Note / Reply", value=row['resolution_note'] if row['resolution_note'] else "")
            
            submit_update = st.form_submit_button("Update Problem")
            if submit_update:
                database.update_problem_status(row['id'], new_status, new_note)
                st.success(f"Successfully updated {row['id']}!")
                st.rerun()

# --- Export ---
st.markdown("---")
st.subheader("Export Data")
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='campus_problems.csv',
    mime='text/csv',
)
