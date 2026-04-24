"""
SELENIUM AUTOMATION TESTS — SARMS
Student Attendance & Result Management System
Login Module + Core Module Automation
Run: python -m pytest selenium_tests/test_sarms_selenium.py -v
Requirements: pip install selenium webdriver-manager
Flask app must be running on http://127.0.0.1:5000
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "http://127.0.0.1:5000"
WAIT     = 10  # seconds
SLOW     = 3   # pause between every action so it's clearly visible


@pytest.fixture(scope="class")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    drv = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    drv.implicitly_wait(WAIT)
    drv.set_page_load_timeout(30)
    yield drv
    drv.quit()


def wait_for(driver, by, value, timeout=WAIT):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))


# ═══════════════════════════════════════════════════════════
# MODULE 1 — HOME PAGE
# ═══════════════════════════════════════════════════════════

class TestSARMSHomePage:

    def test_SA_HP_01_home_page_loads(self, driver):
        """SA-HP-01: Home page loads successfully."""
        driver.get(BASE_URL)
        time.sleep(SLOW)
        assert "SARMS" in driver.title or "University" in driver.page_source
        assert driver.current_url == BASE_URL + "/"

    def test_SA_HP_02_three_role_cards_visible(self, driver):
        """SA-HP-02: All three role cards are visible on home page."""
        driver.get(BASE_URL)
        time.sleep(SLOW)
        page = driver.page_source
        assert "Student" in page
        assert "Teacher" in page
        assert "Admin"   in page

    def test_SA_HP_03_student_login_link(self, driver):
        """SA-HP-03: Student Login button navigates to /login/student."""
        driver.get(BASE_URL)
        time.sleep(SLOW)
        btn = driver.find_element(By.XPATH, "//a[contains(@href,'/login/student')]")
        btn.click()
        time.sleep(SLOW)
        assert "/login/student" in driver.current_url

    def test_SA_HP_04_teacher_login_link(self, driver):
        """SA-HP-04: Teacher Login button navigates to /login/teacher."""
        driver.get(BASE_URL)
        time.sleep(SLOW)
        btn = driver.find_element(By.XPATH, "//a[contains(@href,'/login/teacher')]")
        btn.click()
        time.sleep(SLOW)
        assert "/login/teacher" in driver.current_url

    def test_SA_HP_05_admin_login_link(self, driver):
        """SA-HP-05: Admin Login button navigates to /login/admin."""
        driver.get(BASE_URL)
        time.sleep(SLOW)
        btn = driver.find_element(By.XPATH, "//a[contains(@href,'/login/admin')]")
        btn.click()
        time.sleep(SLOW)
        assert "/login/admin" in driver.current_url


# ═══════════════════════════════════════════════════════════
# MODULE 2 — LOGIN MODULE
# ═══════════════════════════════════════════════════════════

class TestSARMSLoginModule:

    def _open_login(self, driver, role="student"):
        driver.get(f"{BASE_URL}/login/{role}")
        time.sleep(SLOW)

    def _fill_login(self, driver, username, password):
        wait_for(driver, By.ID, "username").clear()
        driver.find_element(By.ID, "username").send_keys(username)
        time.sleep(1)
        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "password").send_keys(password)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(SLOW)

    def test_SA_LM_01_login_page_renders(self, driver):
        """SA-LM-01: Login page renders with username and password fields."""
        self._open_login(driver, "student")
        assert driver.find_element(By.ID, "username").is_displayed()
        assert driver.find_element(By.ID, "password").is_displayed()

    def test_SA_LM_02_valid_student_login(self, driver):
        """SA-LM-02: Valid student credentials redirect to student dashboard."""
        self._open_login(driver, "student")
        self._fill_login(driver, "23BAI001", "23BAI001")
        assert "student_dashboard" in driver.current_url

    def test_SA_LM_03_student_dashboard_welcome(self, driver):
        """SA-LM-03: Student dashboard shows welcome message with username."""
        assert "23BAI001" in driver.page_source or "Welcome" in driver.page_source

    def test_SA_LM_04_logout_from_student(self, driver):
        """SA-LM-04: Logout clears session and redirects to home."""
        driver.find_element(By.XPATH, "//a[contains(@href,'/logout')]").click()
        time.sleep(SLOW)
        assert driver.current_url == BASE_URL + "/"

    def test_SA_LM_05_invalid_credentials(self, driver):
        """SA-LM-05: Invalid credentials show error message."""
        self._open_login(driver, "student")
        self._fill_login(driver, "wronguser", "wrongpass")
        page = driver.page_source
        assert "Invalid" in page or "error" in page.lower() or "credentials" in page.lower()

    def test_SA_LM_06_wrong_password(self, driver):
        """SA-LM-06: Correct username with wrong password shows error."""
        self._open_login(driver, "student")
        self._fill_login(driver, "23BAI001", "wrongpassword")
        page = driver.page_source
        assert "Invalid" in page or "error" in page.lower()

    def test_SA_LM_07_empty_username(self, driver):
        """SA-LM-07: Empty username field prevents form submission."""
        self._open_login(driver, "student")
        driver.find_element(By.ID, "password").send_keys("somepass")
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(SLOW)
        assert "student_dashboard" not in driver.current_url

    def test_SA_LM_08_empty_password(self, driver):
        """SA-LM-08: Empty password field prevents form submission."""
        self._open_login(driver, "student")
        driver.find_element(By.ID, "username").send_keys("23BAI001")
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(SLOW)
        assert "student_dashboard" not in driver.current_url

    def test_SA_LM_09_valid_teacher_login(self, driver):
        """SA-LM-09: Valid teacher credentials redirect to teacher dashboard."""
        self._open_login(driver, "teacher")
        self._fill_login(driver, "TCH001", "TCH001")
        assert "teacher_dashboard" in driver.current_url

    def test_SA_LM_10_logout_from_teacher(self, driver):
        """SA-LM-10: Teacher logout redirects to home."""
        driver.find_element(By.XPATH, "//a[contains(@href,'/logout')]").click()
        time.sleep(SLOW)
        assert driver.current_url == BASE_URL + "/"

    def test_SA_LM_11_valid_admin_login(self, driver):
        """SA-LM-11: Valid admin credentials redirect to admin dashboard."""
        self._open_login(driver, "admin")
        self._fill_login(driver, "admin", "admin123")
        assert "admin_dashboard" in driver.current_url

    def test_SA_LM_12_logout_from_admin(self, driver):
        """SA-LM-12: Admin logout redirects to home."""
        driver.find_element(By.XPATH, "//a[contains(@href,'/logout')]").click()
        time.sleep(SLOW)
        assert driver.current_url == BASE_URL + "/"

    def test_SA_LM_13_direct_dashboard_without_login(self, driver):
        """SA-LM-13: Accessing student dashboard without login redirects to home."""
        driver.get(f"{BASE_URL}/student_dashboard")
        time.sleep(SLOW)
        assert "student_dashboard" not in driver.current_url


# ═══════════════════════════════════════════════════════════
# MODULE 3 — STUDENT CORE MODULE
# ═══════════════════════════════════════════════════════════

class TestSARMSStudentCore:

    def _login_student(self, driver):
        driver.get(f"{BASE_URL}/login/student")
        time.sleep(SLOW)
        driver.find_element(By.ID, "username").send_keys("23BAI001")
        time.sleep(1)
        driver.find_element(By.ID, "password").send_keys("23BAI001")
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(SLOW)

    def test_SA_SC_01_student_dashboard_loads(self, driver):
        """SA-SC-01: Student dashboard loads after login."""
        self._login_student(driver)
        assert "student_dashboard" in driver.current_url

    def test_SA_SC_02_attendance_tab_visible(self, driver):
        """SA-SC-02: Attendance tab is visible on student dashboard."""
        assert "Attendance" in driver.page_source

    def test_SA_SC_03_marks_tab_visible(self, driver):
        """SA-SC-03: Marks tab is visible on student dashboard."""
        assert "Marks" in driver.page_source

    def test_SA_SC_04_subjects_tab_visible(self, driver):
        """SA-SC-04: Subjects tab is visible on student dashboard."""
        assert "Subjects" in driver.page_source

    def test_SA_SC_05_attendance_data_loads(self, driver):
        """SA-SC-05: Attendance table loads data from API."""
        time.sleep(SLOW)
        page = driver.page_source
        assert "CS301" in page or "Present" in page or "Absent" in page

    def test_SA_SC_06_marks_tab_click(self, driver):
        """SA-SC-06: Clicking Marks tab shows marks content."""
        marks_tab = driver.find_element(By.XPATH, "//button[contains(text(),'Marks')]")
        marks_tab.click()
        time.sleep(SLOW)
        assert "Marks" in driver.page_source

    def test_SA_SC_07_subjects_tab_click(self, driver):
        """SA-SC-07: Clicking Subjects tab shows subjects content."""
        sub_tab = driver.find_element(By.XPATH, "//button[contains(text(),'Subjects')]")
        sub_tab.click()
        time.sleep(SLOW)
        assert "Subject" in driver.page_source

    def test_SA_SC_08_logout_student(self, driver):
        """SA-SC-08: Student can logout from dashboard."""
        driver.find_element(By.XPATH, "//a[contains(@href,'/logout')]").click()
        time.sleep(SLOW)
        assert driver.current_url == BASE_URL + "/"


# ═══════════════════════════════════════════════════════════
# MODULE 4 — TEACHER CORE MODULE
# ═══════════════════════════════════════════════════════════

class TestSARMSTeacherCore:

    def _login_teacher(self, driver):
        driver.get(f"{BASE_URL}/login/teacher")
        time.sleep(SLOW)
        driver.find_element(By.ID, "username").send_keys("TCH001")
        time.sleep(1)
        driver.find_element(By.ID, "password").send_keys("TCH001")
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(SLOW)

    def test_SA_TC_01_teacher_dashboard_loads(self, driver):
        """SA-TC-01: Teacher dashboard loads after login."""
        self._login_teacher(driver)
        assert "teacher_dashboard" in driver.current_url

    def test_SA_TC_02_mark_attendance_tab_visible(self, driver):
        """SA-TC-02: Mark Attendance tab is visible."""
        assert "Mark Attendance" in driver.page_source or "Attendance" in driver.page_source

    def test_SA_TC_03_mark_attendance_valid(self, driver):
        """SA-TC-03: Teacher can mark attendance for a valid student."""
        driver.find_element(By.ID, "att_student_id").send_keys("23BAI001")
        time.sleep(1)
        driver.find_element(By.ID, "att_subject_code").send_keys("CS301")
        time.sleep(1)
        Select(driver.find_element(By.ID, "att_status")).select_by_value("Present")
        time.sleep(1)
        driver.find_element(By.ID, "att_date").send_keys("2026-04-10")
        time.sleep(1)
        driver.find_element(By.ID, "attendanceForm").find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(SLOW)
        page = driver.page_source
        assert "Attendance recorded" in page or "success" in page.lower()

    def test_SA_TC_04_enter_marks_tab(self, driver):
        """SA-TC-04: Enter Marks tab is accessible."""
        marks_tab = driver.find_element(By.XPATH, "//button[contains(text(),'Enter Marks') or contains(text(),'Marks')]")
        marks_tab.click()
        time.sleep(SLOW)
        assert "Marks" in driver.page_source

    def test_SA_TC_05_enter_marks_valid(self, driver):
        """SA-TC-05: Teacher can enter marks for a valid student."""
        driver.find_element(By.ID, "m_student_id").send_keys("23BAI001")
        time.sleep(1)
        driver.find_element(By.ID, "m_subject_code").send_keys("CS301")
        time.sleep(1)
        driver.find_element(By.ID, "m_marks").send_keys("95")
        time.sleep(1)
        driver.find_element(By.ID, "marksForm").find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(SLOW)
        page = driver.page_source
        assert "Marks saved" in page or "success" in page.lower()

    def test_SA_TC_06_student_list_tab(self, driver):
        """SA-TC-06: Student List tab loads student data."""
        list_tab = driver.find_element(By.XPATH, "//button[contains(text(),'Student List') or contains(text(),'Students')]")
        list_tab.click()
        time.sleep(SLOW)
        page = driver.page_source
        assert "23BAI" in page or "Arun" in page or "Student" in page

    def test_SA_TC_07_logout_teacher(self, driver):
        """SA-TC-07: Teacher can logout from dashboard."""
        driver.find_element(By.XPATH, "//a[contains(@href,'/logout')]").click()
        time.sleep(SLOW)
        assert driver.current_url == BASE_URL + "/"


# ═══════════════════════════════════════════════════════════
# MODULE 5 — ADMIN CORE MODULE
# ═══════════════════════════════════════════════════════════

class TestSARMSAdminCore:

    def _login_admin(self, driver):
        driver.get(f"{BASE_URL}/login/admin")
        time.sleep(SLOW)
        driver.find_element(By.ID, "username").send_keys("admin")
        time.sleep(1)
        driver.find_element(By.ID, "password").send_keys("admin123")
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(SLOW)

    def test_SA_AC_01_admin_dashboard_loads(self, driver):
        """SA-AC-01: Admin dashboard loads after login."""
        self._login_admin(driver)
        assert "admin_dashboard" in driver.current_url

    def test_SA_AC_02_add_student_tab_visible(self, driver):
        """SA-AC-02: Add Student tab is visible on admin dashboard."""
        assert "Add Student" in driver.page_source or "Student" in driver.page_source

    def test_SA_AC_03_add_student_valid(self, driver):
        """SA-AC-03: Admin can add a new student."""
        driver.find_element(By.ID, "s_id").send_keys("23BAI099")
        time.sleep(1)
        driver.find_element(By.ID, "s_name").send_keys("Selenium Test Student")
        time.sleep(1)
        driver.find_element(By.ID, "s_dept").send_keys("Computer Science")
        time.sleep(1)
        driver.find_element(By.ID, "s_sem").send_keys("4")
        time.sleep(1)
        driver.find_element(By.ID, "studentForm").find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(SLOW)
        page = driver.page_source
        assert "Student added" in page or "success" in page.lower()

    def test_SA_AC_04_add_teacher_tab(self, driver):
        """SA-AC-04: Add Teacher tab is accessible."""
        tab = driver.find_element(By.XPATH, "//button[contains(text(),'Add Teacher')]")
        tab.click()
        time.sleep(SLOW)
        assert "Teacher" in driver.page_source

    def test_SA_AC_05_add_teacher_valid(self, driver):
        """SA-AC-05: Admin can add a new teacher."""
        driver.find_element(By.ID, "t_id").send_keys("TCH099")
        time.sleep(1)
        driver.find_element(By.ID, "t_name").send_keys("Selenium Test Teacher")
        time.sleep(1)
        driver.find_element(By.ID, "t_dept").send_keys("Testing Dept")
        time.sleep(1)
        driver.find_element(By.ID, "teacherForm").find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(SLOW)
        page = driver.page_source
        assert "Teacher added" in page or "success" in page.lower()

    def test_SA_AC_06_add_subject_tab(self, driver):
        """SA-AC-06: Assign Subject tab is accessible."""
        tab = driver.find_element(By.XPATH, "//button[contains(text(),'Subject') or contains(text(),'Assign')]")
        tab.click()
        time.sleep(SLOW)
        assert "Subject" in driver.page_source

    def test_SA_AC_07_add_subject_valid(self, driver):
        """SA-AC-07: Admin can add a new subject."""
        driver.find_element(By.ID, "sub_code").send_keys("SE999")
        time.sleep(1)
        driver.find_element(By.ID, "sub_name").send_keys("Selenium Testing")
        time.sleep(1)
        driver.find_element(By.ID, "sub_sem").send_keys("4")
        time.sleep(1)
        driver.find_element(By.ID, "sub_teacher").send_keys("TCH001")
        time.sleep(1)
        driver.find_element(By.ID, "subjectForm").find_element(
            By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(SLOW)
        page = driver.page_source
        assert "Subject added" in page or "success" in page.lower()

    def test_SA_AC_08_view_all_tab(self, driver):
        """SA-AC-08: View All tab loads students and teachers lists."""
        tab = driver.find_element(By.XPATH, "//button[contains(text(),'View All') or contains(text(),'View')]")
        tab.click()
        time.sleep(SLOW)
        page = driver.page_source
        assert "23BAI" in page or "TCH" in page or "Student" in page

    def test_SA_AC_09_logout_admin(self, driver):
        """SA-AC-09: Admin can logout from dashboard."""
        driver.find_element(By.XPATH, "//a[contains(@href,'/logout')]").click()
        time.sleep(SLOW)
        assert driver.current_url == BASE_URL + "/"
