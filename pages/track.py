import streamlit as st
from core import database
from datetime import datetime
from core.utils import load_css

st.set_page_config(page_title="Track Your Problem", page_icon="🔍", layout="wide")
load_css()

st.title("🔍 Track Your Problem")

# We use columns to center the input nicely
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("Enter your Tracking ID to view the live status of your complaint.")
    
    # Retrieve value from session state if it was just submitted
    default_id = st.session_state.get("tracking_id", "")
    
    with st.form("track_form"):
        tracking_id = st.text_input("Tracking ID", value=default_id, placeholder="e.g. 5A92B4F1")
        submitted = st.form_submit_button("Track Status")

    if submitted or default_id:
        search_id = tracking_id if submitted else default_id
        if search_id:
            problem = database.get_problem(search_id.upper())
            
            if problem:
                st.markdown("---")
                
                # Determine status color
                status_color = "blue"
                icon = "📝"
                if problem['status'] == "Resolved":
                    status_color = "green"
                    icon = "✅"
                elif problem['status'] == "In Progress":
                    status_color = "orange"
                    icon = "⏳"

                st.markdown(f"### {icon} Status: :{status_color}[**{problem['status']}**]")
                
                with st.container():
                    st.info(f"**Category:** {problem['category']} | **Assigned To:** {problem['department']}")
                    
                    st.markdown("#### Description")
                    st.write(f"> {problem['description']}")
                    
                    if problem['resolution_note']:
                        st.markdown("#### 💬 Resolution Note")
                        st.success(problem['resolution_note'])
                    
                    st.caption(f"Submitted on: {problem['submitted_at']} | Last Updated: {problem['updated_at']}")
            else:
                st.error("Tracking ID not found. Please check and try again.")
