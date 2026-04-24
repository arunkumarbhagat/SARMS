# Software Testing Report
## SARMS — Student Attendance & Result Management System

**Project:** Student Attendance & Result Management System (SARMS)  
**Technology Stack:** Flask, MongoDB, Bootstrap 5  
**Testing Framework:** pytest 9.0.3  
**Python Version:** 3.14.3  
**Test Execution Date:** April 9, 2026  
**Total Tests:** 73 | **Passed:** 73 | **Failed:** 0  

---

## 1. Introduction

This report documents the software testing performed on the SARMS university portal. The system supports three user roles — Student, Teacher, and Admin — each with dedicated dashboards and functionality.

Two testing methodologies were applied:

- **Black Box Testing** — validates system behavior from the external user/API perspective with no knowledge of internal code
- **White Box Testing** — validates internal logic, data schemas, guard conditions, and document structures directly

Both test suites were executed against a live MongoDB instance (`sarms_local`) using Flask's built-in test client.

---

## 2. System Under Test — Module Overview

| Module | Description |
|--------|-------------|
| Authentication | Role-based login (Student / Teacher / Admin) via JSON API |
| Student Dashboard | View attendance, marks, subjects |
| Teacher Dashboard | Mark attendance, enter marks, view student list |
| Admin Dashboard | Add students, teachers, subjects; view lists |
| Session Guards | Protect dashboards from unauthorized access |
| Data Models | student_schema, teacher_schema, attendance, marks, subject documents |

---

## 3. Test Environment

| Parameter | Value |
|-----------|-------|
| OS | Windows 11 |
| Python | 3.14.3 |
| pytest | 9.0.3 |
| Flask | Latest |
| Database | MongoDB (localhost:27017) |
| DB Name | sarms_local |
| Test Files | tests/test_black_box.py, tests/test_white_box.py |

---

## 4. Black Box Testing

### 4.1 Overview

Black box testing treats the system as a closed unit. Tests interact only through HTTP endpoints and JSON APIs — exactly as a real browser or client would. No internal code is inspected.

**Total Black Box Tests: 30**  
**Passed: 30 | Failed: 0**

---

### 4.2 Test Cases

#### Module 1 — Home Page

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| BB-01 | Home page loads | GET / | HTTP 200 | 200 OK | PASS |
| BB-02 | Home page shows all roles | GET / | Contains "Student", "Teacher", "Admin" | All present | PASS |

---

#### Module 2 — Login Page

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| BB-03 | Student login page loads | GET /login/student | HTTP 200 | 200 OK | PASS |
| BB-04 | Teacher login page loads | GET /login/teacher | HTTP 200 | 200 OK | PASS |
| BB-05 | Admin login page loads | GET /login/admin | HTTP 200 | 200 OK | PASS |

---

#### Module 3 — Login API

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| BB-06 | Valid student login | username=TEST_STU01, password=TEST_STU01 | HTTP 200, redirect=/student_dashboard | Correct redirect | PASS |
| BB-07 | Valid teacher login | username=TEST_TCH01, password=TEST_TCH01 | HTTP 200, redirect=/teacher_dashboard | Correct redirect | PASS |
| BB-08 | Valid admin login | username=TEST_ADMIN, password=TEST_ADMIN | HTTP 200, redirect=/admin_dashboard | Correct redirect | PASS |
| BB-09 | Invalid credentials | username=nobody, password=wrong | HTTP 401, error in response | 401 returned | PASS |
| BB-10 | Wrong password | Correct username, wrong password | HTTP 401 | 401 returned | PASS |

---

#### Module 4 — Dashboard Access Control

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| BB-11 | Student dashboard without login | GET /student_dashboard (no session) | HTTP 302 redirect | 302 | PASS |
| BB-12 | Teacher dashboard without login | GET /teacher_dashboard (no session) | HTTP 302 redirect | 302 | PASS |
| BB-13 | Admin dashboard without login | GET /admin_dashboard (no session) | HTTP 302 redirect | 302 | PASS |
| BB-14 | Logout redirects to home | GET /logout | HTTP 302 → / | 302 → / | PASS |

