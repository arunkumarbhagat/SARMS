"""
BLACK BOX TESTING - SARMS
Student Attendance & Result Management System
Tests system behavior purely from the API/user perspective.
Run: py -m pytest tests/test_black_box.py -v
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from app import app
from config import (
    users_collection, students_collection, teachers_collection,
    subjects_collection, attendance_collection, marks_collection
)


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture(autouse=True)
def clean_test_data():
    yield
    students_collection.delete_many({"student_id": {"$regex": "^TEST"}})
    teachers_collection.delete_many({"teacher_id": {"$regex": "^TEST"}})
    users_collection.delete_many({"username": {"$regex": "^TEST"}})
    subjects_collection.delete_many({"subject_code": {"$regex": "^TEST"}})
    attendance_collection.delete_many({"student_id": {"$regex": "^TEST"}})
    marks_collection.delete_many({"student_id": {"$regex": "^TEST"}})


# ─────────────────────────────────────────────────────────
# 1. HOME PAGE
# ─────────────────────────────────────────────────────────

class TestHomePage:

    def test_home_page_loads(self, client):
        """BB-01: Home page returns HTTP 200."""
        res = client.get("/")
        assert res.status_code == 200

    def test_home_page_has_role_options(self, client):
        """BB-02: Home page contains Student, Teacher, Admin login links."""
        res = client.get("/")
        assert b"Student" in res.data
        assert b"Teacher" in res.data
        assert b"Admin" in res.data


# ─────────────────────────────────────────────────────────
# 2. LOGIN PAGE
# ─────────────────────────────────────────────────────────

class TestLoginPage:

    def test_login_page_student_loads(self, client):
        """BB-03: GET /login/student returns 200."""
        res = client.get("/login/student")
        assert res.status_code == 200

    def test_login_page_teacher_loads(self, client):
        """BB-04: GET /login/teacher returns 200."""
        res = client.get("/login/teacher")
        assert res.status_code == 200

    def test_login_page_admin_loads(self, client):
        """BB-05: GET /login/admin returns 200."""
        res = client.get("/login/admin")
        assert res.status_code == 200


# ─────────────────────────────────────────────────────────
# 3. LOGIN API
# ─────────────────────────────────────────────────────────

class TestLoginAPI:

    def test_valid_student_login(self, client):
        """BB-06: Valid student credentials return redirect to student_dashboard."""
        users_collection.update_one(
            {"username": "TEST_STU01"},
            {"$set": {"username": "TEST_STU01", "password": "TEST_STU01",
                      "role": "student", "ref_id": "TEST_STU01"}},
            upsert=True
        )
        res = client.post("/login", json={"username": "TEST_STU01", "password": "TEST_STU01"})
        assert res.status_code == 200
        assert res.get_json()["redirect"] == "/student_dashboard"

    def test_valid_teacher_login(self, client):
        """BB-07: Valid teacher credentials return redirect to teacher_dashboard."""
        users_collection.update_one(
            {"username": "TEST_TCH01"},
            {"$set": {"username": "TEST_TCH01", "password": "TEST_TCH01",
                      "role": "teacher", "ref_id": "TEST_TCH01"}},
            upsert=True
        )
        res = client.post("/login", json={"username": "TEST_TCH01", "password": "TEST_TCH01"})
        assert res.status_code == 200
        assert res.get_json()["redirect"] == "/teacher_dashboard"

    def test_valid_admin_login(self, client):
        """BB-08: Valid admin credentials return redirect to admin_dashboard."""
        users_collection.update_one(
            {"username": "TEST_ADMIN"},
            {"$set": {"username": "TEST_ADMIN", "password": "TEST_ADMIN",
                      "role": "admin", "ref_id": "TEST_ADMIN"}},
            upsert=True
        )
        res = client.post("/login", json={"username": "TEST_ADMIN", "password": "TEST_ADMIN"})
        assert res.status_code == 200
        assert res.get_json()["redirect"] == "/admin_dashboard"

    def test_invalid_credentials(self, client):
        """BB-09: Wrong credentials return 401."""
        res = client.post("/login", json={"username": "nobody", "password": "wrong"})
        assert res.status_code == 401
        assert "error" in res.get_json()

    def test_wrong_password(self, client):
        """BB-10: Correct username but wrong password returns 401."""
        users_collection.update_one(
            {"username": "TEST_STU02"},
            {"$set": {"username": "TEST_STU02", "password": "correct",
                      "role": "student", "ref_id": "TEST_STU02"}},
            upsert=True
        )
        res = client.post("/login", json={"username": "TEST_STU02", "password": "wrong"})
        assert res.status_code == 401


# ─────────────────────────────────────────────────────────
# 4. DASHBOARD ACCESS CONTROL
# ─────────────────────────────────────────────────────────

class TestDashboardAccess:

    def test_student_dashboard_without_login_redirects(self, client):
        """BB-11: Accessing student dashboard without login redirects to home."""
        res = client.get("/student_dashboard", follow_redirects=False)
        assert res.status_code == 302

    def test_teacher_dashboard_without_login_redirects(self, client):
        """BB-12: Accessing teacher dashboard without login redirects to home."""
        res = client.get("/teacher_dashboard", follow_redirects=False)
        assert res.status_code == 302

    def test_admin_dashboard_without_login_redirects(self, client):
        """BB-13: Accessing admin dashboard without login redirects to home."""
        res = client.get("/admin_dashboard", follow_redirects=False)
        assert res.status_code == 302

    def test_logout_redirects_to_home(self, client):
        """BB-14: Logout redirects to home page."""
        res = client.get("/logout", follow_redirects=False)
        assert res.status_code == 302
        assert res.headers["Location"] == "/"


# ─────────────────────────────────────────────────────────
# 5. STUDENT DATA API
# ─────────────────────────────────────────────────────────

class TestStudentDataAPI:

    def test_student_data_without_login_returns_401(self, client):
        """BB-15: /student/data without session returns 401."""
        res = client.get("/student/data")
        assert res.status_code == 401

    def test_student_data_with_session_returns_json(self, client):
        """BB-16: /student/data with valid session returns attendance, marks, subjects."""
        users_collection.update_one(
            {"username": "TEST_STU03"},
            {"$set": {"username": "TEST_STU03", "password": "TEST_STU03",
                      "role": "student", "ref_id": "TEST_STU03"}},
            upsert=True
        )
        client.post("/login", json={"username": "TEST_STU03", "password": "TEST_STU03"})
        res = client.get("/student/data")
        assert res.status_code == 200
        data = res.get_json()
        assert "attendance" in data
        assert "marks" in data
        assert "subjects" in data

    def test_get_all_students_returns_list(self, client):
        """BB-17: GET /students returns a JSON list."""
        res = client.get("/students")
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)


# ─────────────────────────────────────────────────────────
# 6. TEACHER ROUTES
# ─────────────────────────────────────────────────────────

class TestTeacherRoutes:

    def _seed_student(self):
        students_collection.update_one(
            {"student_id": "TEST_STU04"},
            {"$set": {"student_id": "TEST_STU04", "name": "Test Student",
                      "department": "CS", "semester": 4}},
            upsert=True
        )

    def test_mark_attendance_valid_student(self, client):
        """BB-18: Marking attendance for valid student returns 200."""
        self._seed_student()
        res = client.post("/teacher/mark_attendance", json={
            "student_id": "TEST_STU04",
            "subject_code": "TEST_CS301",
            "status": "Present",
            "date": "2026-04-01"
        })
        assert res.status_code == 200
        assert res.get_json()["message"] == "Attendance recorded"

    def test_mark_attendance_invalid_student(self, client):
        """BB-19: Marking attendance for non-existent student returns 400."""
        res = client.post("/teacher/mark_attendance", json={
            "student_id": "GHOST999",
            "subject_code": "CS301",
            "status": "Present",
            "date": "2026-04-01"
        })
        assert res.status_code == 400
        assert "error" in res.get_json()

    def test_enter_marks_valid_student(self, client):
        """BB-20: Entering marks for valid student returns 200."""
        self._seed_student()
        res = client.post("/teacher/enter_marks", json={
            "student_id": "TEST_STU04",
            "subject_code": "TEST_CS301",
            "marks": 85
        })
        assert res.status_code == 200
        assert res.get_json()["message"] == "Marks saved"

    def test_enter_marks_invalid_student(self, client):
        """BB-21: Entering marks for non-existent student returns 400."""
        res = client.post("/teacher/enter_marks", json={
            "student_id": "GHOST999",
            "subject_code": "CS301",
            "marks": 90
        })
        assert res.status_code == 400

    def test_get_teacher_students_returns_list(self, client):
        """BB-22: GET /teacher/students returns a JSON list."""
        res = client.get("/teacher/students")
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)


# ─────────────────────────────────────────────────────────
# 7. ADMIN ROUTES
# ─────────────────────────────────────────────────────────

class TestAdminRoutes:

    def test_add_student(self, client):
        """BB-23: Admin can add a student and get success message."""
        res = client.post("/admin/add_student", json={
            "student_id": "TEST_NEW01",
            "name": "New Student",
            "department": "CS",
            "semester": 3
        })
        assert res.status_code == 200
        assert res.get_json()["message"] == "Student added"

    def test_add_student_creates_login(self, client):
        """BB-24: Adding a student auto-creates a login user."""
        client.post("/admin/add_student", json={
            "student_id": "TEST_NEW02",
            "name": "Auto Login",
            "department": "IT",
            "semester": 2
        })
        user = users_collection.find_one({"username": "TEST_NEW02"})
        assert user is not None
        assert user["role"] == "student"

    def test_add_teacher(self, client):
        """BB-25: Admin can add a teacher and get success message."""
        res = client.post("/admin/add_teacher", json={
            "teacher_id": "TEST_TCH02",
            "name": "New Teacher",
            "department": "Math"
        })
        assert res.status_code == 200
        assert res.get_json()["message"] == "Teacher added"

    def test_add_teacher_creates_login(self, client):
        """BB-26: Adding a teacher auto-creates a login user."""
        client.post("/admin/add_teacher", json={
            "teacher_id": "TEST_TCH03",
            "name": "Auto Teacher",
            "department": "Physics"
        })
        user = users_collection.find_one({"username": "TEST_TCH03"})
        assert user is not None
        assert user["role"] == "teacher"

    def test_add_subject(self, client):
        """BB-27: Admin can add a subject and get success message."""
        res = client.post("/admin/add_subject", json={
            "subject_code": "TEST_SUB01",
            "subject_name": "Test Subject",
            "semester": 4,
            "teacher_id": "TEST_TCH01"
        })
        assert res.status_code == 200
        assert res.get_json()["message"] == "Subject added"

    def test_get_admin_students_returns_list(self, client):
        """BB-28: GET /admin/students returns a JSON list."""
        res = client.get("/admin/students")
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)

    def test_get_admin_teachers_returns_list(self, client):
        """BB-29: GET /admin/teachers returns a JSON list."""
        res = client.get("/admin/teachers")
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)


# ─────────────────────────────────────────────────────────
# 8. ATTENDANCE PERSISTENCE
# ─────────────────────────────────────────────────────────

class TestAttendancePersistence:

    def test_attendance_saved_to_db(self, client):
        """BB-30: Attendance record is actually saved in MongoDB."""
        students_collection.update_one(
            {"student_id": "TEST_STU05"},
            {"$set": {"student_id": "TEST_STU05", "name": "Persist Test",
                      "department": "CS", "semester": 1}},
            upsert=True
        )
        client.post("/teacher/mark_attendance", json={
            "student_id": "TEST_STU05",
            "subject_code": "TEST_CS999",
            "status": "Absent",
            "date": "2026-04-05"
        })
        record = attendance_collection.find_one({
            "student_id": "TEST_STU05", "subject_code": "TEST_CS999"
        })
        assert record is not None
        assert record["status"] == "Absent"
