# tests/test_delivery_status.py

from core.ui_delivery_status_test import delivery_status

def test_delivery_status(driver):
    logs = delivery_status(driver)
    return logs
