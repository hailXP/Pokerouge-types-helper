import platform
import pygetwindow as gw
import pyautogui

def screenshot_window_by_name(window_name, output_filename="screenshot.png"):
    """
    Searches for a window by its name and takes a screenshot of it.

    Args:
        window_name (str): The name (or part of the name) of the window to find.
        output_filename (str): The name of the file to save the screenshot to.
    """
    system = platform.system()

    if system == "Windows":
        try:

            window = None
            for win in gw.getWindowsWithTitle(window_name):
                if window_name.lower() in win.title.lower():
                    window = win
                    break

            if window:
                print(f"Window found: {window.title}")
                left, top, width, height = window.left, window.top, window.width, window.height

                screenshot = pyautogui.screenshot(region=(left, top, width, height))
                screenshot.save(output_filename)
                print(f"Screenshot saved to {output_filename}")
            else:
                print(f"Window with name containing '{window_name}' not found.")

        except ImportError:
            print("Please install the required libraries: pip install pygetwindow pyautogui")

    else:
        print(f"Screenshotting windows by name is not yet supported on {system}.")

if __name__ == "__main__":
    window_to_find = "pokérogue"
    screenshot_window_by_name(window_to_find)