# -*- coding: utf-8 -*-
# Manual setup of Chrome WebDriver
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options

# def create_driver():
#     """Sets up and returns a Chrome WebDriver."""
#     chrome_options = Options()
#     chrome_options.add_argument("--start-maximized")  # Start browser maximized
#
#     # Path to your chromedriver.exe
#     DRIVER_PATH = "chromedriver-win64/chromedriver.exe"  # 🔥 Update this manually!
#
#     service = Service(executable_path=DRIVER_PATH)
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#
#     return driver

# Automatic setup of Chrome WebDriver
# core/driver_setup.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def create_driver():
    """Sets up and returns a Chrome WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--window-size=960,1080")  # half screen width
    chrome_options.add_argument("--window-position=960,0")  # right side
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver
