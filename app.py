from flask import Flask, render_template, request, jsonify
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter

nltk.download('punkt')

app = Flask(__name__)

# Load receptionists data
def load_receptionists():
    try:
        with open('data/receptionists.txt') as f:
            receptionists = f.read().splitlines()
    except FileNotFoundError:
        receptionists = []
    return receptionists

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/reviews', methods=['POST'])
def analyze_reviews():
    data = request.json.get('reviews')
    receptionists = load_receptionists()

    # Tokenize and count mentions
    tokens = word_tokenize(data)
    counts = Counter([token for token in tokens if token in receptionists])

    # Convert counts to a list of dictionaries for JSON response
    result = [{'receptionist': k, 'count': v} for k, v in counts.items()]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
