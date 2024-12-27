import keyboard
import pyautogui
import easyocr
import numpy as np
import json

reader = easyocr.Reader(['en'], gpu=True)

print("Press 'q' to capture a screenshot and perform OCR. Press 'esc' to exit.")

with open("Pokemon.json", "r") as f:
    pokemon = json.load(f)

def capture_and_process_screenshot():
    print("Capturing screenshot...")
    screen_width, screen_height = pyautogui.size()
    
    region = [
        int(0.10 * screen_width),
        0,
        int(0.70 * screen_width),
        int(0.65 * screen_height)
    ]
    
    screenshot = pyautogui.screenshot(region=region)
    screenshot_np = np.array(screenshot)
    
    results = reader.readtext(screenshot_np)
    
    words = []
    for (_, text, _) in results:
        if len(text) < 3:
            continue
        words.append(text.replace(' ', '').lower())
    
    mons = {}
    for mon in pokemon:
        for word in words:
            if mon in word:
                mons[mon] = pokemon[mon]
                break
    
    print("Detected Pokémon:", mons)
    print("Press 'q' to capture another screenshot, or 'esc' to exit.")

def on_q_release(_):
    capture_and_process_screenshot()

def on_esc_release(_):
    print("Exiting...")
    keyboard.unhook_all()
    exit()

keyboard.on_release_key('q', on_q_release)
keyboard.on_release_key('esc', on_esc_release)

keyboard.wait()
