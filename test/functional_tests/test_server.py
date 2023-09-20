from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import time


def test_login_selenium(validate_club):
    driver = webdriver.Firefox()

    # navigate to initial url
    app_url = "http://127.0.0.1:5000/"
    driver.get(app_url)

    # enter email and press enter
    input_box = driver.find_element(By.NAME, "email")
    input_box.send_keys(validate_club['email'])
    time.sleep(2)
    input_box.send_keys(Keys.RETURN)
    time.sleep(5)

    # # navigate to welcome page
    # welcome_page_url = driver.current_url
    # driver.get(welcome_page_url)
    # time.sleep(2)
    # click_button = driver.find_element(By.XPATH, '/html/body/ul[2]/li[2]/a')
    # # click_button.click()
    # time.sleep(5)
    # print(click_button)
    # print(driver.current_url)

    driver.quit()
