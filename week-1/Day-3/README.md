# Day 3 - PyAutoGUI Automation Practice

## Overview

Today I worked on **Python PyAutoGUI automation** using Windows, Chrome, Notepad, screenshots, and clipboard handling.

The main goal was to build a practical automation flow:

**Open Chrome → Open Chennai Weather → Copy webpage data → Open Notepad → Paste data → Save the file → Capture screenshots**

---

## Project Location

```text
C:\Users\kesav\OneDrive\Documents\Program_AI\week-1\Day-3
```

---

## Environment

- Operating System: Windows
- Editor: VS Code
- Python: Virtual Environment (`venv`)
- Main library: `pyautogui`
- Clipboard library: `pyperclip`
- Browser: Google Chrome
- Text editor: Windows Notepad

---

## 1. PyAutoGUI Configuration

I learned how to configure PyAutoGUI using:

```python
import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5
```

### `FAILSAFE`

When enabled, moving the mouse to the top-left corner can stop the automation.

### `PAUSE`

Adds a small delay between PyAutoGUI actions, making the automation easier to observe and more reliable.

---

## 2. Keyboard Automation

I practiced keyboard automation using:

```python
pyautogui.write("text")
pyautogui.press("enter")
pyautogui.hotkey("ctrl", "c")
pyautogui.hotkey("ctrl", "v")
```

I also worked with:

- `press()`
- `write()`
- `hotkey()`
- `keyDown()`
- `keyUp()`

These are useful for automating normal keyboard operations.

---

## 3. Opening Applications

I used the Windows Run dialog to launch applications.

Example:

```python
pyautogui.hotkey("win", "r")
time.sleep(1)

pyautogui.write("chrome")
pyautogui.press("enter")
```

The same approach was used to open Notepad:

```python
pyautogui.hotkey("win", "r")
pyautogui.write("notepad")
pyautogui.press("enter")
```

---

## 4. Chrome Automation

The automation opens Chrome and navigates to the Chennai Weather 10-Day page:

```text
https://weather.com/en-IN/in/tamil-nadu/city/chennai/tenday
```

The browser navigation is performed using:

```python
pyautogui.hotkey("ctrl", "l")
pyautogui.write(
    "https://weather.com/en-IN/in/tamil-nadu/city/chennai/tenday"
)
pyautogui.press("enter")
```

The script waits for the page to load before continuing.

---

## 5. Taking Screenshots

I learned how to take screenshots using:

```python
pyautogui.screenshot("filename.png")
```

The final automation saves two screenshots:

```text
01_chennai_weather.png
02_final_result.png
```

These screenshots are saved in the Day-3 project folder.

---

## 6. Clipboard Automation with Pyperclip

I installed and used `pyperclip` to work with clipboard data.

Installation:

```bash
python -m pip install pyperclip
```

Import:

```python
import pyperclip
```

Copy clipboard content into Python:

```python
page_text = pyperclip.paste()
```

Copy Python text to the clipboard:

```python
pyperclip.copy(page_text)
```

---

## 7. Copying Webpage Data

The first approach attempted to identify a specific weather date such as:

```text
Fri 02
```

using regular expressions.

The script successfully found:

```text
Date found: Fri 02
```

However, the requirement changed.

Instead of extracting only one date, the goal became:

> Copy all available text/data exposed by the webpage and paste it into Notepad.

Therefore, the date extraction/regex logic was removed.

The final approach uses:

```python
pyautogui.hotkey("ctrl", "a")
pyautogui.hotkey("ctrl", "c")

page_text = pyperclip.paste()
```

This captures the selectable webpage text into Python.

---

## 8. Pasting Data into Notepad

After copying the webpage text, Notepad is opened and the clipboard content is pasted:

```python
pyautogui.hotkey("ctrl", "v")
```

The data is then saved to:

```text
C:\Users\kesav\OneDrive\Documents\Program_AI\week-1\Day-3\chennai_weather_data.txt
```

---

## 9. Saving the File Automatically

The script uses:

```python
pyautogui.hotkey("ctrl", "s")
```

and enters the complete file path:

```python
pyautogui.write(
    text_file,
    interval=0.01
)
```

This avoids depending on whatever folder Notepad happens to open by default.

---

## 10. Why Fixed Mouse Coordinates Were Avoided

Initially, mouse coordinates were considered for selecting a specific weather date.

For example, clicking a fixed position on the page.

However, this was not reliable because:

- The monitor is 49 inches.
- Browser window size and position can change.
- Website layouts can change.
- Weather.com content is dynamically rendered.
- The position of a forecast row can change.

Therefore, the final approach uses keyboard shortcuts and clipboard operations instead of relying on fixed screen coordinates.

