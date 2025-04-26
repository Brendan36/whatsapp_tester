# tests/test_logout.py

from core.ui_logout_test import logout

def test_logout(driver):
    logs = logout(driver)
    return logs
