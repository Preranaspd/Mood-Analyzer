# pages/3_Trends.py
import streamlit as st
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("pages/4_Login.py")

import streamlit as st
from storage import load_entries
import matplotlib.pyplot as plt
import pandas as pd

st.title("📊 Mood Trends")
df = load_entries()

if df.empty:
    st.info("No data yet.")
else:
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    fig, ax = plt.subplots()
    ax.plot(df["Date"], df["Mood"].astype(int), marker="o")
    ax.set_ylim(0.5, 5.5)
    ax.set_xlabel("Date")
    ax.set_ylabel("Mood (1-5)")
    ax.set_title("Mood Over Time")
    plt.xticks(rotation=45)
    st.pyplot(fig)

