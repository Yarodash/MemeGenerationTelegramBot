import random
import threading
import time

phrases = []

def getPhrase():
    return random.choice(phrases)

def reload():
    global phrases
    with open('MemeGen/phrases.txt', 'r') as file:
        phrases = [el for el in file.read().split('\n') if el]
    time.sleep(5)
    threading.Thread(target=reload).start()

threading.Thread(target=reload).start()

