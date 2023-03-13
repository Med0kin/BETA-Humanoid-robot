from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time


browserDIR = "/tmp/.org.chromium.Chromium.0sEz4a/Default"
webdriverDIR = "/usr/lib/chromium-browser/chromedriver"
# C:\Users\Shinken\AppData\Local\Google\Chrome\User Data\Default
options = Options()
options.add_argument(browserDIR)
options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
  })
service = Service(webdriverDIR)
stt = webdriver.Chrome(webdriverDIR, options=options)
stt.get('https://dictation.io/speech')
stt.minimize_window()
select = Select(stt.find_element("xpath", "//select[@id='lang']"))
select.select_by_value('pl-pl')
time.sleep(1)
stt.find_element("xpath", "//a[@class='btn-mic btn btn--primary-1']").click()
time.sleep(5)
textbox = stt.find_element("xpath", "//div[@class='ql-editor ql-blank']")


while True:
    if textbox.text != '':
        if textbox.text.strip() == 'koniec':
            textbox.clear()
            stt.quit()
            print('Koniec1')
            exit()
        print(textbox.text)
        textbox.clear()

# stt.quit()
