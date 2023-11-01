# utf-8
import os
import pygame
import time

voice_map = {'即将开始识别': 'audio/01.mp3',
             '没有检测到人脸': 'audio/02.mp3',
             '人脸不匹配': 'audio/03.mp3',
             '识别成功': 'audio/04.mp3', }


def will_start_to_recognize():
    pygame.mixer.init()
    pygame.mixer.music.load(voice_map['即将开始识别'])
    pygame.mixer.music.play()
    # time.sleep(5)


def no_face_detected():
    pygame.mixer.init()
    pygame.mixer.music.load(voice_map['没有检测到人脸'])
    pygame.mixer.music.play()
    time.sleep(5)


def face_mismatch():
    pygame.mixer.init()
    pygame.mixer.music.load(voice_map['人脸不匹配'])
    pygame.mixer.music.play()
    time.sleep(5)


def recognized_successful():
    pygame.mixer.init()
    pygame.mixer.music.load(voice_map['识别成功'])
    pygame.mixer.music.play()
    time.sleep(5)


if __name__ == '__main__':
    print(voice_map['识别成功'])
    fp = os.path.abspath(voice_map['识别成功'])
    print(fp)
    print(os.path.exists(voice_map['识别成功']))
    recognized_successful()
