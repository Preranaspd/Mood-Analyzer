# pages/2_History.py
import streamlit as st
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("pages/4_Login.py")

import streamlit as st
from storage import load_entries
st.title("📚 History")
df = load_entries()
if df.empty:
    st.info("No entries yet. Add a journal entry on the Journal page.")
else:
    st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)
    csv = df.to_csv(index=False)
    st.download_button("Download CSV", csv, file_name="journal_history.csv")

