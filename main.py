import keyboard
import pyautogui
import easyocr
import numpy as np
import cv2
import json
from collections import defaultdict

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
    
    mons_list = list(mons.keys())
    if len(mons_list) == 4:
        opponent = mons_list[:2]
        player = mons_list[2:]

    elif len(mons_list) == 2:
        opponent = [mons_list[0]]
        player = [mons_list[1]]

    else:
        opponent = mons_list
        player = []

    print("Opponent: ")
    for mon in opponent:
        print()
        print(f"{mon.title()} ({', '.join(mons[mon].title())})")
        effectiveness = calculate_type_effectiveness(mons[mon])
        effectiveness = {
            k: round(v / 100, 2) 
            for k, v in sorted(effectiveness.items(), key=lambda item: item[1], reverse=False)
        }        
        swapped = defaultdict(list)

        for key, value in effectiveness.items():
            swapped[value].append(key)

        effectiveness = dict(swapped)
        for effective in effectiveness:
            print(f"{int(effective) if str(effective).endswith('.0') else effective}x: {', '.join(effectiveness[effective])}")

    print()
    print("Player: ")

    for mon in player:
        print()
        print(f"{mon.title()} ({', '.join(mons[mon].title())})")
        effectiveness = calculate_type_effectiveness(mons[mon])
        effectiveness = {
            k: round(v / 100, 2) 
            for k, v in sorted(effectiveness.items(), key=lambda item: item[1], reverse=False)
        }        
        swapped = defaultdict(list)

        for key, value in effectiveness.items():
            swapped[value].append(key)

        effectiveness = dict(swapped)
        for effective in effectiveness:
            print(f"{int(effective) if str(effective).endswith('.0') else effective}x: {', '.join(effectiveness[effective])}")

    print("Press 'q' to capture another screenshot, or 'esc' to exit.")

def calculate_type_effectiveness(pokemon_types):
    effectiveness = {}

    for defensive_type in pokemon_types:
        relations = type_damage_relations_map.get(defensive_type, {})

        for atk_type in relations.get("double_damage_from", []):
            old_value = effectiveness.get(atk_type, 100)
            new_value = old_value * 2
            effectiveness[atk_type] = new_value

        for atk_type in relations.get("no_damage_from", []):
            old_value = effectiveness.get(atk_type, 100)
            new_value = old_value * 0
            effectiveness[atk_type] = new_value

        for atk_type in relations.get("half_damage_from", []):
            old_value = effectiveness.get(atk_type, 100)
            new_value = old_value * 0.5
            effectiveness[atk_type] = new_value

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
