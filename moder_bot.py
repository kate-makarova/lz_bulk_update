import json
import time

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ModerBot:
    def __init__(self):
        options = ChromeOptions()
     #   options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.page_load_strategy = 'eager'
        options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=options)
        settings = self.load_settings()
        self.address = settings["address"]
        self.keys = settings["keys"]
        self.user_list_pages = settings["user_list_pages"]

    def load_settings(self):
        with open('settings.json', 'r') as f:
            return json.load(f)

    def quit(self):
        self.driver.quit()

    def set_cookie(self):
        self.driver.get(self.address)
        for key in self.keys:
            self.driver.add_cookie(key)

    def find_interactable_element(self, by: str, selector: str):
        wait = WebDriverWait(self.driver, 10)
        elem = wait.until(EC.presence_of_element_located((by, selector)))

        # Scroll into view first — sometimes EC.element_to_be_clickable fails because it's off-screen
        self.driver.execute_script("arguments[0].scrollIntoView(true);", elem)
        time.sleep(0.2)  # give time for scroll animations

        elem = wait.until(EC.element_to_be_clickable((by, selector)))
        return elem

    def profile_field_update(self, profile_id, field_id, callback):
        self.driver.get(self.address + '/profile.php?section=fields&id=' + str(profile_id))
        try:
            field = self.find_interactable_element(By.CSS_SELECTOR, f"#profile8 #fld{field_id}")
        except TimeoutException:
            return False
        val = field.get_attribute("value")
        new_val = callback(val)
        field.clear()
        field.send_keys(new_val)
        button = self.find_interactable_element(By.NAME, 'update')
        button.click()
        time.sleep(1)
        return True

    def parse_user_list(self):
        for page in range(1, self.user_list_pages + 1):
            self.driver.get(self.address + f"/userlist.php?show_group=-1&sort_by=last_visit&sort_dir=DESC&username=-&p={page}")
            users = []
            elems = self.driver.find_elements(By.CSS_SELECTOR, 'span.usersname a')
            for elem in elems:
                parts = elem.get_attribute('href').split('id=')
                users.append((elem.text, parts[1]))
        return users