This makes the automation more portable and reliable.

---

## 11. Troubleshooting Completed

### Problem 1 - `pyperclip` was not defined

Error:

```text
NameError: name 'pyperclip' is not defined
```

Solution:

```python
import pyperclip
```

and install it if necessary:

```bash
python -m pip install pyperclip
```

---

### Problem 2 - Date extraction returned the wrong information

The initial regex approach selected a date such as:

```text
Fri 02
```

This worked when the objective was to extract one forecast date.

However, the final requirement was to copy **all webpage text**, so the regex extraction was removed.

---

### Problem 3 - Fixed coordinates were unreliable

Selecting a weather row using fixed X/Y coordinates did not work consistently.

The solution was to avoid coordinate-based selection and use:

```text
Ctrl+A → Ctrl+C → Clipboard → Notepad
```

---

## 12. Final Automation Flow

The final workflow is:

```text
Start
  |
  v
Open Chrome
  |
  v
Open Chennai Weather 10-Day page
  |
  v
Wait for page to load
  |
  v
Take weather screenshot
  |
  v
Ctrl+A
  |
  v
Ctrl+C
  |
  v
Read clipboard with pyperclip
  |
  v
Open Notepad
  |
  v
Paste all copied webpage text
  |
  v
Save as chennai_weather_data.txt
  |
  v
Take final screenshot
  |
  v
Verify saved files
  |
  v
End
```

---

## 13. Expected Output Files

After running the final script, the Day-3 folder should contain:

```text
Day-3
│
├── final_demo_pyautogui.py
├── chennai_weather_data.txt
├── 01_chennai_weather.png
└── 02_final_result.png
```

---

## 14. Useful PyAutoGUI Commands Learned Today

| Command | Purpose |
|---|---|
| `pyautogui.write()` | Type text |
| `pyautogui.press()` | Press a keyboard key |
| `pyautogui.hotkey()` | Press keyboard combinations |
| `pyautogui.keyDown()` | Hold a key |
| `pyautogui.keyUp()` | Release a key |
| `pyautogui.click()` | Mouse click |
| `pyautogui.doubleClick()` | Double click |
| `pyautogui.screenshot()` | Capture screen |
| `pyautogui.FAILSAFE` | Emergency stop behavior |
| `pyautogui.PAUSE` | Delay between actions |

---

## 15. Python Modules Used

```python
import pyautogui
import pyperclip
import time
import os
```

### Purpose

- `pyautogui` - GUI automation
- `pyperclip` - Clipboard read/write
- `time` - Delays/waiting
- `os` - File and folder handling

---

## 16. Key Learning from Today

Today's main learning was that GUI automation should not always depend on screen coordinates.

A better automation strategy is often:

```text
Keyboard shortcuts
       +
Clipboard
       +
Python processing
       +
File handling
```

This is particularly useful when working with applications or websites whose screen layout can change.

---

## Final Result

The Day-3 PyAutoGUI exercise successfully automated a real-world workflow involving:

- Windows
- Chrome
- Weather.com
- Clipboard
- Notepad
- File saving
- Screenshots
- Python automation

# Day 3 – Python Automation

## Overview

Day 3 focused on browser automation, GUI automation, web data extraction, Excel automation, and Playwright-based web testing.

---

## 1. PyAutoGUI – Weather to Excel Automation

### Objective

Automate the following workflow using Python and PyAutoGUI:

1. Open Google Chrome.
2. Navigate to the Chennai Weather page.
3. Copy information from the webpage.
4. Extract useful weather information.
5. Open Microsoft Excel.
6. Create a report containing:
   - Date & Time
   - Fetched Data
   - Comment
7. Save the Excel file with the current date.
8. Take a screenshot of the final Excel sheet.
9. Verify that the generated files exist.

### Technologies Used

- Python
- PyAutoGUI
- Pyperclip
- Microsoft Excel
- Google Chrome
- Regular Expressions (`re`)
- Python `datetime`
- OS/file handling

### Weather URL

https://weather.com/en-IN/in/tamil-nadu/city/chennai/tenday

### Python File

`daily_report_bot.py`

### Output Files

The script generates files using the current date:

