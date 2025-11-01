import streamlit as st
from textblob import TextBlob
import re

# Small list of bad words for kid-safe filtering (add more if needed)
BAD_WORDS = {"damn", "hell", "shit", "bastard", "ass"}

# Mapping polarity thresholds to emoji and one-line explanation
def mood_from_polarity(p):
    if p > 0.15:
        return "😀", "Sounds happy!"
    elif p < -0.15:
        return "😞", "Looks sad."
    else:
        return "😐", "Seems neutral."

# Rule-based fallback if TextBlob not available or gives neutral
POS_WORDS = {"happy","good","great","awesome","love","yay","fantastic","excited"}
NEG_WORDS = {"sad","angry","hate","upset","bad","terrible","cry","mad","depressed"}

def rule_based_mood(text):
    tokens = re.findall(r"\w+", text.lower())
    pos = sum(1 for w in tokens if w in POS_WORDS)
    neg = sum(1 for w in tokens if w in NEG_WORDS)
    if pos > neg:
        return "😀", "Sounds happy!"
    if neg > pos:
        return "😞", "Looks sad."
    return "😐", "Seems neutral."

def contains_bad_word(text):
    tokens = re.findall(r"\w+", text.lower())
    return any(t in BAD_WORDS for t in tokens)

st.set_page_config(page_title="Mood2Emoji — Kid-safe Text Mood Detector", layout="centered")
st.title("Mood2Emoji — Kid-safe Text Mood Detector")
st.write("Type a short sentence (for ages 12–16) and get a kid-friendly emoji + short explanation.")

with st.form(key='input_form'):
    sentence = st.text_input("Enter a short sentence:")
    submitted = st.form_submit_button("Detect Mood")

teacher_mode = st.checkbox("Teacher Mode: show how it works")

if teacher_mode:
    st.subheader("How the app works (simple diagram)")
    st.graphviz_chart("""
        digraph G {
          rankdir=LR;
          Input -> Filter;
          Filter -> Analyzer;
          Analyzer -> Output;
          Analyzer -> Fallback [style=dashed];
          Filter [shape=box, label="Filter bad words\n(age-appropriate)"];
          Analyzer [shape=box, label="TextBlob sentiment\n(or rule-based fallback)"];
          Output [shape=box, label="Emoji + 1-line explanation"];
          Fallback [shape=box, label="Neutral fallback for\nunknown/inappropriate text"];
        }
    """)
    st.markdown("**Teacher notes:** We use a simple sentiment score (polarity) to decide mood. If TextBlob is unavailable or the sentence is ambiguous, we fall back to a small rule-based keyword check. Bad words cause a neutral/inappropriate response to keep output kid-safe.")

if submitted:
    if not sentence or sentence.strip() == "":
        st.info("Please type a short sentence to analyze.")
    else:
        # Safety filter
        if contains_bad_word(sentence):
            st.warning("⚠️ This message contains words that aren't age-appropriate. Showing neutral response.")
            st.write("**Result:** 😐 — Seems neutral.")
        else:
            # Try TextBlob first
            try:
                blob = TextBlob(sentence)
                polarity = blob.sentiment.polarity
                emoji, explanation = mood_from_polarity(polarity)
                # If polarity is very near zero, try rule-based to be friendlier
                if abs(polarity) < 0.12:
                    rb_emoji, rb_expl = rule_based_mood(sentence)
                    # prefer rule-based if it finds strong signal
                    if rb_emoji != "😐":
                        emoji, explanation = rb_emoji, rb_expl
            except Exception as e:
                # Fallback
                emoji, explanation = rule_based_mood(sentence)

            st.markdown(f"### Result: {emoji} \n**{explanation}**")
            st.caption("This is a lightweight approach for learning purposes. Not a medical or professional assessment.")

        # Example teaching tip
        if teacher_mode:
            st.markdown("**In-class activity idea:** Let students enter 3-5 short sentences and compare the emoji results — discuss edge cases and why the app might be wrong sometimes.")
