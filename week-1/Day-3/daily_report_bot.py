import pyautogui
import pyperclip
import time
import os
import re
from datetime import datetime

# ============================================================
# DAILY REPORT BOT
# PyAutoGUI + Chrome + Microsoft Excel
# ============================================================

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

SAVE_FOLDER = r"C:\Users\kesav\OneDrive\Documents\Program_AI\week-1\Day-3"

WEATHER_URL = (
    "https://weather.com/en-IN/in/tamil-nadu/city/chennai/tenday"
)

os.makedirs(SAVE_FOLDER, exist_ok=True)

# Generate date and time automatically at runtime
now = datetime.now()
report_date = now.strftime("%Y-%m-%d")
report_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

excel_file = os.path.join(
    SAVE_FOLDER,
    f"daily_report_{report_date}.xlsx"
)

screenshot_file = os.path.join(
    SAVE_FOLDER,
    f"daily_report_{report_date}.png"
)

print("=" * 60)
print("             DAILY REPORT BOT")
print("=" * 60)
print(f"Run date/time : {report_datetime}")
print(f"Excel file    : {excel_file}")
print(f"Screenshot    : {screenshot_file}")
print("=" * 60)


# ============================================================
# 1. OPEN CHROME
# ============================================================

print("\n[1/8] Opening Chrome...")

pyautogui.hotkey("win", "r")
time.sleep(1)
pyautogui.write("chrome")
pyautogui.press("enter")
time.sleep(5)

# Maximize Chrome
pyautogui.hotkey("win", "up")
time.sleep(2)


# ============================================================
# 2. OPEN CHENNAI WEATHER
# ============================================================

print("[2/8] Opening Chennai Weather...")

pyautogui.hotkey("ctrl", "l")
pyautogui.write(WEATHER_URL)
pyautogui.press("enter")

time.sleep(10)

print("      Weather page loaded.")


# ============================================================
# 3. COPY WEBPAGE TEXT
# ============================================================

print("[3/8] Copying webpage text...")

pyautogui.press("esc")
time.sleep(1)

pyautogui.hotkey("ctrl", "a")
time.sleep(1)

pyautogui.hotkey("ctrl", "c")
time.sleep(3)

page_text = pyperclip.paste()

if not page_text.strip():
    raise RuntimeError("No webpage text was copied from Chrome.")

print(f"      Copied approximately {len(page_text):,} characters.")


# ============================================================
# 4. EXTRACT IMPORTANT WEATHER DATA
# ============================================================

print("[4/8] Extracting important weather information...")

# Weather.com may show temperatures in forms such as:
# 81°
# 81 °F
# 29°
# 29 °C
#
# Search for a temperature first.
temperature_patterns = [
    r"(?<!\d)(\d{1,3})\s*°\s*([CF])\b",
    r"(?<!\d)(\d{1,3})\s*°(?!\d)",
]

fetched_data = None

for pattern in temperature_patterns:
    matches = re.findall(
        pattern,
        page_text,
        flags=re.IGNORECASE
    )

    if matches:
        first_match = matches[0]

        if isinstance(first_match, tuple):
            value = first_match[0]
            unit = first_match[1]

            # Normalize to Fahrenheit/Celsius notation.
            fetched_data = f"{value}°{unit.upper()}"
        else:
            fetched_data = first_match.strip()

        break

# If no temperature was detected, look for a temperature followed
# by a weather description in nearby text.
if not fetched_data:
    nearby_pattern = (
        r"(?<!\d)(\d{1,3})\s*°\s*"
        r"(?:\n|\s){0,20}"
        r"(Sunny|Mostly Sunny|Partly Cloudy|Cloudy|Rain|Showers|"
        r"Mostly Cloudy|Clear)"
    )

    match = re.search(
        nearby_pattern,
        page_text,
        flags=re.IGNORECASE
    )

    if match:
        fetched_data = f"{match.group(1)}° - {match.group(2)}"

