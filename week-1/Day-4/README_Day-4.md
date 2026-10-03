# Day 4 - API, FastAPI and Streamlit

## Overview

Day 4 focused on APIs, REST API methods, Postman, FastAPI, and Streamlit.

## Activities Completed

### 1. API Basics
- Introduction to APIs
- API requests and responses
- Endpoints
- JSON responses
- API types

### 2. REST API
Practiced common HTTP methods:

- GET - retrieve data
- POST - create data
- PUT - update data
- DELETE - delete data

### 3. Postman
Used Postman to test API endpoints with GET, POST, PUT and DELETE requests.

Example endpoints:
```text
GET    /
GET    /items/10
GET    /items/10?q=apple
POST   /items
PUT    /items/10
DELETE /items/10
```

# FastAPI

## 4. FastAPI Setup

Installed FastAPI and Uvicorn:

```bash
pip install fastapi uvicorn
```

Created and tested a basic FastAPI application.

Example:

```python
from fastapi import FastAPI

main = FastAPI()

@main.get("/")
def read_root():
    return {"Hello": "World"}
```

Run:

```bash
python -m uvicorn firstapi:main --reload
```

Application:

```text
http://127.0.0.1:8000
```

## 5. FastAPI Multiple HTTP Methods

Created GET, POST, PUT and DELETE endpoints and tested them using Postman.

Path parameter example:

```text
PUT http://127.0.0.1:8000/items/10
```

## 6. FastAPI Assignment

Created `main.py` with:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI application"}

@app.get("/greet/{name}")
def greet_user(name: str):
    return {"message": f"Hello, {name}!"}
```

Run:

```bash
python -m uvicorn main:app --reload
```

Tested:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/greet/Kesav
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/openapi.json
```

The automatic FastAPI Swagger documentation was also tested.

# Streamlit

## 7. Streamlit Installation

Installed Streamlit:

```bash
pip install streamlit
```

Verify:

```bash
streamlit --version
```

## 8. Basic Streamlit Application

Example:

```python
import streamlit as st

st.title("My First Streamlit App")
st.write("Hello, welcome to my Streamlit application!")
```

Run:

```bash
streamlit run streamlit_app.py
```

Default URL:

```text
http://localhost:8501
```

## 9. Streamlit Components

Practiced:

- `st.title()`
- `st.write()`
- `st.text_input()`
- `st.number_input()`
- `st.button()`
- `st.columns()`
- `st.metric()`
- `st.success()`
- `st.error()`
- `st.info()`
- `st.dataframe()`
- `st.table()`
- `st.file_uploader()`

## 10. Streamlit Calculator

Built a calculator-style application with:

- Numbers
- 00
- Decimal
- Addition
- Subtraction
- Multiplication
- Division
- AC
- Equals
- Division-by-zero handling
- `st.session_state` for maintaining calculator state

# Student Grade Manager

## 11. Student Grade Manager

Converted the existing Python Student Grade Manager into a Streamlit UI.

### Grade Rules

| Marks | Grade |
|---|---|
| 90 - 100 | A+ |
| 80 - 89 | A |
| 70 - 79 | B |
| 60 - 69 | C |
| 50 - 59 | D |
| Below 50 | F |

### Features

- Student name input
- Marks input from 0 to 100
- Automatic grade calculation
- Multiple student support
- Results table
- Total students
- Class average
- Highest mark
- Grade scale
- Reset option

# Excel Grade Validation

The Student Grade Manager was enhanced with Excel upload support.

### Supported files

```text
.xlsx
.xls
```

Recommended columns:

```text
Name | Marks | Grade
```

Example:

| Name | Marks | Grade |
|---|---:|---|
| John | 95 | A+ |
| Priya | 82 | A |
| Arun | 67 | C |
| Ravi | 45 | F |

### Validation Process

The application:

1. Uploads the Excel file.
2. Reads student names and marks.
3. Validates marks between 0 and 100.
4. Calculates the expected grade.
5. Compares the uploaded grade with the calculated grade.
6. Displays correct and incorrect grades.
7. Shows total records, correct grades and incorrect grades.

If no Grade column is present, the application calculates and displays the expected grade.

Install Excel dependencies:

```bash
pip install pandas openpyxl
```

Run:

```bash
streamlit run student_grade_manager_excel.py
```

# Technologies Used

- Python
- FastAPI
- Uvicorn
- REST API
- Postman
- Streamlit
- Pandas
- OpenPyXL
- VS Code
- Git / GitHub

# Key Learning Outcomes

By the end of Day 4, I practiced:

- API fundamentals
- REST API concepts
- HTTP methods
- Postman API testing
- FastAPI application development
- Uvicorn
- FastAPI automatic documentation
- Streamlit application development
- Streamlit components
- `st.session_state`
- Building a calculator UI
- Converting a Python program into a Streamlit UI
- Excel file upload
- Excel data validation
- Student grade calculation and validation

## Day 4 Status

**Completed:** API basics, REST API, Postman, FastAPI, FastAPI assignment, Streamlit basics, Streamlit components, calculator practice, Student Grade Manager, and Excel grade validation.
