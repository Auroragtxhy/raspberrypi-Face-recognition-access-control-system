# coding: utf-8
import sys
import os

DEBUG = True
os.environ['DEBUG'] = str(DEBUG)

app_name_en = 'rpi_facial_recognize'
app_name_cn = '树莓派人脸识别门禁系统'
author_name = '官腾'
author_org = '兰州理工大学'
app_version = 'V1.0.0'

base_dir = os.path.abspath(os.path.dirname(__file__))  # 返回.py文件的绝对路径
home_dir = os.path.expanduser('~')  # os.path.expanduser(path) 	把path中包含的"~"和"~user"转换成用户目录
app_config_fp = os.path.join(home_dir, 'qt.{}'.format(app_name_en))  # format函数、os.path.join组合路径

is_rpi = False  # 注意 这里 False 表示使用 usb 摄像头，True 表示使用 picamera
usb_camera = 0
baseUrl = "http://127.0.0.1:8911/face/submitFaceInfo"

person_dict = {
    'guanteng': '官腾',
    'yang_xin_cheng': '杨昕鋮',
    'zhang_ning_ning': '张宁宁',
    'xhy': '谢慧莹',
    'unKnown': '未知用户',
    }


log_file = os.path.join(base_dir, 'log.log')  # log文件路径
image_width = 1024
image_height = 768
