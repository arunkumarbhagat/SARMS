from flask import Blueprint, jsonify, session
from config import students_collection, attendance_collection, marks_collection, subjects_collection

student_routes = Blueprint("student_routes", __name__)

@student_routes.route("/students", methods=["GET"])
def get_students():
    data = list(students_collection.find({}, {"_id": 0}))
    return jsonify(data)

@student_routes.route("/student/data", methods=["GET"])
def get_my_data():
    student_id = session.get("user_id")
    if not student_id:
        return jsonify({"error": "Not logged in"}), 401

    attendance = list(attendance_collection.find({"student_id": student_id}, {"_id": 0}))
    marks = list(marks_collection.find({"student_id": student_id}, {"_id": 0}))
    subjects = list(subjects_collection.find({}, {"_id": 0}))

    return jsonify({"attendance": attendance, "marks": marks, "subjects": subjects})
