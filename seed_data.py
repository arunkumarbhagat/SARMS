"""
Run this to populate MongoDB with sample data:
  python seed_data.py
"""
from config import (
    students_collection, teachers_collection, subjects_collection,
    attendance_collection, marks_collection, users_collection
)

# ── TEACHERS ──────────────────────────────────────────────
teachers = [
    {"teacher_id": "TCH001", "name": "Dr. Ramesh Kumar",   "department": "Computer Science"},
    {"teacher_id": "TCH002", "name": "Prof. Sneha Patel",  "department": "Mathematics"},
    {"teacher_id": "TCH003", "name": "Dr. Arjun Mehta",    "department": "Physics"},
]

# ── STUDENTS ──────────────────────────────────────────────
students = [
    {"student_id": "23BAI001", "name": "Arun Sharma",    "department": "Computer Science", "semester": 4},
    {"student_id": "23BAI002", "name": "Priya Nair",     "department": "Computer Science", "semester": 4},
    {"student_id": "23BAI003", "name": "Rahul Verma",    "department": "Mathematics",      "semester": 2},
    {"student_id": "23BAI004", "name": "Anjali Singh",   "department": "Physics",          "semester": 3},
    {"student_id": "23BAI005", "name": "Karan Patel",    "department": "Computer Science", "semester": 4},
]

# ── SUBJECTS ──────────────────────────────────────────────
subjects = [
    {"subject_code": "CS301", "subject_name": "Data Structures",       "semester": 4, "teacher_id": "TCH001"},
    {"subject_code": "CS302", "subject_name": "Operating Systems",     "semester": 4, "teacher_id": "TCH001"},
    {"subject_code": "MA201", "subject_name": "Linear Algebra",        "semester": 2, "teacher_id": "TCH002"},
    {"subject_code": "PH301", "subject_name": "Quantum Mechanics",     "semester": 3, "teacher_id": "TCH003"},
    {"subject_code": "CS303", "subject_name": "Database Management",   "semester": 4, "teacher_id": "TCH001"},
]

# ── ATTENDANCE ────────────────────────────────────────────
attendance = [
    {"student_id": "23BAI001", "subject_code": "CS301", "status": "Present", "date": "2026-03-20"},
    {"student_id": "23BAI001", "subject_code": "CS301", "status": "Present", "date": "2026-03-21"},
    {"student_id": "23BAI001", "subject_code": "CS302", "status": "Absent",  "date": "2026-03-20"},
    {"student_id": "23BAI001", "subject_code": "CS303", "status": "Present", "date": "2026-03-22"},
    {"student_id": "23BAI002", "subject_code": "CS301", "status": "Present", "date": "2026-03-20"},
    {"student_id": "23BAI002", "subject_code": "CS302", "status": "Present", "date": "2026-03-20"},
    {"student_id": "23BAI002", "subject_code": "CS303", "status": "Absent",  "date": "2026-03-22"},
    {"student_id": "23BAI003", "subject_code": "MA201", "status": "Present", "date": "2026-03-20"},
    {"student_id": "23BAI003", "subject_code": "MA201", "status": "Absent",  "date": "2026-03-21"},
    {"student_id": "23BAI004", "subject_code": "PH301", "status": "Present", "date": "2026-03-20"},
    {"student_id": "23BAI005", "subject_code": "CS301", "status": "Present", "date": "2026-03-20"},
    {"student_id": "23BAI005", "subject_code": "CS302", "status": "Present", "date": "2026-03-21"},
]

# ── MARKS ─────────────────────────────────────────────────
marks = [
    {"student_id": "23BAI001", "subject_code": "CS301", "marks": 88},
    {"student_id": "23BAI001", "subject_code": "CS302", "marks": 74},
    {"student_id": "23BAI001", "subject_code": "CS303", "marks": 91},
    {"student_id": "23BAI002", "subject_code": "CS301", "marks": 79},
    {"student_id": "23BAI002", "subject_code": "CS302", "marks": 85},
    {"student_id": "23BAI002", "subject_code": "CS303", "marks": 68},
    {"student_id": "23BAI003", "subject_code": "MA201", "marks": 92},
    {"student_id": "23BAI004", "subject_code": "PH301", "marks": 77},
    {"student_id": "23BAI005", "subject_code": "CS301", "marks": 83},
    {"student_id": "23BAI005", "subject_code": "CS302", "marks": 90},
]

# ── INSERT ────────────────────────────────────────────────
def seed():
    # Clear existing data
    students_collection.delete_many({})
    teachers_collection.delete_many({})
    subjects_collection.delete_many({})
    attendance_collection.delete_many({})
    marks_collection.delete_many({})
    users_collection.delete_many({"role": {"$in": ["student", "teacher"]}})

    students_collection.insert_many(students)
    teachers_collection.insert_many(teachers)
    subjects_collection.insert_many(subjects)
    attendance_collection.insert_many(attendance)
    marks_collection.insert_many(marks)

    # Create login accounts for students (password = student_id)
    for s in students:
        users_collection.update_one(
            {"username": s["student_id"]},
            {"$set": {"username": s["student_id"], "password": s["student_id"], "role": "student", "ref_id": s["student_id"]}},
            upsert=True
        )

    # Create login accounts for teachers (password = teacher_id)
    for t in teachers:
        users_collection.update_one(
            {"username": t["teacher_id"]},
            {"$set": {"username": t["teacher_id"], "password": t["teacher_id"], "role": "teacher", "ref_id": t["teacher_id"]}},
            upsert=True
        )

    print("✅ Sample data inserted!\n")
    print("── Student Logins ──────────────────")
    for s in students:
        print(f"  {s['name']:<20} | user: {s['student_id']}  pass: {s['student_id']}")
    print("\n── Teacher Logins ──────────────────")
    for t in teachers:
        print(f"  {t['name']:<25} | user: {t['teacher_id']}  pass: {t['teacher_id']}")
    print("\n── Admin Login ─────────────────────")
    print("  username: admin  |  password: admin123")

if __name__ == "__main__":
    seed()
