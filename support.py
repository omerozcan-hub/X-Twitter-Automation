import datetime
import os
import shutil
import time
from datetime import datetime, timedelta

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class support_login:

    def __init__(self, bot, email, password, username, wait):
        self.bot = bot
        self.email = email
        self.username = username
        self.passwd = password
        self.wait = wait

    # general
    def scroll_page(self):
        self.bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    def refresh(self):
        self.bot.refresh()
        time.sleep(5)

    def get_last_date_from_log(self, log_info_path):
        try:
            with open(log_info_path, 'r') as log_info:
                # Read last line of file
                current_date = datetime.now()
                lines = log_info.readlines()
                if lines:
                    last_line = lines[-1].strip()  # Clear spaces at the end of the line
                    file_name, last_date_str = last_line.split(' ',
                                                               1)  # Keep the part up to the first space as the file name, the rest as the date
                    log_last_date = datetime.strptime(last_date_str, "%Y-%m-%d %H:%M:%S")

                    #If the incoming date is older than the current date, the current live date is taken. In short, it is to prevent planning for old dates.
                    if log_last_date < datetime.now():
                        log_last_date = datetime.now()
                        #log_last_date = log_last_date.strftime("%Y-%m-%d %H:%M:%S.%f")

                    return log_last_date
                else:
                    current_date = current_date + timedelta(days=365)  # We find one year later by adding 365 days
                    #current_date_str = current_date.strftime("%Y-%m-%d %H:%M:%S.%f")
                    #current_date_str, millis = current_date_str.split('.')
                    print(f"Son log kaydı bulunamadı.\nPost {current_date_str} itibari ile planlandı.")
                    return current_date
        except Exception as e:
            print(f"Error get_last_date_from_log: {e}")
            return current_date

    def move_file_and_update_log(self,unposted_folder, file_name, start_datetime, logInfo_path):
        try:
            unposted_path = os.path.join(unposted_folder, file_name)
            posted_folder = os.path.dirname(unposted_folder)+"/Posted"
            posted_path = os.path.join(posted_folder, file_name)

            # move file
            shutil.move(unposted_path, posted_path)

            # saved infos to log file
            with open(logInfo_path, 'a') as logInfo:
                logInfo.write(f"{file_name} {start_datetime}\n")
        except Exception as e:
            print(f"Error move_file_and_update_log: {e}")

    # not work
    def get_hot_trends(self):
        try:
            self.bot.get("https://twitter.com/i/trends")
            time.sleep(2)
            # XPath'leri kullanarak elementleri bul ve beklet
            # CSS Selector kullanarak elementi bul

            trends_container = self.bot.find_element(By.CSS_SELECTOR, "[aria-label='Timeline: Trends']")
            print(1)

            # CSS Selector kullanarak altındaki elemanları bul
            trends = trends_container.find_elements(By.XPATH, "//span/span[@class='css-1qaijid r-bcqeeo r-qvutc0 r-poiln3']")

            print(2)

            trending_topics = [trend.text for trend in trends]
            print(3)
            print(trending_topics)
            self.bot.get("https://twitter.com/home")
            time.sleep(3)
            #return trending_topics
        except Exception as e:
            print(f"Error: {e}")

    def get_hashtag(self):
        return "#smile #fashion #instadaily #friends #food #instalike #selfie #nature #travel "

    # post
    def post_images(self, fpath, text, logInfo_path):
        image_folder_path = fpath
        image_files = [f for f in os.listdir(image_folder_path) if os.path.isfile(os.path.join(image_folder_path, f))]
        hashtags = self.get_hashtag()
        plan_datetime = self.get_last_date_from_log(logInfo_path)

        if len(image_files)<1:
            print("There is no file to post")

        try:
            with open(logInfo_path, 'a') as logInfo:
                for image_file in image_files:
                    file_path = os.path.join(image_folder_path, image_file)
                    plan_datetime = plan_datetime + timedelta(hours=1)

                    self.post_area_touch()
                    self.post_schedule(str(plan_datetime.year), str(plan_datetime.month), str(plan_datetime.day),
                                       str(plan_datetime.hour), str(plan_datetime.minute))
                    self.post_image(file_path,hashtags) # görseli ve metini yükler
                    self.post_submit() # postu gönder
                    self.refresh()

                    self.move_file_and_update_log(fpath, image_file, plan_datetime, logInfo_path)
        except Exception as e:
            print(f"Error post_images: {e}")

    def post_schedule(self, year, month, day, hour, minute):
        try:
            #open schedule selector
            element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@data-testid="scheduleOption"]'))
            )
            element.click()
            time.sleep(1)

            #set date
            month_select = Select(self.bot.find_element(By.ID,"SELECTOR_1"))
            month_select.select_by_value(month) #1-12

            day_select = Select(self.bot.find_element(By.ID, "SELECTOR_2"))
            day_select.select_by_value(day) #1-30

            year_select = Select(self.bot.find_element(By.ID, "SELECTOR_3"))
            year_select.select_by_value(year) #2024-2026

            #set time
            hour_select = Select(self.bot.find_element(By.ID,"SELECTOR_4"))
            hour_select.select_by_value(hour) #0-23

            minute_select = Select(self.bot.find_element(By.ID,"SELECTOR_5"))
            minute_select.select_by_value(minute) #0-59

            button_confirm = self.bot.find_element(By.XPATH, "//span[text()='Confirm']")
            button_confirm.click()
            #time.sleep(1)

        except Exception as e:
            print(f"Error post_schedule: {e}")

    def post_text(self,text):
        try:
            input_text = self.bot.find_element(By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')
            input_text.send_keys(text)
        except Exception as e:
            print(f"Error post_text: {e}")

    def post_image(self, path_of_image, text):
        try:

            if text:
                self.post_text(text)

            image_path = path_of_image
            input_element = self.bot.find_element(By.CSS_SELECTOR, 'input[type="file"]')
            input_element.send_keys(image_path)
            time.sleep(1)
        except Exception as e:
            print(f"Error post_image: {e}")

    def post_area_touch(self):
        try:
            button_text_area = self.bot.find_element(By.XPATH,
                                                     "//div[@data-testid='tweetTextarea_0RichTextInputContainer']")
            button_text_area.click()
        except Exception as e:
            print(f"Error post_area_touch: {e}")

    def post_submit(self):
        try:
            button_submit = self.bot.find_element(By.CSS_SELECTOR, "div[data-testid='tweetButtonInline']")
            button_submit.click()
            time.sleep(3)
        except Exception as e:
            print(f"Error post_submit: {e}")


    # login
    def enter_email(self):
        self.bot.get("https://twitter.com/i/flow/login")
        time.sleep(5)

        try:
            input_email = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
            #self.bot.find_element(By.TAG_NAME, "input")
            input_email.clear()
            input_email.send_keys(self.email)
            self.click_next_button()
        except TimeoutException:
            print("Element not found or timed out.")

    def handle_unusual_activity(self):
        try:
            suspect = self.bot.find_elements(By.CSS_SELECTOR, "[data-testid='ocfEnterTextTextInput']")
            # If suspicious elements are found, this will be done
            if suspect:
                usern = self.bot.find_element(By.CSS_SELECTOR, "input[data-testid='ocfEnterTextTextInput']")
                usern.clear()
                usern.send_keys(self.username)
                time.sleep(2)
                self.click_next_button()
        except Exception as e:
            print(f"Error: {e}")

    def enter_password(self):
        try:
            input_passwd = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
            )
            #self.bot.find_element(By.CSS_SELECTOR, "input[name='password']")
            input_passwd.clear()
            input_passwd.send_keys(self.passwd)
            self.click_login_button()
        except NoSuchElementException as e:
            print(f"Error: {e}")


    def click_next_button(self):
        try:
            ileri_button = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//span[text()='İleri']"))
            )
            ileri_button.click()
            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")

    def click_login_button(self):
        try:
            giris_yap_buton = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//span[text()='Giriş yap']"))
            )
            giris_yap_buton.click()
            time.sleep(5)
        except Exception as e:
            print(f"Error: {e}")

    # logout from account
    def to_logout(self):
        self.bot.get("https://twitter.com/home")
        time.sleep(4)

        try:
            three_dot_button = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-testid='SideNav_AccountSwitcher_Button']")))
            three_dot_button.click()
            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")

        try:
            button_logout = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-testid='AccountSwitcher_Logout_Button']")))
            button_logout.click()
            time.sleep(1)
            self.bot.quit()
            print("Mission completed.\nBrowser closed")
        except Exception as e:
            print(f"Error: {e}")

