import keyboard
import pyautogui
import easyocr
import numpy as np
import cv2
import json

reader = easyocr.Reader(['en'], gpu=True)

with open('Effective.json', 'r') as f:
    type_damage_relations_map = json.load(f)

print("Press 'q' to capture a screenshot and perform OCR. Press 'esc' to exit.")

with open("Pokemon.json", "r") as f:
    pokemon = json.load(f)

def capture_and_process_screenshot():
    print("Capturing screenshot...")
    screen_width, screen_height = pyautogui.size()
    
    region = [
        0,
        int(0.05 * screen_width),
        int(0.75 * screen_width),
        int(0.65 * screen_height)
    ]
    
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save("xx.png")
    screenshot_np = np.array(screenshot)
    screenshot_np = cv2.GaussianBlur(screenshot_np, (5, 5), 0)
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

def calculate_type_effectiveness(pokemon_types):
    effectiveness = {}

    def add_multiplier(type_name, multiplier):
        old_value = effectiveness.get(type_name, 100)
        new_value = old_value * multiplier
        effectiveness[type_name] = new_value

    for defensive_type in pokemon_types:
        relations = type_damage_relations_map.get(defensive_type, {})

        for atk_type in relations.get("double_damage_from", []):
            add_multiplier(atk_type["name"], 2)

        for atk_type in relations.get("no_damage_from", []):
            add_multiplier(atk_type["name"], 0)

        for atk_type in relations.get("half_damage_from", []):
            add_multiplier(atk_type["name"], 0.5)

    return effectiveness

def on_q_release(_):
    capture_and_process_screenshot()

def on_esc_release(_):
    print("Exiting...")
    keyboard.unhook_all()
    exit()

keyboard.on_release_key('q', on_q_release)
keyboard.on_release_key('esc', on_esc_release)

keyboard.wait()
