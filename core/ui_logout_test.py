# core/ui_logout_test.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

def logout(driver):
    """Logout from WhatsApp Web."""
    logs = []
    test_name = "Logout Test"

    def add_log(action, status):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logs.append(f"[{timestamp}] [{test_name}] [{status}] {action}")

    try:
        menu_button_xpath = '//div[@title="Menu"]'
        menu_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, menu_button_xpath)))
        menu_button.click()

        time.sleep(1)

        logout_xpath = '//div[text()="Log out"]'
        logout_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, logout_xpath)))
        logout_button.click()

        add_log("Successfully logged out from WhatsApp Web.", "SUCCESS")

    except Exception as e:
        add_log(f"Error while logging out: {str(e)}", "FAIL")

    return logs
