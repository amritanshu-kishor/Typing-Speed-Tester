# Typing Speed Tester

Lightweight typing speed and accuracy tester built with Flask (Python) and a minimal HTML/CSS frontend.

## Features
- Measures words-per-minute (WPM) and accuracy
- Uses online paragraph source with a local fallback
- Single-file Flask app for easy setup

## Requirements
- Python 3.8+
- pip

Optional: create and use a virtual environment to keep dependencies isolated.

## Quick start
1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

2. Install dependencies and run:

```bash
pip install flask
python app.py
```

3. Open the app in your browser: `http://127.0.0.1:5000`

## Development notes
- The app entrypoint is `app.py`.
- Templates are in the `templates/` folder and static assets are under `static/`.
- To change the paragraph source or add features, modify `app.py` and the template `templates/index.html`.

## Project layout

- `app.py` — Flask application
- `templates/` — HTML templates (contains `index.html`)
- `static/` — CSS and client-side assets

## Contributing
Feel free to open issues or pull requests. Keep changes small and include brief descriptions of behavior.

## License
See the `LICENSE` file for license details.
