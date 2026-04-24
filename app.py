from flask import Flask, render_template, session, redirect
from routes.auth_routes import auth_routes
from routes.student_routes import student_routes
from routes.teacher_routes import teacher_routes
from routes.admin_routes import admin_routes

app = Flask(__name__)
app.secret_key = "sarms_secret_key_2024"

app.register_blueprint(auth_routes)
app.register_blueprint(student_routes)
app.register_blueprint(teacher_routes)
app.register_blueprint(admin_routes)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/student_dashboard")
def student_dashboard():
    if session.get("role") != "student":
        return redirect("/")
    return render_template("student_dashboard.html", user=session.get("username"))

@app.route("/teacher_dashboard")
def teacher_dashboard():
    if session.get("role") != "teacher":
        return redirect("/")
    return render_template("teacher_dashboard.html", user=session.get("username"))

@app.route("/admin_dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect("/")
    return render_template("admin_dashboard.html", user=session.get("username"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
