from pynput import keyboard

def keyPressed(key):
    print(str(key))
    with open

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=keyPressed) # type: ignore
    listener.start()
    input()