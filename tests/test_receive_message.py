# tests/test_receive_message.py

from core.ui_receive_message_test import receive_message

def test_receive_message(driver):
    logs = receive_message(driver)
    return logs