```text
daily_report_YYYY-MM-DD.xlsx
daily_report_YYYY-MM-DD.png

Important Features
- Date and time are generated automatically at runtime.
- No hard-coded report date.
- Weather information is extracted from copied webpage text.
- Temperature patterns are detected using regular expressions.
- Excel data is inserted using clipboard-based tab-separated values.
- Excel file existence is verified after saving.
- Screenshot is taken after verifying the Excel file.
- File paths are generated automatically.
Example Excel Structure
Date & Time	Fetched Data	Comment
Runtime generated	Weather information	Check current conditions before outdoor activities.


2. PyAutoGUI Debugging and Improvements
During development, several issues were identified and fixed.
Issue 1 – Missing pyperclip
The script initially produced:
NameError: name 'pyperclip' is not defined

This was fixed by importing:
import pyperclip


Issue 2 – Incorrect Excel Save
The initial automation entered the filename/path into the Excel worksheet instead of correctly saving the workbook.
The Excel Save As workflow was improved by:
- Opening Save As explicitly.
- Focusing the correct File Name field.
- Navigating to the required folder.
- Entering only the filename.
- Verifying that the .xlsx file actually exists.
Issue 3 – Incorrect Data Placement
The Excel automation initially had problems with values being placed in the wrong cells.
This was improved by preparing tab-separated data:
report_text = (    "Date & Time\tFetched Data\tComment\n"    f"{report_datetime}\t{fetched_data}\t{COMMENT}")


Then the complete data was pasted into Excel using the clipboard.
Issue 4 – Large Monitor / Screen Coordinates
Fixed screen coordinates were avoided as much as possible because the automation is running on a large monitor.
The script uses keyboard shortcuts such as:
Win + R
Ctrl + L
Ctrl + N
Ctrl + Shift + S
Alt + N
Alt + D
Ctrl + Home

This makes the automation more reliable than depending heavily on fixed mouse coordinates.
3. Playwright – Cricbuzz Score Automation
Objective
Create a Playwright automation that:
1. Opens Cricbuzz.
2. Finds the cricket score from the page.
3. Prints the score in the terminal.
4. Saves a screenshot as score.png.
5. Runs first in headed mode.
6. Runs again in headless mode.
7. Confirms the result.
Website
https://www.cricbuzz.com/cricket-match/live-scores
Python File
cricbuzz_score.py
Technology Used
- Python
- Playwright
- Chromium / Chrome
- Regular Expressions
4. Playwright Score Detection
Instead of assuming a specific CSS selector, the page was inspected to identify score-like elements.
The automation searches for common cricket score formats such as:
123/4
21-2
173 & 358

The regular expression used was:
r"\b\d{1,3}\s*(?:/|-|&)\s*\d{1,3}\b"


The script waits for the page body to become visible before inspecting the DOM.
Example:
page.locator("body").wait_for(    state="visible",    timeout=30000)


This avoids relying on a fixed sleep for score detection.
5. Headed and Headless Testing
Headed Mode
The first test was executed with the browser visible.
Purpose:
- Watch the browser open.
- Confirm Cricbuzz loads.
- Inspect the page.
- Find the score.
- Save the screenshot.
Screenshot:
score.png

Headless Mode
After the headed test worked, the same automation was executed without displaying the browser.
This verified the automation in headless mode.
6. Cricbuzz / Akamai Issue
During testing, headless mode initially returned an Akamai error page:
https://errors.edgesuite.net/

Because the returned page was not the Cricbuzz score page, the score selector could not find a score.
The script was improved to detect this situation instead of incorrectly reporting that a score was found.
The final version also uses Chrome when launching Playwright:
browser = playwright.chromium.launch(    channel="chrome",    headless=headless)


This improved the reliability of the browser automation.
7. Final Day-3 Deliverables
The main files created/worked on during Day 3 are:
Day-3/
│
├── daily_report_bot.py
├── cricbuzz_score.py
├── daily_report_YYYY-MM-DD.xlsx
├── daily_report_YYYY-MM-DD.png
└── score.png

8. Skills Learned
By completing Day 3, I practiced:
- Python GUI automation
- PyAutoGUI
- Clipboard automation
- Chrome automation
- Excel automation
- Webpage text extraction
- Regular expressions
- Runtime date/time generation
- File handling and validation
- Playwright Sync API
- DOM inspection
- Dynamic element detection
- Headed browser automation
- Headless browser automation
- Browser troubleshooting
- Handling website/Akamai blocking
- Creating screenshots as automation evidence
- Debugging Python automation scripts
Day-3 Status
Completed successfully
- [x] PyAutoGUI weather automation
- [x] Weather data extraction
- [x] Excel report creation
- [x] Excel file saving
- [x] Excel output verification
- [x] Excel screenshot
- [x] Playwright installation/testing
- [x] Cricbuzz score extraction
- [x] Headed browser test
- [x] Headless browser test
- [x] score.png screenshot
- [x] Debugging and error handling

The final objective is to capture the **available selectable text/data from the Chennai Weather webpage**, paste it into Notepad, and save the result automatically in the Day-3 project folder.
