"""Flask-based keep alive worker for the AI Wildlife Ranger server on Render."""
import time
import os
from datetime import datetime
from multiprocessing import Process
from dotenv import load_dotenv
from flask import Flask, jsonify
import requests

load_dotenv('.env')
# Flask app setup
app = Flask(__name__)


# endpoint to ai wildlife ranger
PING_ADDICTION_SOLVER = os.getenv('PING_ADDICTION_SOLVER')
PING_AI_WILDLIFE_RANGER = os.getenv('PING_AI_WILDLIFE_RANGER')
PING_PB_BACKEND = os.getenv("PING_PB_BACKEND")

LOG_FILE = "keep_alive_log.txt"

def log_message(message):
    """Log a message with a timestamp to a file."""
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {message}\n")
        log_file.flush()  # Ensure logs are written immediately
    print(f"[{timestamp}] {message}")  # Print to console for debugging

def ping_servers():
    """Send a request to each app server to keep them alive."""
    while True:
        try:
            res_addiction_solver = requests.get(PING_ADDICTION_SOLVER, timeout=10)
            res_ai_wildlife_ranger = requests.get(PING_AI_WILDLIFE_RANGER, timeout=10)
            res_pb_backend = requests.get(PING_PB_BACKEND, timeout=10)

            if res_addiction_solver.status_code == 200 and res_ai_wildlife_ranger.status_code == 200:
                message_arts = f"Ping to addiction- solver was successful. Response: {res_addiction_solver.json().get('message')}"
                print(message_arts)
                log_message(message_arts)

                message_ranger = f"Ping to ai-wildlife-ranger was successful. Response: {res_ai_wildlife_ranger.json().get('message')}"
                print(message_ranger)
                log_message(message_ranger)
            elif res_addiction_solver.status_code == 200 or res_ai_wildlife_ranger.status_code == 200:
                message_arts = f"Ping to addiction- solver was successful. Response: {res_addiction_solver.json().get('message')}"
                print(message_arts)
                log_message(message_arts)

                message_ranger = f"Ping to ai-wildlife-ranger was successful. Response: {res_ai_wildlife_ranger.json().get('message')}"
                print(message_ranger)
                log_message(message_ranger)
            else:
                message = f"{"Addiction solver: ", res_addiction_solver.status_code, "Ranger: ", res_ai_wildlife_ranger.status_code, "PB:", res_pb_backend}"
                print(message)
                log_message(message)
        except requests.RequestException as e:
            message = f"Failed to reach app.py. Network Issue: {e}"
            log_message(message)
        finally:
            # Wait for 10 minutes before sending the next request
            time.sleep(600)

@app.route('/ping', methods=['GET'])
def handle_ping():
    """Handle incomig ping requests"""
    # log_message("Received ping from addiction- solver: Active")
    return jsonify({"message": "Keep Alive Worker is active"}), 200

# Start the ping app servers function as a separate process
ping_process = Process(target=ping_servers)
ping_process.start()

if __name__ == "__main__":
    # Start the Flask app
    app.run(debug=False, port=5001)
