# core/ui_delivery_status_test.py

from selenium.webdriver.common.by import By
from datetime import datetime
import time

def delivery_status(driver):
    """Check if message was delivered (✔️✔️ double ticks)."""
    logs = []
    test_name = "Delivery Status Test"

    def add_log(action, status):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logs.append(f"[{timestamp}] [{test_name}] [{status}] {action}")

    try:
        time.sleep(3)
        ticks_xpath = '//span[@data-icon="msg-dblcheck"]'
        double_ticks = driver.find_elements(By.XPATH, ticks_xpath)

        if double_ticks:
            add_log("Message delivered successfully (✔️✔️).", "SUCCESS")
        else:
            add_log("Message not yet delivered (no double ticks).", "WARNING")

    except Exception as e:
        add_log(f"Error checking delivery status: {str(e)}", "FAIL")

    return logs
