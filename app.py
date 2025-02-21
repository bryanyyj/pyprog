import flask
from flask import Flask, render_template, Response, json
import time

app = Flask(__name__)
JSON_FILE = "display.json"

def read_json():
    try:
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
            return data.get("numbers", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def generate_numbers():
    last_seen = []
    while True:
        time.sleep(1)  # Check for updates every second
        numbers = read_json()
        if numbers != last_seen:  # Send update only if the content changes
            last_seen = numbers
            yield f"data: {json.dumps(numbers)}\n\n"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    return Response(generate_numbers(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
