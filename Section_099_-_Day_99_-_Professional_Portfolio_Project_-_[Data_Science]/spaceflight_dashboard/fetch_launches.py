import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def scroll_until_end(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def parse_launch_card(card, index):
    """Extract data from a single launch card."""
    data = {}
    try:
        img = card.find_element(By.TAG_NAME, "img")
        data['image_url'] = img.get_attribute('src')
    except:
        data['image_url'] = ''
    try:
        title = card.find_element(By.CSS_SELECTOR, "h3.text-white.text-shadow-lg.font-bold.text-2xl")
        data['name'] = title.text.strip()
    except:
        data['name'] = ''
    try:
        spans = card.find_elements(By.CSS_SELECTOR, ".text-label-secondary .inline-flex span.w-full")
        if len(spans) >= 1:
            raw = spans[0].text.strip()          # e.g. "Falcon 9 Block 5 | SpaceX"
            if '|' in raw:
                parts = raw.split('|')
                data['rocket'] = parts[0].strip()
                data['agency'] = parts[1].strip() if len(parts) > 1 else ''
            else:
                data['rocket'] = raw
                data['agency'] = ''
        if len(spans) >= 2:
            data['location'] = spans[1].text.strip()
        else:
            data['location'] = ''
    except:
        data['rocket'] = data['agency'] = data['location'] = ''
    try:
        # Date – using contains() to be robust
        date_elem = card.find_element(By.XPATH, ".//*[contains(@class,'text-sm') and contains(@class,'font-medium')]//span")
        data['date'] = date_elem.text.strip()
    except:
        data['date'] = ''
    try:
        # Status
        status_elem = card.find_element(By.XPATH, ".//div[contains(@class,'flex') and contains(@class,'gap-2')]//span[contains(@class,'text-xs')]")
        data['status'] = status_elem.text.strip()
    except:
        data['status'] = ''
    try:
        video_link = card.find_element(By.CSS_SELECTOR, "a[href*='youtube']")
        data['video_url'] = video_link.get_attribute('href')
    except:
        data['video_url'] = ''

    # Live progress info
    print(f"[{index}] {data.get('name', 'Unknown')} – {data.get('rocket', '?')} / {data.get('agency', '?')}")

    return data

def fetch_launches():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://nextspaceflight.com/launches/")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".grid.grid-cols-1.sm\\:grid-cols-2.xl\\:grid-cols-3.gap-8 > div")))
    scroll_until_end(driver)
    cards = driver.find_elements(By.CSS_SELECTOR, ".grid.grid-cols-1.sm\\:grid-cols-2.xl\\:grid-cols-3.gap-8 > div")
    total = len(cards)
    print(f"\nFound {total} launch cards. Parsing...\n")
    launches = []
    for idx, card in enumerate(cards, start=1):
        launches.append(parse_launch_card(card, idx))
    driver.quit()
    return launches

if __name__ == "__main__":
    os.makedirs('data', exist_ok=True)
    data = fetch_launches()
    with open('data/launches.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'rocket', 'agency', 'location', 'date', 'status', 'video_url', 'image_url'])
        writer.writeheader()
        writer.writerows(data)
    print(f"\nSaved {len(data)} launches to data/launches.csv")