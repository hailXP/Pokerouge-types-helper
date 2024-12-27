import pygetwindow as gw
import pyautogui
import keyboard
import easyocr
import numpy as np
import cv2
import json
import os
from collections import defaultdict

reader = easyocr.Reader(['en'], gpu=True)

with open('Effective.json', 'r') as f:
    type_damage_relations_map = json.load(f)

with open("Pokemon.json", "r") as f:
    pokemon = json.load(f)

type_colors = {
    "normal": "\033[97m",
    "fire": "\033[91m",
    "water": "\033[94m",
    "grass": "\033[92m",
    "electric": "\033[93m",
    "ice": "\033[96m",
    "fighting": "\033[33m",
    "poison": "\033[95m",
    "ground": "\033[33m",
    "flying": "\033[94m",
    "psychic": "\033[95m",
    "bug": "\033[92m",
    "rock": "\033[37m",
    "ghost": "\033[95m",
    "dragon": "\033[96m",
    "steel": "\033[37m",
    "dark": "\033[33m",
    "fairy": "\033[95m",
    "shadow": "\033[35m",
}
RESET_COLOR = "\033[0m"

print("Press 'q' to Begin...")

def color_text(text, color_code):
    return f"{color_code}{text}{RESET_COLOR}"

def calculate_type_effectiveness(pokemon_types):
    effectiveness = {}

    for defensive_type in pokemon_types:
        relations = type_damage_relations_map.get(defensive_type.lower(), {})

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

def print_pokemon_info(mon_name, mon_types):
    first_type = mon_types[0].lower()
    mon_colored = color_text(mon_name.title(), type_colors.get(first_type, ""))
    types_colored = [color_text(t.title(), type_colors.get(t.lower(), "")) for t in mon_types]
    print(f"{mon_colored} ({', '.join(types_colored)})")

    effectiveness = calculate_type_effectiveness(mon_types)
    effectiveness = {
        k: round(v / 100, 2)
        for k, v in sorted(effectiveness.items(), key=lambda item: item[1], reverse=False)
    }
    swapped = defaultdict(list)

    for key, value in effectiveness.items():
        swapped[value].append(key)

    effectiveness = dict(swapped)
    if 1 in effectiveness:
        del effectiveness[1]
    for effective in effectiveness:
        types_effective_colored = [color_text(t.title(), type_colors.get(t.lower(), "")) for t in effectiveness[effective]]

        effectiveness_colors = {
            0: "\033[97m",
            0.25: "\033[91m",
            0.5: "\033[31m",
            2: "\033[32m",
            4: "\033[92m",
        }
        effective_color_code = effectiveness_colors.get(effective, "")
        effective_colored = color_text(f"{int(effective) if str(effective).endswith('.0') else effective}x", effective_color_code)

        print(f"{effective_colored}: {', '.join(types_effective_colored)}")

def capture_and_process_screenshot():
    window_name = "pokérogue"

    window = None
    for win in gw.getWindowsWithTitle(window_name):
        if window_name.lower() in win.title.lower():
            window = win
            break

    if window:
        left, top, width, height = window.left, window.top, window.width, window.height

        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        screenshot_np = np.array(screenshot)
        screenshot_np = cv2.GaussianBlur(screenshot_np, (3, 3), 0)
        results = reader.readtext(screenshot_np)

        words = []
        for (_, text, _) in results:
            if len(text) < 3:
                continue
            words.append(text.replace(' ', '').lower())

        mons = {}
        
        for mon in pokemon:
            for i, word in enumerate(words):
                if mon[:8] in word:
                    mons[mon] = [pokemon[mon], i]
                    break
        
        mons = {mon: mons[mon][0] for mon in sorted(mons, key=lambda x: mons[x][1])}
        mons_list = list(mons.keys())

        if len(mons_list) == 2:
            opponent = [mons_list[0]]
            player = [mons_list[1]]
        
        elif len(mons_list) == 3:
            opponent = [mons_list[0]]
            player = mons_list[1:]
            
        elif len(mons_list) == 4:
            opponent = mons_list[:2]
            player = mons_list[2:]

        else:
            opponent = []
            player = mons_list

        os.system('cls' if os.name == 'nt' else 'clear')
        print("Opponent: ")
        for mon in opponent:
            print()
            print_pokemon_info(mon, mons[mon])

        print()
        print("Player: ")

        for mon in player:
            print()
            print_pokemon_info(mon, mons[mon])

        print()
        print("======================================")
    else:
        print(f"Window '{window_name}' not found.")

def on_q_release(_):
    capture_and_process_screenshot()

keyboard.on_release_key('q', on_q_release)
keyboard.wait()