# tests/test_send_message.py

from core.ui_send_message_test import send_message

def test_send_message(driver, contact_name="Test Contact", message_text="Hello from WhatsApp Web Tester Bot!"):
    logs = send_message(driver, contact_name, message_text)
    return logs
