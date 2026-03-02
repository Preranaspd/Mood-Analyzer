import streamlit as st

st.set_page_config(page_title="AI Mood Analyzer", page_icon="🧠")

# login control
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# redirect to login page if not logged in
if not st.session_state.logged_in:
    st.switch_page("pages/4_Login.py")

st.title("🌙 AI Mood Analyzer")
st.subheader("Welcome!")

st.write("""
This is your personal AI-powered mood tracker.

Use the sidebar to:
- Write a journal
- View past entries
- Track emotional trends
""")