# Last fallback: use the first useful non-empty weather line,
# but do not use a weekday/date as the report value.
if not fetched_data:
    lines = [
        line.strip()
        for line in page_text.splitlines()
        if line.strip()
    ]

    for line in lines:
        if not re.fullmatch(
            r"(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+\d{1,2}",
            line,
            flags=re.IGNORECASE
        ):
            if len(line) <= 100:
                fetched_data = line
                break

if not fetched_data:
    fetched_data = "Weather information unavailable"

print(f"      Fetched data: {fetched_data}")


# ============================================================
# 5. CREATE SHORT COMMENT
# ============================================================

print("[5/8] Creating comment...")

comment = "Check current conditions before outdoor activities."

print(f"      Comment: {comment}")


# ============================================================
# 6. OPEN MICROSOFT EXCEL
# ============================================================

print("[6/8] Opening Microsoft Excel...")

pyautogui.hotkey("win", "r")
time.sleep(1)

pyautogui.write("excel")
pyautogui.press("enter")

time.sleep(8)

# Maximize Excel reliably using the window system menu.
pyautogui.hotkey("alt", "space")
time.sleep(1)
pyautogui.press("x")
time.sleep(3)


# ============================================================
# 7. CREATE REPORT
# ============================================================

print("[7/8] Creating Excel report...")

pyautogui.hotkey("ctrl", "n")
time.sleep(3)

# Headers
pyautogui.write(
    "Date & Time\tFetched Data\tComment",
    interval=0.01
)
pyautogui.press("enter")

# Data row
pyautogui.write(
    f"{report_datetime}\t{fetched_data}\t{comment}",
    interval=0.01
)

time.sleep(2)

# Make columns easier to read.
# Select the used range and autofit columns.
pyautogui.hotkey("ctrl", "a")
time.sleep(1)
pyautogui.hotkey("alt", "h")
time.sleep(1)
pyautogui.press("o")
time.sleep(1)
pyautogui.press("i")
time.sleep(2)


# ============================================================
# 8. SAVE EXCEL + CLEAN SCREENSHOT
# ============================================================

print("[8/8] Saving Excel report...")

filename_only = f"daily_report_{report_date}.xlsx"

pyautogui.hotkey("ctrl", "s")
time.sleep(3)

# Go to the required folder in the Save dialog.
pyautogui.hotkey("ctrl", "l")
time.sleep(1)

pyautogui.write(
    SAVE_FOLDER,
    interval=0.005
)
pyautogui.press("enter")
time.sleep(3)

# Enter only the filename.
pyautogui.hotkey("ctrl", "a")
pyautogui.write(
    filename_only,
    interval=0.005
)
pyautogui.press("enter")
time.sleep(5)

# If an overwrite confirmation appears, confirm it.
pyautogui.press("left")
pyautogui.press("enter")
time.sleep(3)

# Make sure Excel is maximized before the final screenshot.
pyautogui.hotkey("alt", "space")
time.sleep(1)
pyautogui.press("x")
time.sleep(3)

# Clean screenshot of the Excel window.
pyautogui.screenshot(screenshot_file)

print(f"      Screenshot saved: {screenshot_file}")


# ============================================================
# VERIFY OUTPUTS
# ============================================================

print("\n" + "=" * 60)
print("                    COMPLETED")
print("=" * 60)

excel_exists = os.path.exists(excel_file)
screenshot_exists = os.path.exists(screenshot_file)

print(f"Excel file exists     : {'YES' if excel_exists else 'NO'}")
print(f"Screenshot exists     : {'YES' if screenshot_exists else 'NO'}")

print("\nReport contents:")
print(f"Date & Time : {report_datetime}")
print(f"Data        : {fetched_data}")
print(f"Comment     : {comment}")

if excel_exists and screenshot_exists:
    print("\n✓ Assignment output files created successfully.")
else:
    print("\n⚠ One or more output files could not be verified.")

print("=" * 60)
print("Daily report bot finished.")
print("=" * 60)
