
from tabulate import tabulate
import redis

import logging
import sys

# -----------------------------
# Redis Connection Setup
# -----------------------------
try:
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.ping()
    print("Redis connected successfully!")
except redis.ConnectionError:
    print("Redis connection failed!")
    sys.exit()


# -----------------------------
# Logging Setup (Advanced Bonus)
# -----------------------------
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# -----------------------------
# Grade Calculation Function
# -----------------------------
def calculate_grade(total):
    if total >= 95:
        return "O"
    elif total >= 85:
        return "A+"
    elif total >= 75:
        return "A"
    elif total >= 65:
        return "B+"
    elif total >= 55:
        return "B"
    elif total >= 45:
        return "P"
    else:
        return "F"


def add_student():
    try:
        enrol = input("Enter enrolment number: ").strip()
        key = f"student:{enrol}"

        # Check if student already exists
        if r.exists(key):
            print("Student already exists!")
            return

        name = input("Enter student name: ").strip()
        if not name:
            print("Name cannot be empty!")
            return

        # Input marks with validation
        st1 = int(input("Sessional Test-1 (0-10): "))
        mid = int(input("Mid-Term (0-30): "))
        st2 = int(input("Sessional Test-2 (0-10): "))
        end = int(input("End-Sem (0-40): "))

        if not (0 <= st1 <= 10 and 0 <= mid <= 30 and
                0 <= st2 <= 10 and 0 <= end <= 40):
            print("Marks out of range!")
            return

        total = st1 + mid + st2 + end
        grade = calculate_grade(total)

        # Store in Redis Hash
        r.hset(key, mapping={
            "name": name,
            "st1": st1,
            "mid": mid,
            "st2": st2,
            "end": end,
            "total": total,
            "grade": grade
        })

        print("Student added successfully!")

    except ValueError:
        print("Invalid input! Marks must be integers.")
        logging.error("Invalid marks input")


def view_student():
    enrol = input("Enter enrolment number: ").strip()
    key = f"student:{enrol}"

    if not r.exists(key):
        print("Student not found!")
        return

    student = r.hgetall(key)

    print("\n--- Student Details ---")
    print(f"Name: {student.get('name')}")
    print(f"Sessional Test-1: {student.get('st1')}")
    print(f"Mid-Term: {student.get('mid')}")
    print(f"Sessional Test-2: {student.get('st2')}")
    print(f"End-Sem: {student.get('end')}")
    print(f"Total Marks: {student.get('total')}")
    print(f"Grade: {student.get('grade')}")





def update_marks():
    enrol = input("Enter enrolment number: ").strip()
    key = f"student:{enrol}"

    if not r.exists(key):
        print("Student not found!")
        return

    print("\nWhich marks to update?")
    print("1. Sessional Test-1")
    print("2. Mid-Term")
    print("3. Sessional Test-2")
    print("4. End-Sem")

    choice = input("Enter choice: ")

    try:
        new_mark = int(input("Enter new marks: "))

        # Validation based on component
        if choice == "1" and 0 <= new_mark <= 10:
            r.hset(key, "st1", new_mark)
        elif choice == "2" and 0 <= new_mark <= 30:
            r.hset(key, "mid", new_mark)
        elif choice == "3" and 0 <= new_mark <= 10:
            r.hset(key, "st2", new_mark)
        elif choice == "4" and 0 <= new_mark <= 40:
            r.hset(key, "end", new_mark)
        else:
            print("Invalid marks range!")
            return

        # Recalculate total and grade
        student = r.hgetall(key)
        total = (int(student['st1']) +
                 int(student['mid']) +
                 int(student['st2']) +
                 int(student['end']))

        grade = calculate_grade(total)

        r.hset(key, mapping={
            "total": total,
            "grade": grade
        })

        print("Marks updated successfully!")

    except ValueError:
        print("Invalid input! Enter integer marks.")

def delete_student():
    enrol = input("Enter enrolment number: ").strip()
    key = f"student:{enrol}"

    if not r.exists(key):
        print("Student not found!")
        return

    confirm = input("Are you sure you want to delete? (y/n): ").lower()
    if confirm == 'y':
        r.delete(key)
        print("Student deleted successfully!")
    else:
        print("Deletion cancelled.")





def list_students():
    keys = r.keys("student:*")

    if not keys:
        print("No student records found.")
        return

    table = []

    for key in keys:
        enrol = key.split(":")[1]
        data = r.hgetall(key)

        table.append([
            enrol,
            data.get("name"),
            data.get("st1"),
            data.get("mid"),
            data.get("st2"),
            data.get("end"),
            data.get("total"),
            data.get("grade")
        ])

    headers = [
        "Enrolment",
        "Name",
        "ST1",
        "Mid",
        "ST2",
        "End",
        "Total",
        "Grade"
    ]

    print("\n--- Student Records ---")
    print(tabulate(table, headers=headers, tablefmt="grid"))









# -----------------------------
# Main Menu
# -----------------------------
def main_menu():
    while True:
        print("\n===== Student Management System =====")
        print("1. Add Student")
        print("2. View Student")
        print("3. Update Marks")
        print("4. Delete Student")
        print("5. List All Students")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
           add_student()


        elif choice == "2":
             view_student()
        elif choice == "3":
              update_marks()
        elif choice == "4":
              delete_student()
        elif choice == "5":
              list_students()
	 elif choice == "6":
            print("Exiting program...")
            break
        else:
            print("Invalid choice!")

# Run program
if __name__ == "__main__":
    main_menu()
