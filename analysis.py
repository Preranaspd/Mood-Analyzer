# analysis.py (robust analyze_journal)
import os
import json
import re
from time import sleep
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY not set. Add it to your .env or env vars.")
client = OpenAI(api_key=API_KEY)

def _extract_json_from_text(text):
    """Find first {...} JSON block in text and return it, else None."""
    m = re.search(r"\{(?:[^{}]|(?R))*\}", text, re.S)  # recursive regex if supported
    if not m:
        # fallback simpler regex for most cases
        m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    return m.group()

def _call_model_and_get_text(journal_text, mood, model="gpt-4o-mini"):
    system = "You are an empathetic assistant that must return output ONLY as a single JSON object, with no extra text."
    user = (
        f"Analyze the journal entry below and return ONLY one JSON object with EXACT keys:\n"
        f'\"sentiment\" (one of \"positive\", \"neutral\", \"negative\"),\n'
        f'\"score\" (integer 1-10),\n'
        f'\"emotions\" (short comma-separated string),\n'
        f'\"advice\" (array with exactly two short sentences).\n\n'
        f"Journal entry:\n\"\"\"{journal_text}\"\"\"\n\nMood rating (1-5): {mood}\n\n"
        f"Return only one JSON object and nothing else."
    )
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        temperature=0.2,
        max_tokens=400
    )
    # Use the content from the assistant
    return resp.choices[0].message.content

def analyze_journal(text, *args, **kwargs):
    # Reject gibberish / too-short entries
    if len(text.strip()) < 10:
        return {
            "sentiment": "Invalid",
            "score": 0,
            "emotions": "None",
            "advice": "Please write a meaningful journal entry with complete thoughts."
        }
    """
    Returns a dict: {sentiment, score, emotions, advice}
    On failure returns dict with safe defaults and an 'error' field.
    """
    try:
        # 1) primary call
        reply = _call_model_and_get_text(text, kwargs.get("mood", 3))

        # debug: you can print reply to terminal during development
        # print("DEBUG: model reply:", repr(reply))

        # 2) attempt to extract JSON block
        json_text = _extract_json_from_text(reply)
        if json_text:
            try:
                data = json.loads(json_text)
                # basic normalization / safety
                sentiment = data.get("sentiment", "").lower()
                score = int(data.get("score")) if str(data.get("score")).isdigit() else None
                emotions = data.get("emotions", "")
                advice = data.get("advice", [])
                if isinstance(advice, str):
                    # split lines or commas
                    advice = [a.strip() for a in re.split(r'[\n\r]+|;|,', advice) if a.strip()][:2]
                # ensure advice is list of 2 strings
                if not isinstance(advice, list):
                    advice = [str(advice)]
                advice = advice[:2] + ([""] * 2)[:max(0, 2 - len(advice))]
                return {
                    "sentiment": sentiment or "neutral",
                    "score": score or 5,
                    "emotions": emotions or "",
                    "advice": advice
                }
            except Exception:
                # parse failed — we'll retry
                pass

        # 3) Retry: ask model to return ONLY JSON (short prompt)
        sleep(0.5)
        retry_prompt = (
            "The previous response was not valid JSON. Return again ONLY a single valid JSON object "
            "with keys: sentiment (positive/neutral/negative), score (1-10), emotions, advice (array of two short sentences)."
        )
        resp2 = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant that must output only valid JSON."},
                {"role": "user", "content": retry_prompt}
            ],
            temperature=0.0,
            max_tokens=200
        )
        reply2 = resp2.choices[0].message.content
        json_text2 = _extract_json_from_text(reply2)
        if json_text2:
            try:
                data = json.loads(json_text2)
                sentiment = data.get("sentiment", "").lower()
                score = int(data.get("score")) if str(data.get("score")).isdigit() else None
                emotions = data.get("emotions", "")
                advice = data.get("advice", [])
                if isinstance(advice, str):
                    advice = [a.strip() for a in re.split(r'[\n\r]+|;|,', advice) if a.strip()][:2]
                if not isinstance(advice, list):
                    advice = [str(advice)]
                advice = advice[:2] + ([""] * 2)[:max(0, 2 - len(advice))]
                return {
                    "sentiment": sentiment or "neutral",
                    "score": score or 5,
                    "emotions": emotions or "",
                    "advice": advice
                }
            except Exception:
                pass

        # final fallback: return safe defaults + include raw reply for debugging
        return {
            "sentiment": "neutral",
            "score": 5,
            "emotions": "",
            "advice": ["Try a short walk.", "Write down one thing you're grateful for."],
            "error": "Could not parse JSON from model response.",
            "raw": reply  # useful for debugging (remove in production)
        }

    except Exception as e:
        return {
            "sentiment": "neutral",
            "score": 5,
            "emotions": "",
            "advice": ["Take a deep breath.", "Talk to a friend."],
            "error": f"Exception during analysis: {str(e)}"
        }

