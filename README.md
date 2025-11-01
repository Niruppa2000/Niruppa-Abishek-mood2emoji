# firstname-lastname-mood2emoji

Simple kid-safe Mood2Emoji app (Streamlit + TextBlob / small rule-based fallback).

## What it does
A minimal web app that accepts a short sentence and returns a kid-friendly emoji (😀 😐 😞) and a one-line explanation. Contains a safe filter for bad words and a Teacher Mode that shows a simple diagram of how the app works.

## Setup & Run (local)
1. Clone repo: `git clone https://github.com/<your-username>/firstname-lastname-mood2emoji.git`
2. Create virtual env (recommended): `python -m venv venv && source venv/bin/activate` (Windows: `venv\\Scripts\\activate`)
3. Install: `pip install -r requirements.txt`
4. (If using TextBlob for the first time) download required corpora:
   ```bash
   python -m textblob.download_corpora
   ```
5. Run: `streamlit run app.py`

## How kids learn from it
- Introduces the idea of text -> meaning mapping.
- Demonstrates a simple rule-based approach and a basic statistical sentiment analyzer (TextBlob).
- Encourages critical thinking about edge cases and why models can be wrong (bias, slang, emojis).

## 60-minute teaching plan (high-level)
See `lesson_plan.pdf` in the repo for the full lesson plan.

## Known limitations
- Very small bad-word list — expand for production.
- TextBlob is simple and can mis-handle sarcasm, slang, or mixed sentiment.
- Not intended for diagnosing mental-health issues.

## Credits
Built for the Curriculum Developer Intern assignment. Uses TextBlob (open-source).

## Deployment notes
- To deploy quickly, use Streamlit Community Cloud (share.streamlit.io). See below for steps.
