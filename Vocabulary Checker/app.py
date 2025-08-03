#app.py file
from flask import Flask, render_template, request
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification 
import spacy
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the English language model
try:
    nlp = spacy.load("en_core_web_sm")
    logger.info("spaCy model loaded successfully")
except Exception as e:
    logger.error(f"Error loading spaCy model: {e}")
    nlp = None

# Initialize grammar checker
try:
    model_name = "textattack/roberta-base-CoLA"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    grammar_classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, framework="pt")
    logger.info("Grammar classifier loaded successfully")
except Exception as e:
    logger.error(f"Error loading grammar classifier: {e}")
    grammar_classifier = None

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    feedback = None
    if request.method == 'POST':
        sentence = request.form.get('sentence', '').strip()
        target_word = request.form.get('target_word', '').strip()
        expected_pos = request.form.get('expected_pos', '').strip()

        if not sentence or not target_word or not expected_pos:
            feedback = "Please fill in all fields."
        elif nlp is None:
            feedback = "Error: NLP model unavailable."
        else:
            doc = nlp(sentence)
            word_present = any(token.text.lower() == target_word.lower() for token in doc)
            target_token = next((token for token in doc if token.text.lower() == target_word.lower()), None)
            target_pos = target_token.pos_ if target_token else None
            pos_correct = (target_pos == expected_pos.upper()) if target_pos else False

            grammar_result = check_grammar(sentence)
            feedback = generate_feedback(sentence, target_word, word_present, target_pos, pos_correct, grammar_result)

    return render_template('index.html', feedback=feedback)

def check_grammar(sentence):
    if grammar_classifier is None:
        return {'is_grammatical': None, 'confidence': None, 'error': 'Grammar checker unavailable'}
    try:
        #Get the first element of the classifier output because its a list of maps
        result = grammar_classifier(sentence)[0]
        return {
            #check if result is equal to LABEL_1
            'is_grammatical': result['label'] == 'LABEL_1',
            'confidence': result['score'],
            'error': None
        }
    except Exception as e:
        logger.error(f"Grammar check error: {e}")
        return {'is_grammatical': None, 'confidence': None, 'error': str(e)}

def generate_feedback(sentence, word, found, pos, pos_ok, grammar):
    lines = [
        f"<strong>Sentence:</strong> '{sentence}'",
        f"<strong>Target word:</strong> '{word}'"
    ]
    if found:
        lines.append("Word found: Yes")
        lines.append(f"Part of speech: {pos}")
        lines.append("POS usage: Correct" if pos_ok else f"POS usage: Incorrect (found: {pos})")
    else:
        lines.append("Word found: No")

    if grammar['error']:
        lines.append(f"Grammar check: {grammar['error']}")
    else:
        verdict = "Correct" if grammar['is_grammatical'] else "Incorrect"
        lines.append(f"Grammar: {verdict} (confidence: {grammar['confidence']:.2f})")

    return "<br>".join(lines)

if __name__ == '__main__':
    app.run(debug=True)