import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class Bot:
    def __init__(self):
        self._driver = webdriver.Chrome(ChromeDriverManager().install())
        self._url = "https://splinterlands.com/?p=battle_history"
        self._username = "jseveno.piltant@gmail.com"
        self._password = "LZ6oXLmx"
        self._launch_battle_id = "battle_category_btn"

    def open(self, url):
        self._driver.get(url)

    def click(self, element):
        self._driver.execute_script("arguments[0].click()", element)

    def start_battle(self):
        self._driver.find_element(By.ID, self._launch_battle_id).click()

    def get_element_by(self, by, tag):
        return WebDriverWait(self._driver, 10).until(
            EC.presence_of_element_located((by, tag))
        )

    def login(self):
        self.get_element_by(By.CLASS_NAME, "navbar-toggle").click()
        self._driver.execute_script("SM.ShowLogin(SM.ShowAbout);")
        username_input = self.get_element_by(By.ID, "email")
        self._driver.execute_script(f"arguments[0].value = '{self._username}'", username_input)
        password_input = self.get_element_by(By.ID, "password")
        self._driver.execute_script(f"arguments[0].value = '{self._password}'", password_input)
        time.sleep(5)
        self.get_element_by(By.NAME, "emailPwLogin").submit()
        time.sleep(3)
        self.click(self.get_element_by(By.CLASS_NAME, "close"))
        time.sleep(3)
        self.click(self.get_element_by(By.CLASS_NAME, "play-now-btn"))
        time.sleep(3)
        self.click(self.get_element_by(By.ID, "battle_category_btn"))
        time.sleep(15)
        self.click(self.get_element_by(By.CLASS_NAME, "btn--create-team"))

    def run(self, engine):
        self.open(self._url)
        self.login()
