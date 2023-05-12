# coding: utf8
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time

class speech_to_text():
    def __init__(self):
        browserDIR = "--user-data-dir=/home/pi/.config/chromium/Default"
        webdriverDIR = "/usr/lib/chromium-browser/chromedriver"
        chromium_version = "92.0.4515.98"
        # C:\Users\Shinken\AppData\Local\Google\Chrome\User Data\Default
        options = Options()
        options.add_argument(browserDIR)
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
        })
        service = Service(ChromeDriverManager(version=chromium_version).install())
        self.stt = webdriver.Chrome(ChromeDriverManager(version=chromium_version).install(), options=options)
        # service = Service(webdriverDIR)
        # self.stt = webdriver.Chrome(webdriverDIR, options=options)
        self.stt.get('https://smodin.io/pl/przemowienie-do-tekst-i-tekst-do-przemowienie')
        self.stt.minimize_window()
        self.stt.find_element("xpath", "//button[normalize-space()='Mowa na tekst']").click()
        time.sleep(2)
        self.stt.find_element("xpath", "//body/div[@id='__next']/div[3]/div[1]/div[1]/div[2]/div[2]/button[1]/span[1]").click()
        time.sleep(2)
        self.textbox = self.stt.find_element("xpath", "//textarea[contains(@placeholder,'Naciśnij przycisk i zacznij mówić')]")
        self.clear = self.stt.find_element("xpath", "//span[@data-text='Kasować']//button//span").click
        self.get_text_thread_running = True
        self.get_text_thread = threading.Thread(target=self.get_text)
        self.get_text_thread.start()
        self.s2t_text = ''


    def get_text(self):
        while True:
            if self.textbox.text != '':
                print(self.textbox.text)
                self.s2t_text = self.textbox.text
                self.clear()
            if self.get_text_thread_running == False:
                print("get_text_thread stoped")
                break
    def close_thread(self):
        self.stt.quit()
        self.get_text_thread_running = False
        self.get_text_thread.join()

