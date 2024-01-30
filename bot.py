import time
from support import support_login

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class Bot(support_login):

    def __init__(self,email,password,username):
        # constant datas
        self.is_logged_in = False
        self.botProfile = webdriver.ChromeOptions()
        self.botProfile.add_experimental_option('prefs', {'intl.accept_languages': 'tr,tr_TR'})
        self.bot = webdriver.Chrome(options=self.botProfile)
        self.wait = WebDriverWait(self.bot, 10)
        super().__init__(self.bot, email, password, username, self.wait)

    def post_multiple_image(self, path, text, logInfo_path):
        # klasör dizini / post metini / planlamaya başlangıç tarihi(2024-03-01 14:22:00)
        self.post_images(path, text, logInfo_path)

    def post_planned_image(self,path, text):
        self.post_area_touch()
        self.post_image(path, text)
        self.post_schedule("2024", "1", "24", "11", "30")
        self.post_submit()

    def post_a_text(self):
        self.post_area_touch()
        self.post_text()
        self.post_submit()

    def post_a_image(self, path, text):
        self.post_area_touch()
        self.post_image(path, text) # also you can add a text
        self.post_submit()

    def post_planned_text(self):
        self.post_area_touch()
        self.post_text("Hi, this is a first planned post")
        self.post_schedule("2024", "1", "24", "11", "30")
        self.post_submit()

    def login(self):
        self.enter_email()
        self.handle_unusual_activity()
        self.enter_password()
        self.is_logged_in=True

    def logout(self):
        self.to_logout()

