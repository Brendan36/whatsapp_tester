# core/ui_receive_message_test.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

def receive_message(driver):
    """Check for a received message after sending."""
    logs = []
    test_name = "Receive Message Test"

    def add_log(action, status):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logs.append(f"[{timestamp}] [{test_name}] [{status}] {action}")

    try:
        time.sleep(3)  # Give some time for the message to arrive

        last_message_xpath = '(//div[contains(@class,"message-in")])[last()]'
        message = driver.find_element(By.XPATH, last_message_xpath)

        if message:
            add_log("Received new incoming message!", "SUCCESS")
        else:
            add_log("No new incoming message detected.", "INFO")

    except Exception as e:
        add_log(f"Error checking received message: {str(e)}", "FAIL")

    return logs
