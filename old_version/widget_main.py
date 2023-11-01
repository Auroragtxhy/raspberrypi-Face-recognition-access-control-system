# coding: utf-8
from PyQt5 import QtCore, QtWidgets, QtGui
from utils import AbstractFunction
from ui_design.main import Ui_Form as __Form
from widget_simulate import WidgetScanButton
import config
import sys
from datetime import datetime
import api_baidu
import api_bluetooth
import api_camera
import api_led
import api_servecha
import api_voice
import api_gpio
import os
import time
from api_led import *
from api_gpio import *

class FaceScanService(QtCore.QThread):
    sig_msg = QtCore.pyqtSignal(str)
    sig_image = QtCore.pyqtSignal(bytes)
    sig_finished = QtCore.pyqtSignal()

    def __init__(self, parent):
        super(FaceScanService, self).__init__(parent)
        self.cap = None

    def handle_init(self):
        self.sig_msg.emit('初始化摄像头')
        self.cap = api_camera.init_camera()
        self.sig_msg.emit('摄像头初始化完成')
        self.sig_msg.emit('初始化GPIO')
        api_gpio.init_gpio()
        self.sig_msg.emit('后台服务初始化完成')
        read_mode()  # LED灯指示待机状态
        self.sig_msg.emit('请在黄灯亮起后按下按键进行人脸识别')
        
    def run(self) -> None:  # 人脸识别主体进程
        if self.cap is None:
            # 初始化后台服务
            return self.handle_init()
        # ---------------------------
        # 执行一次人脸识别的流程
        # ---------------------------
        self.sig_msg.emit('准备开始，请面向摄像头 ^_^')
        start_scan()
        api_voice.will_start_to_recognize()
        self.sig_msg.emit('舵机复位开始')
        api_bluetooth.servo_init()
        self.sig_msg.emit('舵机复位完成')
        self.sig_msg.emit('人脸采集开始')
        
        i = 0
        while i < 5:
            img_obj = api_camera.get_image(cap=self.cap)
            self.sig_image.emit(img_obj)
            i += 0.5
            time.sleep(0.2)
            
        self.sig_msg.emit('人脸采集完成')
        

        fn = f'{datetime.now().strftime("%Y%m%d%H%M%S")}.jpg'
        fp = os.path.join('images', fn)
        with open(fp, mode='wb') as f:
            f.write(img_obj)

        self.sig_msg.emit('开始人脸识别')
        t, n, m = api_baidu.recognize(img_obj)
        print(t, n, m)
        if t == api_baidu.recognized_successful:  # 人脸识别成且合法
            name = config.person_dict.get(n)
            self.sig_msg.emit(f'欢迎{name}回家')
            api_servecha.push_message(n)  # 推送消息
            api_bluetooth.bt_open()  # 开门
            LED_recognized_successful()
            api_voice.recognized_successful()  # 播放语音
            time.sleep(1)
            api_bluetooth.bt_close()
        elif t == api_baidu.no_face_detected:  # 没有检测到人脸
            self.sig_msg.emit(m)
            LED_recognition_error()
            api_servecha.push_message(n)
            api_voice.no_face_detected()
        else:  # 人脸检测不合法
            self.sig_msg.emit(m)
            LED_recognition_error()
            api_servecha.push_message(n)
            api_voice.face_mismatch()

        self.sig_finished.emit()
        finished_scan()

class MainApp(QtWidgets.QWidget, __Form, AbstractFunction):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle(config.app_name_cn)

        if not config.is_rpi:
            w = WidgetScanButton(self)
            w.sig_scan.connect(self.handle_start_face_scan)
            w.show()
        else:
            api_gpio.setup_switch(self.handle_start_face_scan)

        self.service = FaceScanService(self)
        self.service.sig_msg.connect(self.display_message)
        self.service.sig_image.connect(self.display_image)
        self.service.sig_finished.connect(self.handle_face_scan_finished)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.init_background_service)
        self.timer.start(1000)
        self.display_message('后台服务启动中...')
        self.setMinimumSize(800, 600)

    def display_message(self, msg: str):
        now = datetime.now().strftime('%H:%M:%S')
        self.text_shell.moveCursor(QtGui.QTextCursor.Start)
        self.text_shell.insertHtml(f'<hr><p style="margin:5px;display:block;"><b style="color:green">[{now}]</b>{msg}</p>')

    def handle_start_face_scan(self, t=None):
        if self.service.isRunning():
            self.display_message('后台任务正在开展中,请耐心等待')
            return
        self.display_message('开始人脸识别')
        self.service.start()

    def init_background_service(self):
        self.timer.stop()
        self.timer.timeout.disconnect(self.init_background_service)
        self.service.start()

    def display_image(self, obj):  #识别结束后展示拍摄的照片
        """展示图片"""
        pix = QtGui.QPixmap()
        pix.loadFromData(obj)
        self.canvas.display_pix(pix)

    def handle_face_scan_finished(self):
        """人脸识别结束"""
        self.display_message('人脸识别结束,请再次按下按键进行人脸识别')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    app.exec_()

