# coding: utf8
import threading
import time
import speech_recognition as sr
from model import ServoAcrobat, ServoController

class STT():
    def __init__(self, servo_acrobat: ServoAcrobat, servo_controller: ServoController) -> None:
        self.r = sr.Recognizer() 
        self.pause = False
        self.get_text_thread_running = True
        self.get_text_thread = threading.Thread(target=self.get_text)
        self.get_text_thread.start()
        self.s2t_text = ''
        self.servo_acrobat = servo_acrobat
        self.servo_controller = servo_controller

    def get_text(self):
        try:
            with sr.Microphone() as source2:
                self.r.adjust_for_ambient_noise(source2, duration=4)
                while True:
                    audio2 = self.r.listen(source2, phrase_time_limit=5)
                    try:
                        MyText = self.r.recognize_google(audio2, language='pl-PL', pfilter=1)
                        self.s2t_text = MyText
                        self.handle_text(self.s2t_text)
                    except sr.UnknownValueError:
                        print("Nie rozpoznano mowy, dawaj dalej!")
                        self.s2t_text = ""
                    if(self.s2t_text == "stop"): break
                    if not self.get_text_thread_running :
                        print("get_text_thread stoped")
                        break
        except sr.RequestError as e:
            print(f"Could not request results: {e} ")
        except sr.UnknownValueError:
            print("unknown error occurred")

    def close_thread(self):
        self.get_text_thread_running = False
        self.get_text_thread.join()

    def set_language(self, language: str) -> None:
        self.pause = True
        if(language == "us"):
            self.pause = False
        elif(language == "pl"):
            self.pause = False
        elif(language == "cs"):
            self.pause = False
        else:
            raise Exception("Language not supported")
        

    def handle_text(self, text: str) -> None:
        if "robot" in text:
            if "chodź" in text:
                #self.servo_controller.move([1, 2, 3, 4, 5, 6], [1000, 2300, 1200, 1700, 700, 2000], [2000, 2000, 2000, 2000, 2000, 2000])
                self.servo_acrobat.move_to_position("hands", 1000)
                time.sleep(2)
                self.servo_acrobat.move_to_position("no1_x", 1000)
                for i in range(3):
                    self.servo_acrobat.move_to_position("no2_x", 1000)
                    self.servo_acrobat.move_to_position("no3_x", 200)
                    self.servo_acrobat.move_to_position("no4_x", 500)
                    self.servo_acrobat.move_to_position("no5_x", 100)
                    self.servo_acrobat.move_to_position("no6_x", 1000)
                    self.servo_acrobat.move_to_position("no7_x", 200)
                    self.servo_acrobat.move_to_position("no8_x", 100)
                    self.servo_acrobat.move_to_position("no9_x", 150)
                    self.servo_acrobat.move_to_position("no10_x", 500)
                    self.servo_acrobat.move_to_position("no11_x", 400)
                    self.servo_acrobat.move_to_position("no12_x", 500)
                    self.servo_acrobat.move_to_position("no13_x", 1000)
                self.servo_acrobat.move_to_position("no2_x", 1200)
                self.servo_acrobat.move_to_position("no1_x", 1000)

            if "pomachaj" in text or "Pomachaj" in text:
                # pr', 'mach2', 'mach1', 'mach2', 'mach1', 'mach2', 'pr']
                self.servo_acrobat.move_to_position("mach1", 1000)
                self.servo_acrobat.move_to_position("mach2", 1000)
                self.servo_acrobat.move_to_position("hands", 1500)

            
