from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time

class speech_2_text():
    def __init__(self):
        browserDIR = "/tmp/.org.chromium.Chromium.0sEz4a/Default"
        webdriverDIR = "/usr/lib/chromium-browser/chromedriver"
        # C:\Users\Shinken\AppData\Local\Google\Chrome\User Data\Default
        options = Options()
        options.add_argument(browserDIR)
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
        })
        service = Service(webdriverDIR)
        self.stt = webdriver.Chrome(webdriverDIR, options=options)
        self.stt.get('https://dictation.io/speech')
        self.stt.minimize_window()
        select = Select(self.stt.find_element("xpath", "//select[@id='lang']"))
        select.select_by_value('pl-pl')
        time.sleep(1)
        self.stt.find_element("xpath", "//a[@class='btn-mic btn btn--primary-1']").click()
        time.sleep(5)
        self.textbox = self.stt.find_element("xpath", "//div[@class='ql-editor ql-blank']")
        self.get_text()

    def get_text(self):
        while True:
            if self.textbox.text != '':
                if self.textbox.text.strip() == 'koniec':
                    self.textbox.clear()
                    self.stt.quit()
                    print('Koniec1')
                    exit()
                print(self.textbox.text)
                self.textbox.clear()

# self.stt.quit()
