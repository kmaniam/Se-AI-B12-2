
import csv
import re
from pathlib import Path
from datetime import datetime
import logging

LOG_FILE = Path(__file__).resolve().parent / "student_etl.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)

# --------------------------------------------------
# STEP 1: EXTRACT - Locate the input file
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "students_dirty.csv"
OUTPUT_FILE = BASE_DIR / "students_cleaned.csv"

print("Starting Student ETL Automation")
logger.info("ETL process started")

try:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    print(f"Input file: {INPUT_FILE}")

# --------------------------------------------------
# STEP 2: READ - Read all CSV records
# --------------------------------------------------

    with open(INPUT_FILE, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("CSV file has no header row.")

        # Normalize headers to make matching consistent
        reader.fieldnames = [
            name.strip().lower() for name in reader.fieldnames
        ]

        students = list(reader)

        print(f"Total records loaded: {len(students)}")
        logger.info("Loaded %d student records", len(students))

    # --------------------------------------------------
    # STEP 3: TRANSFORM - Clean the student data
    # --------------------------------------------------


    ALLOWED_COURSES = {
        "python automation": "Python Automation",
        "data science": "Data Science",
        "generative ai": "Generative AI",
        "full stack": "Full Stack"
    }



    def get_value(row, *possible_names):
        """Read a value using any matching column name."""
        for name in possible_names:
            value = row.get(name.lower())
            if value is not None:
                return str(value).strip()
        return ""


    def title_case(value):
        return value.strip().title() if value.strip() else "Unknown"


    def clean_email(value):
        value = value.strip().lower()

        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if re.fullmatch(pattern, value):
            return value

        return "INVALID_EMAIL"


    def clean_phone(value):
        digits = re.sub(r"\D", "", value)

        if len(digits) < 10:
            return "MISSING"

        return digits


    def clean_course(value):
        key = value.strip().lower()
        return ALLOWED_COURSES.get(key, "INVALID_COURSE")


    def clean_fee(value):
        if value is None or not value.strip():
            return False

        try:
            amount = float(value.strip().replace(",", ""))
            return amount > 0
        except ValueError:
            return False


    def clean_date(value):
        value = value.strip()

        if not value:
            return ""

        formats = [
            "%Y-%m-%d",
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%m-%d-%Y",
            "%d-%m-%Y"
        ]

        for fmt in formats:
            try:
                return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue

        return ""


    cleaned_students = []

    for row in students:
        cleaned_row = {
            "Student_id": get_value(
                row, "student_id", "student id"
            ),
            "name": title_case(
                get_value(row, "name")
            ),
            "email": clean_email(
                get_value(row, "email")
            ),
            "phone": clean_phone(
                get_value(row, "phone")
            ),
            "course": clean_course(
                get_value(row, "course")
            ),
            "fee_paid": clean_fee(
                get_value(row, "fee_paid", "fee paid")
            ),
            "city": title_case(
                get_value(row, "city")
            ),
            "enrolled_date": clean_date(
                get_value(
                    row, "enrolled_date", "enrolled_date"
                )
            )
        }

        cleaned_students.append(cleaned_row)

    print("Data cleaning completed.")
    logger.info("Data cleaning completed")

    # --------------------------------------------------
    # STEP 4: LOAD - Write the final cleaned CSV
    # --------------------------------------------------

    fieldnames = [
        "Student_id",
        "name",
        "email",
        "phone",
        "course",
        "fee_paid",
        "city",
        "enrolled_date"
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_students)

    print(f"Total records cleaned: {len(cleaned_students)}")
    print(f"Output saved to: {OUTPUT_FILE}")
    logger.info("Cleaned CSV created: %s", OUTPUT_FILE)
    print("ETL Automation completed successfully!")
    logger.info("ETL process completed successfully")



    # --------------------------------------------------
    # STEP 5: DATA QUALITY REPORT
    # --------------------------------------------------

    total_records = len(cleaned_students)

    invalid_emails = sum(
        row["email"] == "INVALID_EMAIL"
        for row in cleaned_students
    )

    missing_phones = sum(
        row["phone"] == "MISSING"
        for row in cleaned_students
    )

    invalid_courses = sum(
        row["course"] == "INVALID_COURSE"
        for row in cleaned_students
    )

    missing_dates = sum(
        not row["enrolled_date"]
        for row in cleaned_students
    )

    missing_ids = sum(
        not row["Student_id"]
        for row in cleaned_students
    )

    report = f"""
    STUDENT ETL - DATA QUALITY REPORT
    =================================

    Total Records Processed : {total_records}

    DATA QUALITY ISSUES
    -------------------
    Invalid Emails          : {invalid_emails}
    Missing Phone Numbers   : {missing_phones}
    Invalid Courses         : {invalid_courses}
    Missing/Invalid Dates   : {missing_dates}
    Missing Student IDs     : {missing_ids}

    Report Generated Successfully.
    """

    REPORT_FILE = BASE_DIR / "data_quality_report.txt"

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        file.write(report)

    print(report)
    print(f"Quality report saved to: {REPORT_FILE}")

except FileNotFoundError:
    logger.exception("File not found or inaccessible")
    print("ERROR: File not found. Check the path.")
    raise

except csv.Error:
    logger.exception("CSV processing failed")
    print("ERROR: CSV processing failed. Check the log.")
    raise

except Exception:
    logger.exception("Unexpected ETL error")
    print("ERROR: ETL failed. Check student_etl.log.")
    raise