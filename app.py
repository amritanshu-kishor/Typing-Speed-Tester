from flask import Flask, render_template, request
import time
import random
import urllib.request
import urllib.parse
import json

app = Flask(__name__)

FALLBACK_PARAGRAPHS = [
    "The quick brown fox jumps over the lazy dog. Python is a great programming language. Typing speed tests are fun and challenging.",
    "Artificial intelligence is transforming the world. Machine learning and deep learning are subsets of AI that are widely used today.",
    "Typing speed tests help improve your accuracy and speed. Practice regularly to become a faster and more accurate typist.",
    "Programming is a skill that requires patience and practice. Debugging is an essential part of the development process.",
]


def _normalize_paragraph(text: str) -> str:
    text = (text or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    text = " ".join(text.split())
    return text


def _mostly_ascii_english(text: str) -> bool:
    if not text:
        return False
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return False
    ascii_letters = sum(1 for c in letters if "a" <= c.lower() <= "z")
    return (ascii_letters / len(letters)) >= 0.95


def get_online_paragraph(min_words: int = 35, timeout_s: float = 3.5) -> str | None:
    """
    Fetches a paragraph from Quotable (English quotes, no API key needed).
    Returns None on failure.
    """
    try:
        params = urllib.parse.urlencode({"minLength": 200, "maxLength": 320})
        url = f"https://api.quotable.io/random?{params}"
        with urllib.request.urlopen(url, timeout=timeout_s) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
        if not isinstance(data, dict) or "content" not in data:
            return None
        paragraph = _normalize_paragraph(data.get("content"))
        if len(paragraph.split()) < min_words:
            return None
        if not _mostly_ascii_english(paragraph):
            return None
        return paragraph
    except Exception:
        return None


def get_random_paragraph() -> str:
    online = get_online_paragraph()
    if online:
        return online
    return random.choice(FALLBACK_PARAGRAPHS)

@app.route('/')
def index():
    # Fetch a random paragraph and pass it to the template
    sentence = get_random_paragraph()
    timer_duration = 5
    return render_template('index.html', sentence=sentence, timer_duration=timer_duration)

@app.route('/submit_test', methods=['POST'])
def submit_test():
    # Retrieve form data
    sentence = request.form['sentence']
    user_input = request.form['user_input']
    start_time = float(request.form['start_time'])
    end_time = time.time()
    
    # Calculate elapsed time, WPM, and accuracy
    elapsed_time = max(0.01, end_time - start_time)
    words = len(sentence.split())
    user_words = len(user_input.split())
    correct_words = sum(1 for a, b in zip(sentence.split(), user_input.split()) if a == b)

    wpm = (user_words / elapsed_time) * 60
    accuracy = (correct_words / words) * 100

    # Pass results back to the template
    return render_template(
        'index.html',
        sentence=sentence,
        user_input=user_input,
        elapsed_time=round(elapsed_time, 2),
        wpm=round(wpm, 2),
        accuracy=round(accuracy, 2),
        timer_duration=5,
    )

if __name__ == "__main__":
    app.run(debug=True)
