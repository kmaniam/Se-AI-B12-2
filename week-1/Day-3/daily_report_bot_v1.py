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

# ------------------------------------------------------------
# 1. PROJECT / FILE SETTINGS
# ------------------------------------------------------------

SAVE_FOLDER = r"C:\Users\kesav\OneDrive\Documents\Program_AI\week-1\Day-3"

WEATHER_URL = (
    "https://weather.com/en-IN/in/tamil-nadu/city/chennai/tenday"
)

os.makedirs(SAVE_FOLDER, exist_ok=True)

# Generate date/time automatically at runtime
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


# ------------------------------------------------------------
# 2. OPEN CHROME
# ------------------------------------------------------------

print("\n[1/8] Opening Chrome...")

pyautogui.hotkey("win", "r")
time.sleep(1)

pyautogui.write("chrome")
pyautogui.press("enter")

time.sleep(5)

# Maximize the window without relying on screen coordinates.
pyautogui.hotkey("win", "up")
time.sleep(2)


# ------------------------------------------------------------
# 3. OPEN CHENNAI WEATHER PAGE
# ------------------------------------------------------------

print("[2/8] Opening Chennai Weather...")

pyautogui.hotkey("ctrl", "l")
pyautogui.write(WEATHER_URL)
pyautogui.press("enter")

# Allow the dynamic webpage to load.
time.sleep(10)

print("      Weather page loaded.")


# ------------------------------------------------------------
# 4. COPY WEBPAGE TEXT
# ------------------------------------------------------------

print("[3/8] Copying webpage text...")

# Escape any active browser element, then select/copy page text.
pyautogui.press("esc")
time.sleep(1)

pyautogui.hotkey("ctrl", "a")
time.sleep(1)

pyautogui.hotkey("ctrl", "c")
time.sleep(3)

page_text = pyperclip.paste()

if not page_text.strip():
    raise RuntimeError(
        "No webpage text was copied from Chrome."
    )

print(
    f"      Copied approximately {len(page_text):,} characters."
)


# ------------------------------------------------------------
# 5. EXTRACT AN IMPORTANT WEATHER VALUE
# ------------------------------------------------------------

print("[4/8] Extracting weather information...")

# Weather.com page text can change over time.
# First try to identify a temperature such as 29° or 29°F/29°C.
temperature_patterns = [
    r"\b\d{1,3}\s*°\s*[CF]\b",
    r"\b\d{1,3}\s*°\b",
]

fetched_data = None

for pattern in temperature_patterns:
    matches = re.findall(
        pattern,
        page_text,
        flags=re.IGNORECASE
    )

    if matches:
        fetched_data = matches[0].strip()
        break

# If no temperature is found, use the first useful forecast
# date/weather text detected from the copied page.
if not fetched_data:
    forecast_pattern = (
        r"\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+\d{1,2}\b"
    )

    matches = re.findall(
        forecast_pattern,
        page_text,
        flags=re.IGNORECASE
    )

    if matches:
        fetched_data = matches[0]

# Final fallback: store a small piece of copied webpage text.
if not fetched_data:
    cleaned_lines = [
        line.strip()
        for line in page_text.splitlines()
        if line.strip()
    ]

    if cleaned_lines:
        fetched_data = cleaned_lines[0]

if not fetched_data:
    fetched_data = "Weather data could not be identified"

print(f"      Fetched data: {fetched_data}")


# ------------------------------------------------------------
# 6. CREATE SHORT COMMENT
# ------------------------------------------------------------

print("[5/8] Creating comment...")

# Keep the comment short and deterministic for the assignment.
comment = "Check current conditions before outdoor activities."

print(f"      Comment: {comment}")


# ------------------------------------------------------------
# 7. OPEN MICROSOFT EXCEL
# ------------------------------------------------------------

print("[6/8] Opening Microsoft Excel...")

pyautogui.hotkey("win", "r")
time.sleep(1)

pyautogui.write("excel")
pyautogui.press("enter")

# Give Excel time to start.
time.sleep(8)

# Maximize Excel.
pyautogui.hotkey("win", "up")
time.sleep(2)


# ------------------------------------------------------------
# 8. CREATE WORKBOOK AND ENTER DATA
# ------------------------------------------------------------

print("[7/8] Creating Excel report...")

# Create a new workbook.
pyautogui.hotkey("ctrl", "n")
time.sleep(3)

# Excel normally opens at A1 in a new workbook.
# Enter headers and the automatically generated row.
headers = "Date & Time\tFetched Data\tComment"
data_row = (
    f"{report_datetime}\t"
    f"{fetched_data}\t"
    f"{comment}"
)

pyautogui.write(headers, interval=0.01)
pyautogui.press("enter")

pyautogui.write(data_row, interval=0.01)

time.sleep(2)


# ------------------------------------------------------------
# 9. SAVE EXCEL FILE
# ------------------------------------------------------------

# ------------------------------------------------------------
# SAVE EXCEL FILE
# ------------------------------------------------------------

print("      Saving Excel workbook...")

pyautogui.hotkey("ctrl", "s")
time.sleep(3)

# Navigate to the required folder first
pyautogui.hotkey("ctrl", "l")
time.sleep(1)

pyautogui.write(
    SAVE_FOLDER,
    interval=0.005
)

pyautogui.press("enter")
time.sleep(3)

# Enter ONLY the filename
filename_only = f"daily_report_{report_date}.xlsx"

pyautogui.hotkey("ctrl", "a")

pyautogui.write(
    filename_only,
    interval=0.005
)

pyautogui.press("enter")

time.sleep(5)


# ------------------------------------------------------------
# 10. SCREENSHOT FINAL EXCEL SHEET
# ------------------------------------------------------------

print("[8/8] Taking screenshot of final Excel sheet...")

time.sleep(2)

pyautogui.screenshot(screenshot_file)

print("      Screenshot saved.")


# ------------------------------------------------------------
# 11. VERIFY OUTPUTS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("                    COMPLETED")
print("=" * 60)

if os.path.exists(excel_file):
    print("✓ Excel file saved successfully")
    print(f"  {excel_file}")
else:
    print("✗ Excel file was not found")

if os.path.exists(screenshot_file):
    print("✓ Final Excel screenshot saved successfully")
    print(f"  {screenshot_file}")
else:
    print("✗ Screenshot was not found")

print("\nReport contents:")
print(f"Date & Time : {report_datetime}")
print(f"Data        : {fetched_data}")
print(f"Comment     : {comment}")

print("=" * 60)
print("Daily report bot finished.")
print("=" * 60)
