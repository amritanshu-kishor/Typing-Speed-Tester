from flask import Flask, render_template, request
import time
import random

app = Flask(__name__)

# Function to fetch random paragraphs manually added
def get_random_paragraph():
    try:
        # List of predefined paragraphs
        paragraphs = [
            "The quick brown fox jumps over the lazy dog. Python is a great programming language. Typing speed tests are fun and challenging.",
            "Artificial intelligence is transforming the world. Machine learning and deep learning are subsets of AI that are widely used today.",
            "Typing speed tests help improve your accuracy and speed. Practice regularly to become a faster and more accurate typist.",
            "Programming is a skill that requires patience and practice. Debugging is an essential part of the development process."
        ]
        # Choose a random paragraph
        return random.choice(paragraphs)
    except Exception as e:
        print(f"Error selecting paragraph: {e}")
        return "The quick brown fox jumps over the lazy dog. Python is a great programming language. Typing speed tests are fun and challenging."

@app.route('/')
def index():
    # Fetch a random paragraph and pass it to the template
    sentence = get_random_paragraph()
    timer_duration = 5  # Extend the timer to 15 seconds
    return render_template('index.html', sentence=sentence, timer_duration=timer_duration)

@app.route('/submit_test', methods=['POST'])
def submit_test():
    # Retrieve form data
    sentence = request.form['sentence']
    user_input = request.form['user_input']
    start_time = float(request.form['start_time'])
    end_time = time.time()
    
    # Calculate elapsed time, WPM, and accuracy
    elapsed_time = end_time - start_time
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
        timer_duration=15  # Keep the timer duration consistent
    )

if __name__ == "__main__":
    app.run(debug=True)
