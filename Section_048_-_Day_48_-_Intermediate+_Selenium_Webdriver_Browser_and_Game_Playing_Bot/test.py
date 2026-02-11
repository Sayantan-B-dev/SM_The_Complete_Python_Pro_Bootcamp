from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)


driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.amazon.com")


# Find the search bar
t1 = driver.find_element(By.ID, "twotabsearchtextbox")
t1.send_keys("Python", Keys.ENTER)

# Find the first result
t2 = driver.find_element(By.ID, "result_0")

# Click the first result
t3 = driver.find_element(By.LINK_TEXT, "Python Crash Course, 3rd Edition")
t3.click()

# Find the price
t4 = driver.find_element(By.ID, "priceblock_ourprice")

print(t4.text)


# Close the browser
driver.close()
driver.quit()