# Библиотеки распознавания и синтеза речи
import speech_recognition as sr
from gtts import gTTS

# Воспроизведение речи
import pygame
from pygame import mixer

mixer.init()

import os
import sys
import time
import datetime
import logging
import webbrowser
import subprocess


class Speech_AI:

    def __init__(self):
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()

        now_time = datetime.datetime.now()
        self._mp3_name = now_time.strftime("%d%m%Y%I%M%S") + ".mp3"
        self._mp3_nameold = '111'

    def work(self):
        print("Минутку тишины, пожалуйста...")
        with self._microphone as source:
            self._recognizer.adjust_for_ambient_noise(source)

        try:
            while True:
                print("Скажи что - нибудь!")
                with self._microphone as source:
                    audio = self._recognizer.listen(source)
                print("Понял, идет распознавание...")
                try:
                    statement = self._recognizer.recognize_google(audio, language="ru_RU")
                    statement = statement.lower()

                    # Команды для открытия различных внешних приложений

                    if ((statement.find("калькулятор") != -1) or (statement.find("calculator") != -1)):
                        self.osrun('calc')

                    if ((statement.find("блокнот") != -1) or (statement.find("notepad") != -1)):
                        self.osrun('notepad')

                    if ((statement.find("paint") != -1) or (statement.find("паинт") != -1)):
                        self.osrun('mspaint')

                    if ((statement.find("browser") != -1) or (statement.find("браузер") != -1)):
                        self.openurl('http://google.ru', 'Открываю браузер')

                    # Команды для открытия URL в браузере

                    if (((statement.find("youtube") != -1) or (statement.find("youtub") != -1) or (
                            statement.find("ютуб") != -1) or (statement.find("you tube") != -1)) and (
                            statement.find("смотреть") == -1)):
                        self.openurl('http://youtube.com', 'Открываю ютуб')

                    if (((statement.find("новости") != -1) or (statement.find("новость") != -1) or (
                            statement.find("на усть") != -1)) and (
                            (statement.find("youtube") == -1) and (statement.find("youtub") != -1) and (
                            statement.find("ютуб") == -1) and (statement.find("you tube") == -1))):
                        self.openurl('https://www.youtube.com/user/rtrussian/videos', 'Открываю новости')

                    if ((statement.find("mail") != -1) or (statement.find("майл") != -1)):
                        self.openurl('https://e.mail.ru/messages/inbox/', 'Открываю почту')

                    if ((statement.find("вконтакте") != -1) or (statement.find("в контакте") != -1)):
                        self.openurl('http://vk.com', 'Открываю Вконтакте')

                    # Команды для поиска в сети интернет

                    if ((statement.find("найти") != -1) or (statement.find("поиск") != -1) or (
                            statement.find("найди") != -1) or (statement.find("дайте") != -1) or (
                            statement.find("mighty") != -1)):
                        statement = statement.replace('найди', '')
                        statement = statement.replace('найти', '')
                        statement = statement.strip()
                        self.openurl('https://yandex.ru/yandsearch?text=' + statement, "Я нашла следующие результаты")

                    if ((statement.find("смотреть") != -1) and (
                            (statement.find("фильм") != -1) or (statement.find("film") != -1))):
                        statement = statement.replace('посмотреть', '')
                        statement = statement.replace('смотреть', '')
                        statement = statement.replace('хочу', '')
                        statement = statement.replace('фильм', '')
                        statement = statement.replace('film', '')
                        statement = statement.strip()
                        self.openurl('https://yandex.ru/yandsearch?text=Смотреть+онлайн+фильм+' + statement,
                                     "Выберите сайт где смотреть фильм")

                    if (((statement.find("youtube") != -1) or (statement.find("ютуб") != -1) or (
                            statement.find("you tube") != -1)) and (statement.find("смотреть") != -1)):
                        statement = statement.replace('хочу', '')
                        statement = statement.replace('на ютубе', '')
                        statement = statement.replace('на ютуб', '')
                        statement = statement.replace('на youtube', '')
                        statement = statement.replace('на you tube', '')
                        statement = statement.replace('на youtub', '')
                        statement = statement.replace('youtube', '')
                        statement = statement.replace('ютуб', '')
                        statement = statement.replace('ютубе', '')
                        statement = statement.replace('посмотреть', '')
                        statement = statement.replace('смотреть', '')
                        statement = statement.strip()
                        self.openurl('http://www.youtube.com/results?search_query=' + statement, 'Ищу в ютуб')

                    if ((statement.find("слушать") != -1) and (statement.find("песн") != -1)):
                        statement = statement.replace('песню', '')
                        statement = statement.replace('песни', '')
                        statement = statement.replace('песня', '')
                        statement = statement.replace('песней', '')
                        statement = statement.replace('послушать', '')
                        statement = statement.replace('слушать', '')
                        statement = statement.replace('хочу', '')
                        statement = statement.strip()
                        self.openurl('https://my.mail.ru/music/search/' + statement, "Нажмите плэй")

                    # Поддержание диалога

                    if ((statement.find("до свидания") != -1) or (statement.find("досвидания") != -1)):
                        answer = "Пока!"
                        self.say(str(answer))
                        while pygame.mixer.music.get_busy():
                            time.sleep(0.1)
                        sys.exit()

                    print("Вы сказали: {}".format(statement))

                except sr.UnknownValueError:
                    print("Упс! Кажется, я тебя не поняла, повтори еще раз")
                except sr.RequestError as e:
                    print("Не могу получить данные от сервиса Google Speech Recognition; {0}".format(e))
        except KeyboardInterrupt:
            self._clean_up()
            print("Пока!")

    def osrun(self, cmd):
        PIPE = subprocess.PIPE
        p = subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=subprocess.STDOUT)

    def openurl(self, url, ans):
        webbrowser.open(url)
        self.say(str(ans))
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    def say(self, phrase):
        tts = gTTS(text=phrase, lang="ru")
        tts.save(self._mp3_name)

        # Play answer
        mixer.music.load(self._mp3_name)
        mixer.music.play()
        if (os.path.exists(self._mp3_nameold)):
            os.remove(self._mp3_nameold)

        now_time = datetime.datetime.now()
        self._mp3_nameold = self._mp3_name
        self._mp3_name = now_time.strftime("%d%m%Y%I%M%S") + ".mp3"

    def _clean_up(self):
        def clean_up():
            os.remove(self._mp3_name)


def main():
    ai = Speech_AI()
    ai.work()


main()
