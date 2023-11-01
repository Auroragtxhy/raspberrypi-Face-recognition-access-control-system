# coding: utf-8
import config

if config.is_rpi:
    import RPi.GPIO as GPIO

# 信号灯管脚定义
GPIO_IN_PIN22 = 25  # 中断输入管脚变量，22脚


def init_gpio():
    if not config.is_rpi:
        print('初始化GPIO')
        return
    GPIO.setmode(GPIO.BCM)  # 设置GPIO模式，BCM模式在所有的树莓派中通用
    GPIO.setwarnings(False)  # 禁用警告
    # GPIO.setup(24,GPIO.OUT) #设置GPIO 18 为输出，该脚表示人脸识别正在运行
    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 中断输入管脚


def start_scan():
    if not config.is_rpi:
        print('设置GPIO')
        return
    GPIO.setmode(GPIO.BCM)  # 设置GPIO模式，BCM模式在所有的树莓派中通用
    GPIO.setwarnings(False)  # 禁用警告
    GPIO.setup(24, GPIO.OUT)  # 设置GPIO 18 为输出，该脚表示人脸识别正在运行
    GPIO.setup(21, GPIO.OUT)

    GPIO.output(21, GPIO.LOW)  # 黄灯灭
    GPIO.output(24, GPIO.HIGH)  # 蓝灯亮


def finished_scan():
    if not config.is_rpi:
        print('恢复GPIO')
        return
    GPIO.setmode(GPIO.BCM)  # 设置GPIO模式，BCM模式在所有的树莓派中通用
    GPIO.setwarnings(False)  # 禁用警告
    GPIO.setup(24, GPIO.OUT)  # 设置GPIO 18 为输出，该脚表示人脸识别正在运行
    GPIO.setup(21, GPIO.OUT)
    GPIO.output(24, GPIO.LOW)  # 蓝灯灭
    GPIO.output(21, GPIO.HIGH)  # 黄灯亮


# 绑定中断函数
def setup_switch(func):
    if not config.is_rpi:
        print('setup_switch')
        return
    GPIO.setmode(GPIO.BCM)  # 设置GPIO模式，BCM模式在所有的树莓派中通用
    GPIO.setwarnings(False)  # 禁用警告
    GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 中断输入管脚
    GPIO.add_event_detect(GPIO_IN_PIN22, GPIO.FALLING, callback=func, bouncetime=150)


# 待机模式，没有执行任何操作
def read_mode():
    if not config.is_rpi:
        print('read_mode')
        return
    GPIO.setmode(GPIO.BCM)  # 设置GPIO模式，BCM模式在所有的树莓派中通用
    GPIO.setwarnings(False)  # 禁用警告
    GPIO.setup(21, GPIO.OUT)
    GPIO.output(21, GPIO.HIGH)  # 黄灯亮
