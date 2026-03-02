import streamlit as st
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("pages/4_Login.py")

import streamlit as st
from analysis import analyze_journal

st.title("📝 AI Mood Analyzer – Journal Page")

st.write("Write your journal entry below and the AI will analyze your mood.")

# Input text box
text = st.text_area("Your Journal Entry", height=200)

# Submit button
if st.button("Analyze My Mood"):
    if text.strip() == "":
        st.warning("Please enter something in your journal.")
    else:
        with st.spinner("Analyzing your mood..."):
            try:
                res = analyze_journal(text)   # res will be a dictionary

                st.subheader("🌤 Overall Mood")
                st.write(res["sentiment"])

                st.subheader("📊 Mood Score (1–10)")
                st.write(res["score"])

                st.subheader("💬 Main Emotions")
                st.write(res["emotions"])

                st.subheader("💡 Advice")
                st.write(res["advice"])

            except Exception as e:
                st.error("Something went wrong.")
                st.error(str(e))
