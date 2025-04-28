# * Gavin's Code *

from selenium import webdriver
import time

def test_home_page_load():

    driver = webdriver.Chrome() # Makes sure webdriver is installed - and the purpose of this is to ensure home page loads correctly
    driver.get("http://127.0.0.1:5000") # Open the app URL associated with our system
    time.sleep(2.5)  # Allows the entire page to load
    assert "Komodo Hub" in driver.title # Validates the page title
    driver.quit() # Closes the browser

def test_login_redirect():
    # Tests the login redirect directly 
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000") # URL page
    loginRedirectButton = driver.find_element("link text", "Login") # Finds the UI with the login button
    loginRedirectButton.click()
    time.sleep(2) # Allows the page to load
    assert "Login" in driver.title # Ensures the login page loads
    driver.quit() # Exit to move on

def test_register_redirect():
    # Tests the register redirect directly 
    driver = webdriver.Chrome() 
    driver.get("http://127.0.0.1:5000") # Opens the home page first
    registerRedirectButton = driver.find_element("link text", "Register") # Finds the UI with the register/signup button
    registerRedirectButton.click() # Clicks the button
    time.sleep(2.5) # Allows again 2 seconds for the page to load
    assert "Signup" in driver.title, f"Expected 'Signup' in page title, but got '{driver.title}'"
    driver.quit() # Close the browser after test has been completed 