---

#### Module 5 — Student Data API

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| BB-15 | Student data without login | GET /student/data (no session) | HTTP 401 | 401 | PASS |
| BB-16 | Student data with valid session | GET /student/data (logged in) | HTTP 200, JSON with attendance, marks, subjects | All keys present | PASS |
| BB-17 | Get all students | GET /students | HTTP 200, JSON list | List returned | PASS |

---

#### Module 6 — Teacher Routes

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| BB-18 | Mark attendance — valid student | POST /teacher/mark_attendance (valid student_id) | HTTP 200, "Attendance recorded" | Success | PASS |
| BB-19 | Mark attendance — invalid student | POST /teacher/mark_attendance (unknown student_id) | HTTP 400, error message | 400 error | PASS |
| BB-20 | Enter marks — valid student | POST /teacher/enter_marks (valid student_id) | HTTP 200, "Marks saved" | Success | PASS |
| BB-21 | Enter marks — invalid student | POST /teacher/enter_marks (unknown student_id) | HTTP 400, error message | 400 error | PASS |
| BB-22 | Get teacher student list | GET /teacher/students | HTTP 200, JSON list | List returned | PASS |

---

#### Module 7 — Admin Routes

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| BB-23 | Add student | POST /admin/add_student (valid data) | HTTP 200, "Student added" | Success | PASS |
| BB-24 | Add student creates login | POST /admin/add_student | User created in users collection | User found in DB | PASS |
| BB-25 | Add teacher | POST /admin/add_teacher (valid data) | HTTP 200, "Teacher added" | Success | PASS |
| BB-26 | Add teacher creates login | POST /admin/add_teacher | User created in users collection | User found in DB | PASS |
| BB-27 | Add subject | POST /admin/add_subject (valid data) | HTTP 200, "Subject added" | Success | PASS |
| BB-28 | Get admin students list | GET /admin/students | HTTP 200, JSON list | List returned | PASS |
| BB-29 | Get admin teachers list | GET /admin/teachers | HTTP 200, JSON list | List returned | PASS |

---

#### Module 8 — Attendance Persistence

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| BB-30 | Attendance saved to MongoDB | POST /teacher/mark_attendance | Record exists in DB with correct status | Record found | PASS |

---

### 4.3 Black Box Test Summary

| Module | Total Tests | Passed | Failed |
|--------|-------------|--------|--------|
| Home Page | 2 | 2 | 0 |
| Login Page | 3 | 3 | 0 |
| Login API | 5 | 5 | 0 |
| Dashboard Access Control | 4 | 4 | 0 |
| Student Data API | 3 | 3 | 0 |
| Teacher Routes | 5 | 5 | 0 |
| Admin Routes | 7 | 7 | 0 |
| Attendance Persistence | 1 | 1 | 0 |
| **TOTAL** | **30** | **30** | **0** |

---

## 5. White Box Testing

### 5.1 Overview

White box testing examines the internal structure of the code. Tests directly invoke model functions, verify document schemas, trace all logical branches in guard conditions, and validate data transformation logic.

**Total White Box Tests: 43**  
**Passed: 43 | Failed: 0**

---

### 5.2 Test Cases

#### Module 1 — student_schema() — models/student_model.py

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| WB-01 | All required keys present | Full data dict | Keys: name, email, department, semester | All present | PASS |
| WB-02 | Name stored correctly | name="Rahul Sharma" | schema["name"] == "Rahul Sharma" | Correct | PASS |
| WB-03 | Email stored correctly | email="test@college.edu" | schema["email"] == "test@college.edu" | Correct | PASS |
| WB-04 | Department stored correctly | department="Mechanical" | schema["department"] == "Mechanical" | Correct | PASS |
| WB-05 | Semester stored correctly | semester=6 | schema["semester"] == 6 | Correct | PASS |
| WB-06 | No extra keys in schema | Full data dict | Exactly 4 keys | 4 keys only | PASS |

---

