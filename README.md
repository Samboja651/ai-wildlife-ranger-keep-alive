# Keep Alive Worker

This is a Flask-based application designed to keep the AI Wildlife Ranger server active by periodically sending ping requests to its endpoint. It also provides a `/ping` endpoint to confirm the worker's status.

## Features

- Periodically sends requests to a specified endpoint to keep it alive.
- Logs all activities (successes and failures) to a log file (`keep_alive_log.txt`).
- Provides a `/ping` endpoint to check the worker's status.

## Requirements

The application requires the following Python packages:
- `flask`
- `requests`

Install the dependencies using:
```bash
pip install -r requirements.txt
```

## File Structure

- `keep_alive_worker.py`: Main script containing the Flask app and the keep-alive logic.
- `requirements.txt`: List of required Python packages.
- `keep_alive_log.txt`: Log file where all activities are recorded.

## How to Run

### Locally

1. **Start the Application**:
   Run the following command to start the application:
   ```bash
   python3 keep_alive_worker.py
   ```

2. **Access the Flask App**:
   - The Flask app will run on `http://127.0.0.1:5001`.
   - Use a browser or a tool like `curl` to access the `/ping` endpoint:
     ```bash
     curl http://127.0.0.1:5001/ping
     ```

3. **Logs**:
   - All logs are written to `keep_alive_log.txt`.
   - You can monitor the log file to see the status of the pings.

### Deployment

When deploying on a platform like Render:
- The `ping_app` function runs as a separate process to send periodic pings.
- The Flask app will be served on the specified port (default: `5001`).
- The `ping_app` process is initialized outside the `if __name__ == "__main__":` block, ensuring it runs even when the script is imported by a WSGI server.

## Debugging

- If you do not see any logs or pings:
  - Check the `keep_alive_log.txt` file for errors.
  - Ensure the target endpoint (`APP_PING_URL`) is correct and accessible.
  - Verify that the Flask app is running and responding to requests.

## Example Logs

Here is an example of what the `keep_alive_log.txt` file might look like:
```
[2023-10-01 12:00:00] Ping to app.py successful. Response: Keep Alive Worker is active
[2023-10-01 12:00:10] Ping to app.py successful. Response: Keep Alive Worker is active
[2023-10-01 12:00:20] Failed to reach app.py. Network Issue: HTTPConnectionPool(host='127.0.0.1', port=5000): Max retries exceeded
```

## Notes

- The `ping_app` function runs in a separate process using the `multiprocessing` module.
- The Flask app and the `ping_app` process are decoupled to ensure smooth operation in both local and deployed environments.
- The `ping_app` process is started automatically when the script is imported or executed, ensuring it works in production environments.
