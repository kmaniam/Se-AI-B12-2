def calculate_grade(marks):
    """Calculates letter grade based on marks percentage."""
    if marks >= 90:
        return 'A+'
    elif marks >= 80:
        return 'A'
    elif marks >= 70:
        return 'B'
    elif marks >= 60:
        return 'C'
    elif marks >= 50:
        return 'D'
    else:
        return 'F'

def get_valid_marks():
    """Prompts for valid marks between 0 and 100 with error handling."""
    while True:
        try:
            marks = float(input("   Enter total marks (0 - 100): "))
            if 0 <= marks <= 100:
                return marks
            else:
                print("   ❌ Error: Marks must be between 0 and 100. Try again.")
        except ValueError:
            print("   ❌ Error: Invalid input! Please enter a numeric value.")

def main():
    print("=" * 45)
    print("         STUDENT GRADE MANAGER")
    print("=" * 45)

    students = []

    # Get number of students with exception handling
    while True:
        try:
            num_students = int(input("Enter the number of students to evaluate: "))
            if num_students > 0:
                break
            else:
                print("Please enter a positive integer greater than 0.")
        except ValueError:
            print("Invalid input! Please enter a whole number.")

    print("\n--- Student Details Collection ---")
    for i in range(1, num_students + 1):
        print(f"\nStudent #{i}:")
        name = input("   Enter student name: ").strip()
        while not name:
            name = input("   Name cannot be blank. Enter student name: ").strip()

        marks = get_valid_marks()
        grade = calculate_grade(marks)

        students.append({
            "name": name,
            "marks": marks,
            "grade": grade
        })

    # Display Results
    print("\n" + "=" * 45)
    print("               FINAL RESULTS")
    print("=" * 45)
    print(f"{'Name':<20} | {'Marks':<8} | {'Grade':<5}")
    print("-" * 45)

    total_marks = 0
    for student in students:
        print(f"{student['name']:<20} | {student['marks']:<8.2f} | {student['grade']:<5}")
        total_marks += student['marks']

    class_average = total_marks / num_students
    print("-" * 45)
    print(f"Class Average Marks: {class_average:.2f}")
    print("=" * 45)

if __name__ == "__main__":
    main()