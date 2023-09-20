from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import time


def test_login_and_purchase_places(validate_club):
    driver = webdriver.Chrome()

    # navigate to initial url
    app_url = "http://127.0.0.1:5000/"
    driver.get(app_url)

    # enter email and press enter
    input_box = driver.find_element(By.NAME, 'email')
    input_box.send_keys(validate_club['email'])
    time.sleep(2)
    input_box.send_keys(Keys.RETURN)
    time.sleep(2)

    # welcome page, find book places hyperlink and click
    click_button = driver.find_element(By.XPATH, '/html/body/ul/li[1]/a')
    click_button.click()
    time.sleep(2)

    # book one place
    input_box = driver.find_element(By.NAME, 'places')
    input_box.send_keys(1)
    time.sleep(2)
    input_box.send_keys(Keys.RETURN)
    time.sleep(2)

    driver.quit()
