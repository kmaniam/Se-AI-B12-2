import streamlit as st
import pandas as pd


def calculate_grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    else:
        return "F"


st.set_page_config(
    page_title="Student Grade Manager",
    page_icon="🎓",
    layout="wide",
)

if "students" not in st.session_state:
    st.session_state.students = []


def reset_app():
    st.session_state.students = []


st.title("🎓 Student Grade Manager")
st.write("Enter student details and marks to calculate grades.")
st.divider()

st.subheader("📝 Student Details")

with st.form("student_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input(
            "Student Name",
            placeholder="Enter student name",
        )

    with col2:
        marks = st.number_input(
            "Marks",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.5,
        )

    submitted = st.form_submit_button(
        "➕ Add Student",
        use_container_width=True,
    )

    if submitted:
        name = name.strip()

        if not name:
            st.error("Student name cannot be blank.")
        else:
            grade = calculate_grade(marks)

            st.session_state.students.append(
                {
                    "Name": name,
                    "Marks": marks,
                    "Grade": grade,
                }
            )

            st.success(f"{name} added successfully!")


if st.session_state.students:
    st.divider()
    st.subheader("📊 Student Results")

    df = pd.DataFrame(st.session_state.students)

    display_df = df.copy()
    display_df["Marks"] = display_df["Marks"].map(lambda x: f"{x:.2f}")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

    numeric_marks = [
        student["Marks"] for student in st.session_state.students
    ]

    class_average = sum(numeric_marks) / len(numeric_marks)
    highest_mark = max(numeric_marks)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Students", len(st.session_state.students))

    with col2:
        st.metric("Class Average", f"{class_average:.2f}")

    with col3:
        st.metric("Highest Mark", f"{highest_mark:.2f}")

    st.subheader("📋 Grade Scale")

    grade_data = {
        "Marks": [
            "90 - 100",
            "80 - 89",
            "70 - 79",
            "60 - 69",
            "50 - 59",
            "Below 50",
        ],
        "Grade": ["A+", "A", "B", "C", "D", "F"],
    }

    st.table(pd.DataFrame(grade_data))

    st.button(
        "🔄 Reset All Students",
        on_click=reset_app,
    )
else:
    st.info("No students added yet. Enter a student name and marks above.")

st.divider()
st.caption("Student Grade Manager | Built with Streamlit")