#### Module 2 — teacher_schema() — models/teacher_model.py

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| WB-07 | All required keys present | Full data dict | Keys: teacher_id, name, department | All present | PASS |
| WB-08 | teacher_id stored correctly | teacher_id="TCH999" | schema["teacher_id"] == "TCH999" | Correct | PASS |
| WB-09 | Name stored correctly | name="Dr. Sneha Patel" | schema["name"] == "Dr. Sneha Patel" | Correct | PASS |
| WB-10 | Department stored correctly | department="Electronics" | schema["department"] == "Electronics" | Correct | PASS |
| WB-11 | No extra keys in schema | Full data dict | Exactly 3 keys | 3 keys only | PASS |

---

#### Module 3 — Login Redirect Logic — routes/auth_routes.py

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| WB-12 | Student role → student dashboard | role="student" | /student_dashboard | /student_dashboard | PASS |
| WB-13 | Teacher role → teacher dashboard | role="teacher" | /teacher_dashboard | /teacher_dashboard | PASS |
| WB-14 | Admin role → admin dashboard | role="admin" | /admin_dashboard | /admin_dashboard | PASS |
| WB-15 | Unknown/None role → home | role="unknown", None, "" | / | / | PASS |

---

#### Module 4 — Session Guard Logic — app.py

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| WB-16 | Student allowed on student dashboard | session_role="student", required="student" | True (allowed) | True | PASS |
| WB-17 | Teacher blocked on student dashboard | session_role="teacher", required="student" | False (blocked) | False | PASS |
| WB-18 | Admin blocked on student dashboard | session_role="admin", required="student" | False (blocked) | False | PASS |
| WB-19 | None session blocked on all dashboards | session_role=None | False for all | False | PASS |
| WB-20 | Admin allowed on admin dashboard | session_role="admin", required="admin" | True (allowed) | True | PASS |
| WB-21 | Teacher allowed on teacher dashboard | session_role="teacher", required="teacher" | True (allowed) | True | PASS |

---

#### Module 5 — Attendance Record Structure — routes/teacher_routes.py

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| WB-22 | Attendance has all 4 fields | Full attendance data | Keys: student_id, subject_code, status, date | All present | PASS |
| WB-23 | Status "Present" stored correctly | status="Present" | record["status"] == "Present" | Correct | PASS |
| WB-24 | Status "Absent" stored correctly | status="Absent" | record["status"] == "Absent" | Correct | PASS |
| WB-25 | student_id stored correctly | student_id="23BAI002" | record["student_id"] == "23BAI002" | Correct | PASS |
| WB-26 | Date stored correctly | date="2026-12-25" | record["date"] == "2026-12-25" | Correct | PASS |

---

#### Module 6 — Marks Upsert Logic — routes/teacher_routes.py

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| WB-27 | Upsert filter has student_id | student_id="23BAI001" | "student_id" in filter | Present | PASS |
| WB-28 | Upsert filter has subject_code | subject_code="CS301" | "subject_code" in filter | Present | PASS |
| WB-29 | Update uses $set operator | marks=88 | "$set" in update doc | Present | PASS |
| WB-30 | Marks value in $set | marks=95 | update["$set"]["marks"] == 95 | 95 | PASS |

---

#### Module 7 — Admin Student Document — routes/admin_routes.py

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| WB-31 | Student doc has all fields | Full data | Keys: student_id, name, department, semester | All present | PASS |
| WB-32 | student_id stored correctly | student_id="23BAI099" | doc["student_id"] == "23BAI099" | Correct | PASS |

---

#### Module 8 — Auto Login Creation Logic — routes/admin_routes.py

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| WB-33 | Student login username equals ID | student_id="23BAI001" | username == "23BAI001" | Correct | PASS |
| WB-34 | Student default password equals ID | student_id="23BAI001" | password == "23BAI001" | Correct | PASS |
| WB-35 | Student login role is "student" | role="student" | doc["role"] == "student" | Correct | PASS |
| WB-36 | Teacher login role is "teacher" | role="teacher" | doc["role"] == "teacher" | Correct | PASS |
| WB-37 | ref_id equals entity ID | student_id="23BAI001" | ref_id == "23BAI001" | Correct | PASS |

---

