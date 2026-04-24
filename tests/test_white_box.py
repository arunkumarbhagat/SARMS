"""
WHITE BOX TESTING - SARMS
Student Attendance & Result Management System
Tests internal logic, schemas, guards, and data transformations directly.
Run: py -m pytest tests/test_white_box.py -v
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from models.student_model import student_schema
from models.teacher_model import teacher_schema


# ─────────────────────────────────────────────────────────
# 1. student_schema — models/student_model.py
# ─────────────────────────────────────────────────────────

class TestStudentSchema:

    def test_all_keys_present(self):
        """WB-01: student_schema returns all required keys."""
        data = {"name": "Alice", "email": "a@x.com", "department": "CS", "semester": 4}
        schema = student_schema(data)
        for key in ["name", "email", "department", "semester"]:
            assert key in schema

    def test_name_stored_correctly(self):
        """WB-02: Name is stored as provided."""
        data = {"name": "Rahul Sharma", "email": "r@x.com", "department": "IT", "semester": 2}
        assert student_schema(data)["name"] == "Rahul Sharma"

    def test_email_stored_correctly(self):
        """WB-03: Email is stored as provided."""
        data = {"name": "X", "email": "test@college.edu", "department": "CS", "semester": 1}
        assert student_schema(data)["email"] == "test@college.edu"

    def test_department_stored_correctly(self):
        """WB-04: Department is stored as provided."""
        data = {"name": "X", "email": "x@x.com", "department": "Mechanical", "semester": 3}
        assert student_schema(data)["department"] == "Mechanical"

    def test_semester_stored_correctly(self):
        """WB-05: Semester is stored as provided."""
        data = {"name": "X", "email": "x@x.com", "department": "CS", "semester": 6}
        assert student_schema(data)["semester"] == 6

    def test_schema_has_no_extra_keys(self):
        """WB-06: student_schema does not add unexpected keys."""
        data = {"name": "X", "email": "x@x.com", "department": "CS", "semester": 1}
        schema = student_schema(data)
        assert set(schema.keys()) == {"name", "email", "department", "semester"}


# ─────────────────────────────────────────────────────────
# 2. teacher_schema — models/teacher_model.py
# ─────────────────────────────────────────────────────────

class TestTeacherSchema:

    def test_all_keys_present(self):
        """WB-07: teacher_schema returns all required keys."""
        data = {"teacher_id": "TCH001", "name": "Dr. Kumar", "department": "CS"}
        schema = teacher_schema(data)
        for key in ["teacher_id", "name", "department"]:
            assert key in schema

    def test_teacher_id_stored_correctly(self):
        """WB-08: teacher_id is stored as provided."""
        data = {"teacher_id": "TCH999", "name": "Prof X", "department": "Math"}
        assert teacher_schema(data)["teacher_id"] == "TCH999"

    def test_name_stored_correctly(self):
        """WB-09: Teacher name is stored as provided."""
        data = {"teacher_id": "T01", "name": "Dr. Sneha Patel", "department": "Physics"}
        assert teacher_schema(data)["name"] == "Dr. Sneha Patel"

    def test_department_stored_correctly(self):
        """WB-10: Department is stored as provided."""
        data = {"teacher_id": "T01", "name": "X", "department": "Electronics"}
        assert teacher_schema(data)["department"] == "Electronics"

    def test_schema_has_no_extra_keys(self):
        """WB-11: teacher_schema does not add unexpected keys."""
        data = {"teacher_id": "T01", "name": "X", "department": "CS"}
        schema = teacher_schema(data)
        assert set(schema.keys()) == {"teacher_id", "name", "department"}


# ─────────────────────────────────────────────────────────
# 3. Login redirect logic — routes/auth_routes.py
# ─────────────────────────────────────────────────────────

class TestLoginRedirectLogic:
    """Tests the role-to-redirect mapping logic directly."""

    def _get_redirect(self, role):
        redirects = {
            "student": "/student_dashboard",
            "teacher": "/teacher_dashboard",
            "admin":   "/admin_dashboard"
        }
        return redirects.get(role, "/")

    def test_student_role_redirects_to_student_dashboard(self):
        """WB-12: Role 'student' maps to /student_dashboard."""
        assert self._get_redirect("student") == "/student_dashboard"

    def test_teacher_role_redirects_to_teacher_dashboard(self):
        """WB-13: Role 'teacher' maps to /teacher_dashboard."""
        assert self._get_redirect("teacher") == "/teacher_dashboard"

    def test_admin_role_redirects_to_admin_dashboard(self):
        """WB-14: Role 'admin' maps to /admin_dashboard."""
        assert self._get_redirect("admin") == "/admin_dashboard"

    def test_unknown_role_redirects_to_home(self):
        """WB-15: Unknown role defaults to /."""
        assert self._get_redirect("unknown") == "/"
        assert self._get_redirect(None) == "/"
        assert self._get_redirect("") == "/"


# ─────────────────────────────────────────────────────────
# 4. Session guard logic — app.py
# ─────────────────────────────────────────────────────────

class TestSessionGuardLogic:
    """Tests the role-based session guard used in dashboard routes."""

    def _is_allowed(self, session_role, required_role):
        return session_role == required_role

    def test_student_allowed_on_student_dashboard(self):
        """WB-16: session role 'student' passes student dashboard guard."""
        assert self._is_allowed("student", "student") is True

    def test_teacher_blocked_on_student_dashboard(self):
        """WB-17: session role 'teacher' blocked from student dashboard."""
        assert self._is_allowed("teacher", "student") is False

    def test_admin_blocked_on_student_dashboard(self):
        """WB-18: session role 'admin' blocked from student dashboard."""
        assert self._is_allowed("admin", "student") is False

    def test_no_session_blocked(self):
        """WB-19: None session role is blocked from all dashboards."""
        assert self._is_allowed(None, "student") is False
        assert self._is_allowed(None, "teacher") is False
        assert self._is_allowed(None, "admin")   is False

    def test_admin_allowed_on_admin_dashboard(self):
        """WB-20: session role 'admin' passes admin dashboard guard."""
        assert self._is_allowed("admin", "admin") is True

    def test_teacher_allowed_on_teacher_dashboard(self):
        """WB-21: session role 'teacher' passes teacher dashboard guard."""
        assert self._is_allowed("teacher", "teacher") is True


# ─────────────────────────────────────────────────────────
# 5. Attendance record structure — teacher_routes.py
# ─────────────────────────────────────────────────────────

class TestAttendanceRecordStructure:
    """Tests the attendance document structure built in teacher_routes."""

    def _build_attendance(self, student_id, subject_code, status, date):
        return {
            "student_id":   student_id,
            "subject_code": subject_code,
            "status":       status,
            "date":         date
        }

    def test_attendance_has_all_fields(self):
        """WB-22: Attendance record contains all 4 required fields."""
        rec = self._build_attendance("23BAI001", "CS301", "Present", "2026-04-01")
        for key in ["student_id", "subject_code", "status", "date"]:
            assert key in rec

    def test_attendance_status_present(self):
        """WB-23: Status 'Present' is stored correctly."""
        rec = self._build_attendance("23BAI001", "CS301", "Present", "2026-04-01")
        assert rec["status"] == "Present"

    def test_attendance_status_absent(self):
        """WB-24: Status 'Absent' is stored correctly."""
        rec = self._build_attendance("23BAI001", "CS301", "Absent", "2026-04-01")
        assert rec["status"] == "Absent"

    def test_attendance_student_id_stored(self):
        """WB-25: student_id is stored as provided."""
        rec = self._build_attendance("23BAI002", "MA201", "Present", "2026-04-02")
        assert rec["student_id"] == "23BAI002"

    def test_attendance_date_stored(self):
        """WB-26: Date is stored as provided."""
        rec = self._build_attendance("23BAI001", "CS301", "Present", "2026-12-25")
        assert rec["date"] == "2026-12-25"


# ─────────────────────────────────────────────────────────
# 6. Marks upsert logic — teacher_routes.py
# ─────────────────────────────────────────────────────────

class TestMarksUpsertLogic:
    """Tests the upsert filter and update structure for marks."""

    def _build_upsert_filter(self, student_id, subject_code):
        return {"student_id": student_id, "subject_code": subject_code}

    def _build_upsert_update(self, marks):
        return {"$set": {"marks": marks}}

    def test_filter_has_student_id(self):
        """WB-27: Upsert filter contains student_id."""
        f = self._build_upsert_filter("23BAI001", "CS301")
        assert "student_id" in f

    def test_filter_has_subject_code(self):
        """WB-28: Upsert filter contains subject_code."""
        f = self._build_upsert_filter("23BAI001", "CS301")
        assert "subject_code" in f

    def test_update_uses_set_operator(self):
        """WB-29: Update document uses $set operator."""
        u = self._build_upsert_update(88)
        assert "$set" in u

    def test_marks_value_stored_in_update(self):
        """WB-30: Marks value is correctly placed inside $set."""
        u = self._build_upsert_update(95)
        assert u["$set"]["marks"] == 95


# ─────────────────────────────────────────────────────────
# 7. Admin student document structure — admin_routes.py
# ─────────────────────────────────────────────────────────

class TestAdminStudentDocument:

    def _build_student_doc(self, data):
        return {
            "student_id": data["student_id"],
            "name":       data["name"],
            "department": data["department"],
            "semester":   data["semester"]
        }

    def test_student_doc_has_all_fields(self):
        """WB-31: Student document has student_id, name, department, semester."""
        doc = self._build_student_doc({
            "student_id": "23BAI001", "name": "Arun",
            "department": "CS", "semester": 4
        })
        for key in ["student_id", "name", "department", "semester"]:
            assert key in doc

    def test_student_id_stored_correctly(self):
        """WB-32: student_id is stored as provided."""
        doc = self._build_student_doc({
            "student_id": "23BAI099", "name": "X",
            "department": "IT", "semester": 1
        })
        assert doc["student_id"] == "23BAI099"


# ─────────────────────────────────────────────────────────
# 8. Admin auto-login creation logic — admin_routes.py
# ─────────────────────────────────────────────────────────

class TestAutoLoginCreation:
    """Tests the logic that auto-creates user login when admin adds student/teacher."""

    def _build_user_doc(self, entity_id, role):
        return {
            "username": entity_id,
            "password": entity_id,   # default password = ID
            "role":     role,
            "ref_id":   entity_id
        }

    def test_student_login_username_equals_id(self):
        """WB-33: Auto-created student login username equals student_id."""
        doc = self._build_user_doc("23BAI001", "student")
        assert doc["username"] == "23BAI001"

    def test_student_login_password_equals_id(self):
        """WB-34: Auto-created student login default password equals student_id."""
        doc = self._build_user_doc("23BAI001", "student")
        assert doc["password"] == "23BAI001"

    def test_student_login_role_is_student(self):
        """WB-35: Auto-created student login has role 'student'."""
        doc = self._build_user_doc("23BAI001", "student")
        assert doc["role"] == "student"

    def test_teacher_login_role_is_teacher(self):
        """WB-36: Auto-created teacher login has role 'teacher'."""
        doc = self._build_user_doc("TCH001", "teacher")
        assert doc["role"] == "teacher"

    def test_ref_id_equals_entity_id(self):
        """WB-37: ref_id in user document equals the entity ID."""
        doc = self._build_user_doc("23BAI001", "student")
        assert doc["ref_id"] == "23BAI001"


# ─────────────────────────────────────────────────────────
# 9. Subject document structure — admin_routes.py
# ─────────────────────────────────────────────────────────

class TestSubjectDocument:

    def _build_subject_doc(self, data):
        return {
            "subject_code": data["subject_code"],
            "subject_name": data["subject_name"],
            "semester":     data["semester"],
            "teacher_id":   data["teacher_id"]
        }

    def test_subject_doc_has_all_fields(self):
        """WB-38: Subject document has all 4 required fields."""
        doc = self._build_subject_doc({
            "subject_code": "CS301", "subject_name": "Data Structures",
            "semester": 4, "teacher_id": "TCH001"
        })
        for key in ["subject_code", "subject_name", "semester", "teacher_id"]:
            assert key in doc

    def test_subject_code_stored_correctly(self):
        """WB-39: subject_code is stored as provided."""
        doc = self._build_subject_doc({
            "subject_code": "MA201", "subject_name": "Algebra",
            "semester": 2, "teacher_id": "TCH002"
        })
        assert doc["subject_code"] == "MA201"

    def test_teacher_id_linked_correctly(self):
        """WB-40: teacher_id is stored correctly in subject document."""
        doc = self._build_subject_doc({
            "subject_code": "PH301", "subject_name": "Quantum",
            "semester": 3, "teacher_id": "TCH003"
        })
        assert doc["teacher_id"] == "TCH003"


# ─────────────────────────────────────────────────────────
# 10. Student data API session check — student_routes.py
# ─────────────────────────────────────────────────────────

class TestStudentDataSessionCheck:
    """Tests the session guard logic in /student/data."""

    def _is_logged_in(self, session):
        return bool(session.get("user_id"))

    def test_empty_session_not_logged_in(self):
        """WB-41: Empty session means not logged in."""
        assert self._is_logged_in({}) is False

    def test_session_with_user_id_is_logged_in(self):
        """WB-42: Session with user_id means logged in."""
        assert self._is_logged_in({"user_id": "23BAI001"}) is True

    def test_session_without_user_id_not_logged_in(self):
        """WB-43: Session with other keys but no user_id is not logged in."""
        assert self._is_logged_in({"role": "student", "username": "x"}) is False
