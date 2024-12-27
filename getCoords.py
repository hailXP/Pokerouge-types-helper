import pyautogui
from pynput import keyboard

def on_press(key):
    try:
        if key.char == 'q':
            x, y = pyautogui.position()
            print(f"Mouse position: ({x}, {y})")
        elif key.char == 'w':
            return False
    except AttributeError:
        pass

def main():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    print("Press 'q' to print mouse coordinates. Press 'w' to exit.")
    main()
