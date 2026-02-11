from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def fetch_html(url, wait=5):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(wait)
        return driver.page_source
    finally:
        driver.quit()