import pyautogui
import time

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1

# Open Run
pyautogui.hotkey("win", "r")

time.sleep(1)

# Open Notepad
pyautogui.write("notepad")
pyautogui.press("enter")

time.sleep(2)

# Type text
pyautogui.write("Hello! This is my first PyAutoGUI keyboard automation.", interval=0.05)

# New line
pyautogui.press("enter")

pyautogui.write("I am learning keyboard automation with Python.", interval=0.05)

# Save
pyautogui.hotkey("ctrl", "s")