#### Module 9 — Subject Document Structure — routes/admin_routes.py

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| WB-38 | Subject doc has all 4 fields | Full data | Keys: subject_code, subject_name, semester, teacher_id | All present | PASS |
| WB-39 | subject_code stored correctly | subject_code="MA201" | doc["subject_code"] == "MA201" | Correct | PASS |
| WB-40 | teacher_id linked correctly | teacher_id="TCH003" | doc["teacher_id"] == "TCH003" | Correct | PASS |

---

#### Module 10 — Student Data Session Check — routes/student_routes.py

| Test ID | Test Case | Input | Expected Output | Actual Output | Status |
|---------|-----------|-------|-----------------|---------------|--------|
| WB-41 | Empty session → not logged in | session={} | False | False | PASS |
| WB-42 | Session with user_id → logged in | session={"user_id":"23BAI001"} | True | True | PASS |
| WB-43 | Session without user_id → not logged in | session={"role":"student"} | False | False | PASS |

---

### 5.3 White Box Test Summary

| Module | Total Tests | Passed | Failed |
|--------|-------------|--------|--------|
| student_schema() | 6 | 6 | 0 |
| teacher_schema() | 5 | 5 | 0 |
| Login Redirect Logic | 4 | 4 | 0 |
| Session Guard Logic | 6 | 6 | 0 |
| Attendance Record Structure | 5 | 5 | 0 |
| Marks Upsert Logic | 4 | 4 | 0 |
| Admin Student Document | 2 | 2 | 0 |
| Auto Login Creation Logic | 5 | 5 | 0 |
| Subject Document Structure | 3 | 3 | 0 |
| Student Data Session Check | 3 | 3 | 0 |
| **TOTAL** | **43** | **43** | **0** |

---

## 6. Combined Test Execution Results

```
============================= test session starts ==============================
platform win32 -- Python 3.14.3, pytest-9.0.3

tests/test_white_box.py — 43 passed in 0.15s
tests/test_black_box.py — 30 passed in 0.59s

========================= 73 passed in 0.74s ===================================
```

---

## 7. Coverage Analysis

| Feature Area | Black Box Coverage | White Box Coverage |
|---|---|---|
| Authentication | Login for all 3 roles, invalid credentials, wrong password | Redirect mapping logic, all role branches |
| Session Management | Dashboard access without login (3 dashboards), logout | Guard logic for all role combinations including None |
| Student Features | /student/data auth check, data structure, /students list | Session check logic (3 branches), student_schema fields |
| Teacher Features | Mark attendance (valid/invalid), enter marks (valid/invalid), student list | Attendance document structure, marks upsert filter and $set |
| Admin Features | Add student/teacher/subject, auto-login creation, list endpoints | Student doc structure, teacher doc structure, auto-login logic |
| Data Models | API response keys verified | All schema fields, no extra keys, correct types |

---

## 8. Defects Found

No defects were found during testing. All 73 test cases passed on first execution.

---

## 9. Comparison: Black Box vs White Box

| Aspect | Black Box | White Box |
|--------|-----------|-----------|
| Perspective | External (HTTP/API) | Internal (functions/logic) |
| Knowledge required | Only API spec | Full source code |
| What it tests | HTTP status codes, redirects, JSON responses | Schema fields, guard branches, document structure |
| Tools used | Flask test client, HTTP assertions | Direct function calls, dict inspection |
| Tests written | 30 | 43 |
| Execution time | 0.59s | 0.15s |
| Best for finding | Missing auth checks, wrong status codes, broken routes | Schema bugs, wrong defaults, logic branch errors |

---

## 10. Conclusion

The SARMS application passed all 73 test cases across both testing methodologies.

Black box testing confirmed that all three user roles authenticate correctly, dashboards are protected from unauthorized access, teacher operations validate student existence before writing, and admin operations correctly create both entity records and login accounts simultaneously.

White box testing confirmed that all data schemas produce correct document structures with no extra or missing fields, role-based redirect logic covers all branches including unknown roles, session guards correctly block all unauthorized role combinations, and the marks upsert uses the correct MongoDB $set operator with proper filter keys.

The system is functionally stable across all modules and ready for further integration or UAT testing.
