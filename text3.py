# utf-8
# _*_author-GT_*_
# 基于树莓派的人脸识别门禁系统
# 基于百度API的人脸识别
from aip import AipFace
from picamera import PiCamera
import urllib.request
import RPi.GPIO as GPIO
import base64
import time

from bluetooth_text import bt_open, bt_close, servo_init
from led3 import LED_recognized_successful, LED_recognition_error
from servecha import getmessages1, getmessages2, getmessages3
from voice import will_start_to_recognize, no_face_detected, face_mismatch, recognized_successful

# 百度人脸时别API帐号
APP_ID = '23748600'
API_KEY = '8oLKV0GqmGW6DAO2qkgWXB2c'
SECRET_KEY = 'h2PRloq3CRt23izsYkO43lGZhdcry2EG'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)  # 创建一个客户端用以访问百度云
# 图像编码方式
IMAGE_TYPE = 'BASE64'
camera = PiCamera()  # 定义一个摄像头对象
# 用户组
GROUP = 'GT_01'

# 信号灯管脚定义
GPIO_IN_PIN22 = 25  # 中断输入管脚变量，22脚
ledStatus = True
GPIO.setmode(GPIO.BCM)  # 设置GPIO模式，BCM模式在所有的树莓派中通用
# 如果RPi.GPIO检测到一个引脚已经被设置成了非默认值，那么你将看到一个警告信息
GPIO.setwarnings(False)  # 禁用警告
# GPIO.setup(24,GPIO.OUT) # 设置GPIO 18 为输出，该脚表示人脸识别正在运行
GPIO.setup(21, GPIO.OUT)  # 设置GPIO 40 为输出,该脚表示等待中断
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 中断输入管脚


# 照相函数
def getimage():
    camera.resolution = (1024, 768)  # 摄像界面为1024*768
    camera.start_preview()  # 开始摄像
    time.sleep(2)
    camera.capture('faceimage.jpg')  # 拍照并保存
    time.sleep(2)


#  对图片的格式进行转换
def transimage():
    f = open('faceimage.jpg', 'rb')
    img = base64.b64encode(f.read())
    return img


# 上传到百度api进行人脸检测,此处参考百度文档
def go_api(image):
    result = client.search(str(image, 'utf-8'), IMAGE_TYPE, GROUP)  # 在百度云人脸库中寻找有没有匹配的人脸
    if result['error_msg'] == 'SUCCESS':  # 如果成功了
        name = result['result']['user_list'][0]['user_id']  # 获取名字
        score = result['result']['user_list'][0]['score']  # 获取相似度
        if score > 80:  # 如果相似度大于80
            if name == 'guanteng':
                print("欢迎%s !" % name)
                getmessages1()
                time.sleep(1)
            if name == 'yang_xin_cheng':
                print("欢迎%s !" % name)
                getmessages3()
                time.sleep(1)
            if name == "yusheng_02":
                print("欢迎%s !" % name)
                time.sleep(1)
            if name == "tanwenjie":
                print("欢迎%s !" % name)
        else:
            print("对不起，我不认识你！")
            name = 'Unknow'
            return 0
        curren_time = time.asctime(time.localtime(time.time()))  # 获取当前时间
        # 将人员出入的记录保存到log.txt中
        f = open('Log.txt', 'a')
        f.write("Person: " + name + "     " + "Time:" + str(curren_time) + '\n')
        f.close()
        return 1
    if result['error_msg'] == 'pic not has face':
        print('检测不到人脸')
        time.sleep(3)
        return -1
    else:
        print(result['error_code'] + ' ' + result['error_code'])
        return 0


# 主函数
# if __name__ == '__main__':
def programing():
    servo_init()  # 舵机复位

    GPIO.setmode(GPIO.BCM)  # 设置GPIO模式，BCM模式在所有的树莓派中通用
    GPIO.setwarnings(False)  # 禁用警告
    GPIO.setup(24, GPIO.OUT)  # 设置GPIO 18 为输出，该脚表示人脸识别正在运行
    GPIO.setup(21, GPIO.OUT)

    GPIO.output(21, GPIO.LOW)
    GPIO.output(24, GPIO.HIGH)
    will_start_to_recognize()
    print('准备开始，请面向摄像头 ^_^')
    if True:
        getimage()  # 拍照
        img = transimage()  # 转换照片格式
        res = go_api(img)  # 将转换了格式的照片上传百度云
        if res == 1:  # 是人脸库中的人
            LED_recognized_successful()  # LED闪烁
            recognized_successful()  # voice broadcast
            bt_open()
            print("欢迎回家，门已经打开")
            print("门将在5秒后关闭")
        elif res == -1:  # 没有检测到人脸
            LED_recognition_error()
            no_face_detected()
            print("我没有看见您，请您在黄灯亮起后按下按键再次尝试")
            time.sleep(3)
        elif res == 0:  # 不是人脸库中的人脸
            LED_recognition_error()
            getmessages2()
            face_mismatch()
            print("人脸不匹配，请再次尝试")
            time.sleep(3)
        else:
            print("请再次尝试")

        time.sleep(5)
        bt_close()
        print("请下按键再次进行人脸识别")
        GPIO.setmode(GPIO.BCM)  # 设置GPIO模式，BCM模式在所有的树莓派中通用
        GPIO.setwarnings(False)  # 禁用警告
        GPIO.setup(24, GPIO.OUT)  # 设置GPIO 18 为输出，该脚表示人脸识别正在运行
        GPIO.setup(21, GPIO.OUT)
        GPIO.output(24, GPIO.LOW)
        GPIO.output(21, GPIO.HIGH)


def my_callback(channel):
    global ledStatus
    ledStatus = not ledStatus
    if ledStatus:
        programing()
    else:
        pass
    pass


# 给22引脚添加一个事件函数，触发条件是：捕获到GPIO.FALLING（下降沿）
GPIO.add_event_detect(GPIO_IN_PIN22, GPIO.FALLING, callback=my_callback, bouncetime=150)
if __name__ == '__main__':
    while True:
        try:
            # GPIO.output(23,GPIO.LOW)
            GPIO.output(21, GPIO.HIGH)  # GPIO 18输出3.3v 输出高电平 LED灯亮
            print("按下按键进行人脸识别,,,")
            time.sleep(100)
            break
        except:
            GPIO.output(21, GPIO.LOW)  # GPIO 18输出3.3v 输出高电平 LED灯亮
            break
            pass
        pass
