from flask import Blueprint, request, jsonify
from config import students_collection, teachers_collection, subjects_collection, users_collection

admin_routes = Blueprint("admin_routes", __name__)

@admin_routes.route("/admin/add_student", methods=["POST"])
def add_student():
    data = request.json
    students_collection.insert_one({
        "student_id": data["student_id"],
        "name": data["name"],
        "department": data["department"],
        "semester": data["semester"]
    })
    # create login user for student
    users_collection.update_one(
        {"username": data["student_id"]},
        {"$set": {"username": data["student_id"], "password": data["student_id"], "role": "student", "ref_id": data["student_id"]}},
        upsert=True
    )
    return jsonify({"message": "Student added"})

@admin_routes.route("/admin/add_teacher", methods=["POST"])
def add_teacher():
    data = request.json
    teachers_collection.insert_one({
        "teacher_id": data["teacher_id"],
        "name": data["name"],
        "department": data["department"]
    })
    users_collection.update_one(
        {"username": data["teacher_id"]},
        {"$set": {"username": data["teacher_id"], "password": data["teacher_id"], "role": "teacher", "ref_id": data["teacher_id"]}},
        upsert=True
    )
    return jsonify({"message": "Teacher added"})

@admin_routes.route("/admin/add_subject", methods=["POST"])
def add_subject():
    data = request.json
    subjects_collection.insert_one({
        "subject_code": data["subject_code"],
        "subject_name": data["subject_name"],
        "semester": data["semester"],
        "teacher_id": data["teacher_id"]
    })
    return jsonify({"message": "Subject added"})

@admin_routes.route("/admin/students", methods=["GET"])
def get_students():
    return jsonify(list(students_collection.find({}, {"_id": 0})))

@admin_routes.route("/admin/teachers", methods=["GET"])
def get_teachers():
    return jsonify(list(teachers_collection.find({}, {"_id": 0})))
