import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import subprocess
import asyncio
from pyppeteer import launch



opts = {
    'alias': ('Валентина', 'Валя', 'Неваляшка', 'Валюха', 'Валь', 'Карданный вал', 'Распредвал', 'Червячный вал', ''),
    'tbr': ('скажи', 'глаголь', 'заебала', 'расскажи', 'сколько', 'покажи', 'тварь', 'открой'),
    'cmds': {
        'ctime': ('текущее время', 'сейчас времени', 'который час', ),
        'music': ('включи музыку', 'бахни музла', 'хочу трэки'),
        'pycharm': ('пайчарм', 'пичарм', 'писюн', 'pycharm'),
        'webstorm': ('вэбшторм', 'шторм', 'webstorm'),
        'file': ('блокнот', 'текстовик'),
        'google': ('гугл', 'google', 'поиск')
    }
}


def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language='ru-RU').lower()
        print('[Log message] - Распознано |-->' + voice)

        if voice.startswith(opts['alias']):
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, '').strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, '').strip()

            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        speak('Нихуя не понял')
        print('[Log message] - Голос не распознан!')
    except sr.RequestError as e:
        speak('Подключись деган')
        print('[Log message] - Проверьте подключение к интернету!')


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 60}
    for c,v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == 'ctime':
        now = datetime.datetime.now()
        speak('Cейчас ' + str(now.hour) + ':' + str(now.minute))
    elif cmd == 'music':
        speak('Нехуй петь')
        os.system("C:\\Users\\Santanyan\\Downloads\\Telegram Desktop\\Growl - Mushrooms.mp3")
    elif cmd == 'webstorm':
        speak('Заебал кодить, иди потрахайся')
        subprocess.Popen(['C:\\Program Files\\JetBrains\\WebStorm 2019.2.3\\bin\\webstorm64.exe'])
    elif cmd == 'pycharm':
        speak('Заебал кодить, иди потрахайся')
        subprocess.Popen(['C:\\Program Files\\JetBrains\\PyCharm 2019.2.4\\bin\\pycharm64.exe'])
    elif cmd == 'file':
        speak('Обстрочись')
        subprocess.Popen(['C:\\Windows\\notepad.exe'])
    elif cmd == 'google':
        asyncio.get_event_loop().run_until_complete(openBrowser('http://www.google.com'))
    else:
        speak('Команда - дерьмо, если чесно!')
        print('Команда - дерьмо, если чесно!')


async def openBrowser(url):
    browser = await launch(headless=False)
    await browser
    page = await browser.newPage()
    await page.setViewport({'width': 1920, 'height': 1080})
    await page.goto(url)


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

        try:
            callback(r, audio)
        except Exception as e:
            print("Exception: " + str(e))


speak_engine = pyttsx3.init()

voices = speak_engine.getProperty('voices')
# speak_engine.setProperty('voice', voices[''])

speak('Хало кучерявый')
speak('Базарь')

while True:
    get_audio()
