from flask import Blueprint, render_template, request, jsonify, session
from config import users_collection

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/login/<role>")
def login_page(role):
    return render_template("login.html", role=role)

@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.json
    user = users_collection.find_one({
        "username": data["username"],
        "password": data["password"]
    })

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    session["username"] = user["username"]
    session["role"] = user["role"]
    session["user_id"] = user.get("ref_id", "")  # student_id or teacher_id

    redirects = {
        "student": "/student_dashboard",
        "teacher": "/teacher_dashboard",
        "admin": "/admin_dashboard"
    }
    return jsonify({"redirect": redirects.get(user["role"], "/")})
