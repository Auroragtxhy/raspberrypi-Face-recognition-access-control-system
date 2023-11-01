# coding utf-8

import config
if config.is_rpi:  # LED灯指示状态
    import RPi.GPIO as GPIO   # 导入树梅派提供的python模块

from time import sleep   # 导入时间包，用于控制闪烁

# 表示程序正常運行
# def LED_program_running():
#
#     GPIO.setmode(GPIO.BCM) #设置GPIO模式，BCM模式在所有的树莓派中通用
#     如果RPi.GPIO检测到一个引脚已经被设置成了非默认值，那么你将看到一个警告信息
#     GPIO.setwarnings(False) #禁用警告
#     GPIO.setup(24,GPIO.OUT) #设置GPIO 18 为输出
#
#     GPIO.output(24,GPIO.HIGH)  #GPIO 18输出3.3v 输出高电平 LED灯亮
#     sleep(2) #程序控制流程睡眠1秒
#     GPIO.output(24,GPIO.LOW)   #GPIO 18输出低电平 LED灯灭
#     sleep(2)
#
#     GPIO.cleanup()  #释放掉脚本中使用的GPIO引脚。并会清除设置的引脚编号规则


def LED_recognized_successful():
    """表示人脸识别成功"""
    if not config.is_rpi:
        print('人脸识别成功, LED 操作')
        return
    GPIO.setmode(GPIO.BCM)  # 设置GPIO模式，BCM模式在所有的树莓派中通用
    # 如果RPi.GPIO检测到一个引脚已经被设置成了非默认值，那么你将看到一个警告信息
    GPIO.setwarnings(False)  # 禁用警告
    GPIO.setup(23,GPIO.OUT)  # 设置GPIO 16 为输出

    GPIO.output(23,GPIO.HIGH)  # GPIO 16输出3.3v 输出高电平 LED灯亮
    sleep(2) # 程序控制流程睡眠1秒
    GPIO.output(23,GPIO.LOW)   # GPIO 16输出低电平 LED灯灭
    # sleep(1)

    # GPIO.cleanup()  # 释放掉脚本中使用的GPIO引脚。并会清除设置的引脚编号规则


def LED_recognition_error():
    """表示人脸识别错误"""
    if not config.is_rpi:
        print('人脸识别错误, LED 操作')
        return
    GPIO.setmode(GPIO.BCM)  # 设置GPIO模式，BCM模式在所有的树莓派中通用
    # 如果RPi.GPIO检测到一个引脚已经被设置成了非默认值，那么你将看到一个警告信息
    GPIO.setwarnings(False)  # 禁用警告
    GPIO.setup(12,GPIO.OUT)  # 设置GPIO 32为输出

    GPIO.output(12,GPIO.HIGH)  # GPIO 32输出3.3v 输出高电平 LED灯亮
    sleep(2)  # 程序控制流程睡眠1秒
    GPIO.output(12,GPIO.LOW)   # GPIO 32输出低电平 LED灯灭
    # sleep(1)

    # GPIO.cleanup()  #释放掉脚本中使用的GPIO引脚。并会清除设置的引脚编号规则
# while True:
    # LED_program_running()
    

    
    
