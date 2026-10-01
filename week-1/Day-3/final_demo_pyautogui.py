import pyautogui
import pyperclip
import time
import os

# =====================================================
# SETTINGS
# =====================================================

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

save_folder = r"C:\Users\kesav\OneDrive\Documents\Program_AI\week-1\Day-3"

text_file = os.path.join(
    save_folder,
    "chennai_weather_data.txt"
)

weather_screenshot = os.path.join(
    save_folder,
    "01_chennai_weather.png"
)

final_screenshot = os.path.join(
    save_folder,
    "02_final_result.png"
)

os.makedirs(save_folder, exist_ok=True)


print("========================================")
print("       PyAutoGUI FINAL DEMO")
print("       Chennai Weather - ALL DATA")
print("========================================")


# =====================================================
# 1. OPEN CHROME
# =====================================================

print("1. Opening Chrome...")

pyautogui.hotkey("win", "r")
time.sleep(1)

pyautogui.hotkey("ctrl", "a")
pyautogui.write("chrome")

pyautogui.press("enter")

time.sleep(5)

pyautogui.hotkey("win", "up")

time.sleep(2)


# =====================================================
# 2. OPEN CHENNAI WEATHER
# =====================================================

print("2. Opening Chennai Weather 10-Day page...")

pyautogui.hotkey("ctrl", "l")

pyautogui.write(
    "https://weather.com/en-IN/in/tamil-nadu/city/chennai/tenday"
)

pyautogui.press("enter")

time.sleep(8)

print("Chennai Weather page loaded.")


# =====================================================
# 3. TAKE SCREENSHOT
# =====================================================

print("3. Taking weather screenshot...")

pyautogui.screenshot(weather_screenshot)

print("Saved:", weather_screenshot)


# =====================================================
# 4. COPY ALL WEBPAGE TEXT
# =====================================================

print("4. Copying ALL webpage text...")

# Make sure page has focus
pyautogui.press("esc")

time.sleep(1)

# Select everything on the webpage
pyautogui.hotkey("ctrl", "a")

time.sleep(1)

# Copy everything
pyautogui.hotkey("ctrl", "c")

time.sleep(3)


# =====================================================
# 5. GET COPIED DATA
# =====================================================

page_text = pyperclip.paste()

print("Webpage data copied successfully.")

print("----------------------------------------")
print("Characters copied:", len(page_text))
print("----------------------------------------")


# =====================================================
# 6. CHECK DATA
# =====================================================

if not page_text.strip():

    print("ERROR: No webpage data was copied.")

    input("Press Enter to exit...")

    raise SystemExit


# =====================================================
# 7. OPEN NOTEPAD
# =====================================================

print("5. Opening Notepad...")

pyautogui.hotkey("win", "r")

time.sleep(1)

pyautogui.hotkey("ctrl", "a")

pyautogui.write("notepad")

pyautogui.press("enter")

time.sleep(3)


# =====================================================
# 8. PASTE ALL DATA
# =====================================================

print("6. Pasting ALL weather data into Notepad...")

pyautogui.hotkey("ctrl", "v")

time.sleep(3)


# =====================================================
# 9. SAVE FILE
# =====================================================

print("7. Saving weather data...")

pyautogui.hotkey("ctrl", "s")

time.sleep(2)

pyautogui.hotkey("ctrl", "a")

pyautogui.write(
    text_file,
    interval=0.01
)

pyautogui.press("enter")

time.sleep(3)


# =====================================================
# 10. FINAL SCREENSHOT
# =====================================================

print("8. Taking final screenshot...")

pyautogui.screenshot(final_screenshot)


# =====================================================
# 11. VERIFY
# =====================================================

print("")
print("========================================")
print("          DEMO COMPLETED")
print("========================================")

print("Characters copied :", len(page_text))

print("Weather data file  :")
print(text_file)

print("")
print("Weather screenshot :")
print(weather_screenshot)

print("")
print("Final screenshot   :")
print(final_screenshot)

print("----------------------------------------")


if os.path.exists(text_file):
    print("✓ ALL weather data saved successfully")
else:
    print("✗ Weather data file was NOT saved")


if os.path.exists(weather_screenshot):
    print("✓ Weather screenshot saved")
else:
    print("✗ Weather screenshot was NOT saved")


if os.path.exists(final_screenshot):
    print("✓ Final screenshot saved")
else:
    print("✗ Final screenshot was NOT saved")


print("========================================")