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

The final objective is to capture the **available selectable text/data from the Chennai Weather webpage**, paste it into Notepad, and save the result automatically in the Day-3 project folder.
