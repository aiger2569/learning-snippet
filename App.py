from flask import Flask, render_template, request, session
from backend import create_audio_snippet
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secure secret key!
AUDIO_DIR = os.path.join("static", "Audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    audio_file = None
    display_text = None
    if 'history' not in session:
        session['history'] = []
    if request.method == "POST":
        topics = request.form.get("topics")
        time_limit = int(request.form.get("time_limit", 5))
        audio_file, display_text = create_audio_snippet(topics, time_limit, AUDIO_DIR)
        # Store search in history (as dict)
        new_entry = {"topics": topics, "time_limit": time_limit, "audio_file": audio_file}
        session['history'].append(new_entry)
        session['history'] = session['history'][-5:]  # Keep only last 5
        session.modified = True
    return render_template("index.html", audio_file=audio_file, display_text=display_text, history=session.get('history', []))

if __name__ == "__main__":
    app.run(debug=True)
