import json
import os
import time
import threading

class Settings:
    def __init__(self, standart_setting, setting_name):
        self.data = {}
        self.standart_setting = standart_setting
        self.file = setting_name
        self.load()
        threading.Thread(target=self.mainloop).start()

    def load(self):
        if os.path.exists('Settings\\'+self.file+'.txt'):
            with open('Settings\\'+self.file+'.txt', 'r') as file:
                self.data = json.loads(file.read() or '{}')

    def save(self):
        with open('Settings\\'+self.file+'.txt', 'w') as file:
            print(json.dumps(self.data), file=file)

    def add(self, chat_id, setting):
        self.data[str(chat_id)] = setting
        
    def get(self, chat_id):
        return self.data[str(chat_id)] if str(chat_id) in self.data else self.standart_setting

    def mainloop(self):
        self.save()
        time.sleep(5)
        threading.Thread(target=self.mainloop).start()

place = Settings('on_image', 'data_place')
font = Settings('impact', 'data_font')
