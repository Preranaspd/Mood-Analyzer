# storage.py
import pandas as pd
import os

FILE = "journal.csv"
COLUMNS = ["Date", "Mood", "Entry", "Sentiment", "Summary", "Advice"]

def load_entries():
    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
        return df
    return pd.DataFrame(columns=COLUMNS)

def save_entry(date, mood, entry, sentiment="", summary="", advice=""):
    df = load_entries()
    new = {
        "Date": date,
        "Mood": mood,
        "Entry": entry,
        "Sentiment": sentiment,
        "Summary": summary,
        "Advice": advice
    }
    df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
    df.to_csv(FILE, index=False)

