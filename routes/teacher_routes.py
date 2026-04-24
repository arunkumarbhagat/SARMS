from flask import Blueprint, request, jsonify, session
from config import attendance_collection, marks_collection, students_collection

teacher_routes = Blueprint("teacher_routes", __name__)

@teacher_routes.route("/teacher/mark_attendance", methods=["POST"])
def mark_attendance():
    data = request.json
    student = students_collection.find_one({"student_id": data["student_id"]})
    if not student:
        return jsonify({"error": "Student not found"}), 400

    attendance_collection.insert_one({
        "student_id": data["student_id"],
        "subject_code": data["subject_code"],
        "status": data["status"],
        "date": data["date"]
    })
    return jsonify({"message": "Attendance recorded"})

@teacher_routes.route("/teacher/enter_marks", methods=["POST"])
def enter_marks():
    data = request.json
    student = students_collection.find_one({"student_id": data["student_id"]})
    if not student:
        return jsonify({"error": "Student not found"}), 400

    marks_collection.update_one(
        {"student_id": data["student_id"], "subject_code": data["subject_code"]},
        {"$set": {"marks": data["marks"]}},
        upsert=True
    )
    return jsonify({"message": "Marks saved"})

@teacher_routes.route("/teacher/students", methods=["GET"])
def get_students():
    data = list(students_collection.find({}, {"_id": 0}))
    return jsonify(data)
