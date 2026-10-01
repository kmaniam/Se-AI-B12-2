import pyautogui

print("Taking screenshot...")

screenshot = pyautogui.screenshot()

screenshot.save("test_screenshot.png")

print("Screenshot saved successfully!")