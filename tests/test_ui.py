from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_ui_form_submit():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Remote(
        command_executor="http://localhost:4444/wd/hub",
        options=options
    )
    driver.get("http://127.0.0.1:5000/")
    search_box = driver.find_element(By.NAME, "search")
    search_box.send_keys("hello")
    driver.find_element(By.TAG_NAME, "form").submit()
    time.sleep(1)
    assert "You searched for: hello" in driver.page_source
    driver.quit()
