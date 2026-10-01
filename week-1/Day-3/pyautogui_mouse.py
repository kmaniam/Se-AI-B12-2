import pyautogui
import time

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 10.0

print("PyAutoGUI is working!")

print("Mouse position:", pyautogui.position())

pyautogui.moveTo(500, 300, duration=1)

time.sleep(2)

pyautogui.click()

print("Mouse moved and clicked!")
