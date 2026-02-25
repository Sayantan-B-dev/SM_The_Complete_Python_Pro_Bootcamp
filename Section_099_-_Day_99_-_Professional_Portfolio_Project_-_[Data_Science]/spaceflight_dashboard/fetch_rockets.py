import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def parse_rocket_card(card, index):
    """Extract data from a single rocket card."""
    data = {}
    try:
        img = card.find_element(By.TAG_NAME, "img")
        data['image_url'] = img.get_attribute('src')
    except:
        data['image_url'] = ''
    try:
        title = card.find_element(By.CSS_SELECTOR, "h3.text-white")
        data['name'] = title.text.strip()
    except:
        data['name'] = ''
    try:
        agency_elem = card.find_element(By.CSS_SELECTOR, ".text-label-secondary .inline-flex span.w-full")
        data['agency'] = agency_elem.text.strip()
    except:
        data['agency'] = ''

    print(f"[{index}] {data.get('name', 'Unknown')} – {data.get('agency', '?')}")
    return data

def fetch_rockets():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://nextspaceflight.com/rockets/")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".grid.grid-cols-1.sm\\:grid-cols-2.xl\\:grid-cols-3.gap-8 > div")))
    # Rockets page loads all cards without infinite scroll
    cards = driver.find_elements(By.CSS_SELECTOR, ".grid.grid-cols-1.sm\\:grid-cols-2.xl\\:grid-cols-3.gap-8 > div")
    total = len(cards)
    print(f"\nFound {total} rocket cards. Parsing...\n")
    rockets = []
    for idx, card in enumerate(cards, start=1):
        rockets.append(parse_rocket_card(card, idx))
    driver.quit()
    return rockets

if __name__ == "__main__":
    os.makedirs('data', exist_ok=True)
    data = fetch_rockets()
    with open('data/rockets.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'agency', 'image_url'])
        writer.writeheader()
        writer.writerows(data)
    print(f"\nSaved {len(data)} rockets to data/rockets.csv")