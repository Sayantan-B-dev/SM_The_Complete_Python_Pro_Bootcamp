import logging
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from app.config import Config
from app.models import data_manager, report_manager

logger = logging.getLogger(__name__)

def setup_driver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    return driver

def login_to_web_app(driver, config):
    url = config['web']['login_url']
    username = os.getenv('WEB_USERNAME')
    password = os.getenv('WEB_PASSWORD')
    if not username or not password:
        raise ValueError("Missing WEB_USERNAME or WEB_PASSWORD in .env")
    driver.get(url)
    try:
        wait = WebDriverWait(driver, 10)
        username_field = wait.until(EC.presence_of_element_located((By.ID, config['web']['username_field'])))
        password_field = driver.find_element(By.ID, config['web']['password_field'])
        login_button = driver.find_element(By.ID, config['web']['login_button'])
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        logger.info("Login successful")
    except TimeoutException:
        logger.error("Login page elements not found")
        raise

def fill_form(driver, row, config):
    """Fill form using row data. Customize selectors and fields."""
    # Example: adjust based on your actual form
    # Here we assume the form fields are named 'field1', 'field2', etc.
    # You can map CSV columns to form fields using a mapping in config.
    mapping = config.get('form_mapping', {})
    for csv_col, form_field in mapping.items():
        element = driver.find_element(By.ID, form_field)
        element.clear()
        element.send_keys(str(row[csv_col]))
    submit_button = driver.find_element(By.ID, config['web']['submit_button'])
    submit_button.click()
    time.sleep(2)  # wait for submission

def run_automation_once():
    """Execute one full automation cycle."""
    config = Config.automation_config
    logger.info("Automation cycle started")

    # Read input data
    df = data_manager.read_data()
    if df.empty:
        logger.info("No input data to process")
        return

    # Web automation if enabled
    if config.get('web', {}).get('enabled', False):
        driver = setup_driver(headless=True)
        try:
            login_to_web_app(driver, config)
            for idx, row in df.iterrows():
                fill_form(driver, row, config)
                logger.info(f"Processed row {idx+1}")
        except Exception as e:
            logger.error(f"Web automation failed: {e}")
        finally:
            driver.quit()

    # Generate report (example: summary statistics)
    report = df.describe()
    report_manager.write_report(report)
    logger.info("Report generated and saved")

    # Optional: send email (we can reuse original send_email, but need to adapt)
    # For brevity, email part can be added later.

    logger.info("Automation cycle completed")