"""Flask-based keep alive worker for the AI Wildlife Ranger server on Render."""
import time
from datetime import datetime
from multiprocessing import Process
from flask import Flask, jsonify
import requests

# Flask app setup
app = Flask(__name__)

# endpoint to ai wildlife ranger
APP_PING_URL = "https://ai-wildlife-ranger-2.onrender.com/ping"
LOG_FILE = "keep_alive_log.txt"

def log_message(message):
    """Log a message with a timestamp to a file."""
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {message}\n")
        log_file.flush()  # Ensure logs are written immediately
    print(f"[{timestamp}] {message}")  # Print to console for debugging

def ping_app():
    """Send a request to the app.py server to keep it alive."""
    while True:
        try:
            response = requests.get(APP_PING_URL, timeout=300)
            if response.status_code == 200:
                message = f"Ping to ai wildlife ranger successful. Response: {response.json().get('message')}"
                log_message(message)
            else:
                message = f"Either the app server is restarting or is busy: {response.status_code}"
                log_message(message)
        except requests.RequestException as e:
            message = f"Failed to reach app.py. Network Issue: {e}"
            log_message(message)
        finally:
            # Wait for 10 minutes before sending the next request
            time.sleep(600)

@app.route('/ping', methods=['GET'])
def handle_ping():
    """Handle ping requests from https://ai-wildlife-ranger.onrender.com/ping."""
    log_message("Received ping from ai wildlife ranger")
    return jsonify({"message": "Keep Alive Worker is active"}), 200

# Start the ping_app function as a separate process
ping_process = Process(target=ping_app)
ping_process.start()

if __name__ == "__main__":
    # Start the Flask app
    app.run(debug=False, port=5001)
