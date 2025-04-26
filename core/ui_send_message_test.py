# core/ui_send_message_test.py

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

def send_message(driver, contact_name="Test Contact", message_text="Hello from WhatsApp Web Tester Bot!"):
    """Send a WhatsApp message."""
    logs = []
    test_name = "Send Message Test"

    def add_log(action, status):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logs.append(f"[{timestamp}] [{test_name}] [{status}] {action}")

    try:
        search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'
        search_box = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, search_xpath)))
        search_box.clear()
        search_box.click()
        search_box.send_keys(contact_name)
        search_box.send_keys(Keys.ENTER)
        add_log(f"Opened chat with {contact_name}.", "SUCCESS")

        time.sleep(2)

        message_box_xpath = '//div[@contenteditable="true"][@data-tab="10"]'
        message_box = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, message_box_xpath)))
        message_box.click()
        message_box.send_keys(message_text)
        message_box.send_keys(Keys.ENTER)
        add_log(f"Sent message to {contact_name}: '{message_text}'", "SUCCESS")

    except Exception as e:
        add_log(f"Failed to send message: {str(e)}", "FAIL")

    return logs
