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
st.write("Enter student details manually or upload an Excel file to validate grades.")
st.divider()


# =========================================================
# OPTION 1 - MANUAL STUDENT ENTRY
# =========================================================
st.subheader("📝 Add Student Manually")

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


# =========================================================
# OPTION 2 - EXCEL UPLOAD
# =========================================================
st.divider()
st.subheader("📤 Validate Grades from Excel")

st.write(
    "Upload an Excel file containing student names and marks. "
    "The application will calculate the expected grade and validate "
    "the grade in the file if a Grade column is provided."
)

uploaded_file = st.file_uploader(
    "Choose an Excel file",
    type=["xlsx", "xls"],
    help="Recommended columns: Name, Marks, Grade",
)

if uploaded_file is not None:
    try:
        excel_df = pd.read_excel(uploaded_file)

        # Normalize column names for easier matching
        excel_df.columns = [
            str(column).strip().lower()
            for column in excel_df.columns
        ]

        # Accept common alternatives for the name column
        name_column = None
        for column in ["name", "student name", "student_name", "student"]:
            if column in excel_df.columns:
                name_column = column
                break

        # Accept common alternatives for marks
        marks_column = None
        for column in ["marks", "mark", "score", "percentage"]:
            if column in excel_df.columns:
                marks_column = column
                break

        # Accept common alternatives for grade
        grade_column = None
        for column in ["grade", "expected grade", "student grade"]:
            if column in excel_df.columns:
                grade_column = column
                break

        if name_column is None or marks_column is None:
            st.error(
                "Excel file must contain at least these columns: "
                "Name and Marks."
            )
        else:
            excel_df[marks_column] = pd.to_numeric(
                excel_df[marks_column],
                errors="coerce",
            )

            invalid_marks = (
                excel_df[marks_column].isna()
                | (excel_df[marks_column] < 0)
                | (excel_df[marks_column] > 100)
            )

            if invalid_marks.any():
                st.error(
                    "Some rows contain invalid marks. "
                    "Marks must be between 0 and 100."
                )
                st.dataframe(
                    excel_df[invalid_marks],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                # Calculate expected grade using the original grade rules
                excel_df["Calculated Grade"] = excel_df[marks_column].apply(
                    calculate_grade
                )

                if grade_column is not None:
                    excel_df["Uploaded Grade"] = (
                        excel_df[grade_column]
                        .astype(str)
                        .str.strip()
                        .str.upper()
                    )

                    excel_df["Validation"] = excel_df.apply(
                        lambda row: (
                            "✅ Correct"
                            if row["Uploaded Grade"]
                            == row["Calculated Grade"]
                            else "❌ Incorrect"
                        ),
                        axis=1,
                    )

                    correct_count = (
                        excel_df["Validation"] == "✅ Correct"
                    ).sum()
                    incorrect_count = (
                        excel_df["Validation"] == "❌ Incorrect"
                    ).sum()

                    st.success(
                        f"Excel validation completed: "
                        f"{correct_count} correct, "
                        f"{incorrect_count} incorrect."
                    )

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Total Records",
                            len(excel_df),
                        )

                    with col2:
                        st.metric(
                            "Correct Grades",
                            int(correct_count),
                        )

                    with col3:
                        st.metric(
                            "Incorrect Grades",
                            int(incorrect_count),
                        )

                    result_columns = [
                        name_column,
                        marks_column,
                        "Uploaded Grade",
                        "Calculated Grade",
                        "Validation",
                    ]

                    st.dataframe(
                        excel_df[result_columns],
                        use_container_width=True,
                        hide_index=True,
                    )

                else:
                    st.info(
                        "No Grade column was found. "
                        "The application calculated the expected grade "
                        "for each student."
                    )

                    result_columns = [
                        name_column,
                        marks_column,
                        "Calculated Grade",
                    ]

                    st.dataframe(
                        excel_df[result_columns],
                        use_container_width=True,
                        hide_index=True,
                    )

    except Exception as error:
        st.error(f"Unable to read the Excel file: {error}")


# =========================================================
# MANUAL RESULTS
# =========================================================
if st.session_state.students:
    st.divider()
    st.subheader("📊 Manually Added Student Results")

    df = pd.DataFrame(st.session_state.students)

    display_df = df.copy()
    display_df["Marks"] = display_df["Marks"].map(
        lambda x: f"{x:.2f}"
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

    numeric_marks = [
        student["Marks"]
        for student in st.session_state.students
    ]

    class_average = sum(numeric_marks) / len(numeric_marks)
    highest_mark = max(numeric_marks)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Students",
            len(st.session_state.students),
        )

    with col2:
        st.metric(
            "Class Average",
            f"{class_average:.2f}",
        )

    with col3:
        st.metric(
            "Highest Mark",
            f"{highest_mark:.2f}",
        )


# =========================================================
# GRADE SCALE
# =========================================================
st.divider()
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


# =========================================================
# RESET
# =========================================================
if st.session_state.students:
    st.button(
        "🔄 Reset Manual Students",
        on_click=reset_app,
    )

st.divider()
st.caption("Student Grade Manager | Built with Streamlit")
