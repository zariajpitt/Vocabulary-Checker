# Vocabulary Productivity Checker 🧠

This is a Flask-based web app that helps language learners practice vocabulary in context. Learners input a sentence, a target word, and the expected part of speech (POS). The system evaluates:

- Whether the word appears in the sentence
- Whether it's used with the correct POS
- Whether the sentence is grammatically acceptable using a pretrained model from Hugging Face (CoLA)

### 💡 Tech Stack
- Python + Flask
- spaCy (for POS tagging)
- Hugging Face Transformers (`textattack/roberta-base-CoLA` for grammar checking)
- HTML + CSS frontend

### ✅ Example Usage

Input:
- Sentence: `He always run fast.`
- Target Word: `run`
- Expected POS: `VERB`

Output:
- Word found: Yes
- Part of speech: VERB
- POS usage: ✅
- Grammar: ❌ (confidence: 0.12)

### 🛠️ To Run the App
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Run with: `python app.py`
