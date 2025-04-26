# tests/test_login.py

from core.ui_login_test import login_to_whatsapp

def test_login():
    """Test function to perform WhatsApp Web login."""
    driver, logs, login_successful = login_to_whatsapp()
    return driver, logs, login_successful
