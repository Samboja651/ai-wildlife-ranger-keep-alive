"""keep alive worker for the ai wildlife ranger server on render"""
import time
from datetime import datetime
import requests

# Define the endpoint to ping
KEEP_ALIVE_URL = "https://ai-wildlife-ranger.onrender.com/"
LOG_FILE = "keep_alive_log.txt"

def log_message(message):
    """Log a message with a timestamp to a file."""
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {message}\n")

def keep_server_alive():
    """Send a request to the server every 5 minutes to keep it active."""
    while True:
        try:
            response = requests.get(KEEP_ALIVE_URL, timeout=100)
            if response.status_code == 200:
                message = f"Server is active. Response: {response.status_code}"
                log_message(message)
            else:
                message = f"Unexpected response: {response.status_code}"
                log_message(message)
        except requests.RequestException:
            message = "Failed to reach the server. Network Issue"
            log_message(message)
        
        # Wait for 10 minutes before sending the next request
        time.sleep(600)

if __name__ == "__main__":
    keep_server_alive()

# Instructions to run and stop the script using nohup:
# -----------------------------------------------------
# 1. To run the script in the background and log output to keep_alive_log.txt:
#    nohup python3 keep_alive_worker.py > keep_alive_log.txt 2>&1 &
#
#    - `nohup`: Ensures the script continues running even after the terminal is closed.
#    - `python3 keep_alive_worker.py`: Runs the script.
#    - `> keep_alive_log.txt`: Redirects stdout to the log file.
#    - `2>&1`: Redirects stderr to the same log file as stdout.
#    - `&`: Runs the script in the background.
#
# 2. To check the running process:
#    ps aux | grep keep_alive_worker.py
#
# 3. To stop the script:
#    Find the process ID (PID) from the above command and kill it:
#    kill <PID>

# 4. You have to run the script again if your laptop shutsdwon or restarts.
