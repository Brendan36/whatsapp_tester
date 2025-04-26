# core/ui_login_test.py

from core.driver_setup import create_driver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

def login_to_whatsapp():
    """Perform login to WhatsApp Web."""
    logs = []
    test_name = "Login Test"

    def add_log(action, status):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logs.append(f"[{timestamp}] [{test_name}] [{status}] {action}")

    driver = create_driver()
    driver.get("https://web.whatsapp.com/")
    add_log("Opened WhatsApp Web page.", "INFO")

    login_successful = False
    retries = 0
    max_retries = 3

    while not login_successful and retries < max_retries:
        time.sleep(30)

        try:
            driver.find_element("id", "pane-side")
            login_successful = True
            add_log("Login successful after scanning QR code.", "SUCCESS")
            break
        except NoSuchElementException:
            add_log(f"Login not detected. Attempt {retries+1}/{max_retries}.", "WARNING")
            retries += 1

            driver.execute_script('alert("Need more time? Click OK to continue, Cancel to close.");')

            try:
                WebDriverWait(driver, 5).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                add_log("User clicked OK. Retrying login.", "INFO")
                continue
            except TimeoutException:
                add_log("No response to alert. Auto-closing browser.", "FAIL")
                driver.quit()
                return None, logs, False
            except UnexpectedAlertPresentException:
                add_log("Unexpected alert handled.", "WARNING")
                continue

    if not login_successful:
        add_log("Login failed after maximum retries.", "FAIL")
        driver.quit()
        return None, logs, False

    add_log("Holding browser open after login.", "INFO")
    return driver, logs, True
