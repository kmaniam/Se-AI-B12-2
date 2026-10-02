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
WEATHER_URL = "https://weather.com/en-IN/in/tamil-nadu/city/chennai/tenday"

os.makedirs(SAVE_FOLDER, exist_ok=True)

# Runtime date/time - NOT hard-coded
now = datetime.now()
report_date = now.strftime("%Y-%m-%d")
report_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

excel_file = os.path.join(
    SAVE_FOLDER, f"daily_report_{report_date}.xlsx"
)
screenshot_file = os.path.join(
    SAVE_FOLDER, f"daily_report_{report_date}.png"
)

COMMENT = "Check current conditions before outdoor activities."


def open_app(app_name, wait=5):
    """Open a Windows application using the Run dialog."""
    pyautogui.hotkey("win", "r")
    time.sleep(1)
    pyautogui.write(app_name, interval=0.03)
    pyautogui.press("enter")
    time.sleep(wait)


def extract_temperature(text):
    """Find a temperature such as 82°, 82°F, or 28°C."""
    patterns = [
        r"(?<!\d)(\d{1,3})\s*°\s*([CF])\b",
        r"(?<!\d)(\d{1,3})\s*°(?!\d)",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)

        if matches:
            value = matches[0]

            if isinstance(value, tuple):
                return f"{value[0]}°{value[1].upper()}"

            return value.strip()

    return None


print("=" * 60)
print("              DAILY REPORT BOT")
print("=" * 60)
print(f"Runtime date/time : {report_datetime}")
print(f"Excel output      : {excel_file}")
print(f"Screenshot output : {screenshot_file}")
print("=" * 60)


# ============================================================
# 1. OPEN CHROME
# ============================================================

print("\n[1/7] Opening Chrome...")

open_app("chrome", wait=5)

pyautogui.hotkey("win", "up")
time.sleep(2)


# ============================================================
# 2. OPEN CHENNAI WEATHER
# ============================================================

print("[2/7] Opening Chennai Weather...")

pyautogui.hotkey("ctrl", "l")
pyautogui.write(WEATHER_URL, interval=0.01)
pyautogui.press("enter")

time.sleep(10)

pyautogui.press("esc")
time.sleep(1)


# ============================================================
# 3. COPY PAGE AND EXTRACT TEMPERATURE
# ============================================================

print("[3/7] Copying weather information...")

pyautogui.hotkey("ctrl", "a")
time.sleep(1)

pyautogui.hotkey("ctrl", "c")
time.sleep(3)

page_text = pyperclip.paste()

if not page_text.strip():
    raise RuntimeError("Chrome did not provide any copied webpage text.")

fetched_data = extract_temperature(page_text)

if not fetched_data:
    raise RuntimeError(
        "Could not find a temperature in the copied Chennai Weather text."
    )

print(f"      Temperature found: {fetched_data}")


# ============================================================
# 4. OPEN EXCEL
# ============================================================

print("[4/7] Opening Microsoft Excel...")

open_app("excel", wait=8)

# Maximize Excel using the Windows system menu.
pyautogui.hotkey("alt", "space")
time.sleep(1)
pyautogui.press("x")
time.sleep(3)

# New workbook.
pyautogui.hotkey("ctrl", "n")
time.sleep(3)


# ============================================================
# 5. ENTER EXACTLY ONE REPORT ROW
# ============================================================

print("[5/7] Creating Excel report...")

# Use clipboard to enter tab-separated data.
# This avoids typing/tab-navigation problems and places
# each value in the correct cell.
report_text = (
    "Date & Time\tFetched Data\tComment\n"
    f"{report_datetime}\t{fetched_data}\t{COMMENT}"
)

pyperclip.copy(report_text)

pyautogui.hotkey("ctrl", "v")
time.sleep(3)

# Move back to A1 and select the used cells.
pyautogui.hotkey("ctrl", "home")
time.sleep(1)


# ============================================================
# 6. SAVE USING EXCEL'S SAVE AS DIALOG
# ============================================================

print("[6/7] Saving Excel file...")

filename_only = f"daily_report_{report_date}.xlsx"

# Ctrl+Shift+S explicitly opens Save As.
pyautogui.hotkey("ctrl", "shift", "s")
time.sleep(4)

# IMPORTANT:
# Do NOT use Ctrl+L here.
# In the Windows Save As dialog, Ctrl+L can change focus
# and cause the filename to be typed into the wrong control.
#
# Instead use Alt+N to focus the File Name field.
pyautogui.hotkey("alt", "n")
time.sleep(1)

pyautogui.hotkey("ctrl", "a")
pyautogui.write(filename_only, interval=0.03)

# Move to the folder using the address/location field.
# Alt+D focuses the dialog's location/address field.
pyautogui.hotkey("alt", "d")
time.sleep(1)

pyautogui.write(SAVE_FOLDER, interval=0.01)
pyautogui.press("enter")
time.sleep(3)

# Re-focus File Name and enter the filename again.
pyautogui.hotkey("alt", "n")
time.sleep(1)

pyautogui.hotkey("ctrl", "a")
pyautogui.write(filename_only, interval=0.03)

# Save.
pyautogui.press("enter")
time.sleep(5)

# Handle a possible overwrite confirmation.
# If no dialog exists, these keys have no effect on the workbook.
pyautogui.press("left")
pyautogui.press("enter")
time.sleep(3)


# ============================================================
# 7. VERIFY FILE THEN TAKE CLEAN SCREENSHOT
# ============================================================

print("[7/7] Verifying file and taking screenshot...")

if not os.path.exists(excel_file):
    raise RuntimeError(
        "Excel file was not saved automatically.\n"
        f"Expected: {excel_file}"
    )

# Bring Excel to the foreground and maximize.
pyautogui.hotkey("alt", "tab")
time.sleep(2)

pyautogui.hotkey("alt", "space")
time.sleep(1)
pyautogui.press("x")
time.sleep(3)

# Make sure the worksheet is visible.
pyautogui.hotkey("ctrl", "home")
time.sleep(1)

# Save screenshot only AFTER verifying the workbook exists.
pyautogui.screenshot(screenshot_file)

if not os.path.exists(screenshot_file):
    raise RuntimeError(
        f"Screenshot was not saved: {screenshot_file}"
    )


# ============================================================
# FINAL VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("                 SUCCESS")
print("=" * 60)
print(f"Date & Time : {report_datetime}")
print(f"Data        : {fetched_data}")
print(f"Comment     : {COMMENT}")
print()
print(f"Excel file  : {excel_file}")
print(f"Screenshot  : {screenshot_file}")
print()
print("✓ Excel file verified")
print("✓ Screenshot verified")
print("✓ Report completed")
print("=" * 60)
