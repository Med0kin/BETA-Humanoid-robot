# coding: utf8
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time


browserDIR = "--user-data-dir=/home/pi/.config/chromium/Default"
webdriverDIR = "/usr/lib/chromium-browser/chromedriver"
# C:\Users\Shinken\AppData\Local\Google\Chrome\User Data\Default
options = Options()
options.add_argument(browserDIR)
options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
  })
service = Service(webdriverDIR)
stt = webdriver.Chrome(webdriverDIR, options=options)
stt.get('https://smodin.io/pl/przemowienie-do-tekst-i-tekst-do-przemowienie')
stt.minimize_window()
stt.find_element("xpath", "//button[normalize-space()='Mowa na tekst']").click()
stt.find_element("xpath", "//body/div[@id='__next']/div[2]/div[1]/div[1]/div[2]/div[2]/button[1]/span[1]").click()
time.sleep(5)
textbox = stt.find_element("xpath", "//textarea[contains(@placeholder,'Naciśnij przycisk i zacznij mówić')]")
clear = stt.find_element("xpath", "//span[@data-text='Kasować']//button//span").click

while True:
    if textbox.text != '':
        if textbox.text.strip() == 'koniec':
            clear()
            stt.quit() ################ WAZNE !!!!!!!! ################
            print('Koniec1')
            exit()
        print(textbox.text)
        clear()
