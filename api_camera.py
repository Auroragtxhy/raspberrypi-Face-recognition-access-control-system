# coding: utf-8
from io import BytesIO
import config
from PIL import Image
from time import sleep
import base64


if config.is_rpi:
    from picamera import PiCamera
else:
    import cv2


def init_camera():
    if config.is_rpi:
        camera = PiCamera()  # 定义一个摄像头对象
        camera.resolution = (config.image_width, config.image_width)
        return camera
    else:
        cap: cv2.VideoCapture = cv2.VideoCapture(config.usb_camera)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.image_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.image_height)
        print('1111111111111111')
        return cap


def test_camera():
    if config.is_rpi:
        print('Only for usb camera')
        return
    cap = init_camera()
    while True:
        ret, frame = cap.read()
        cv2.imshow("Video", frame)
        # 读取内容
        if cv2.waitKey(10) == ord("q"):
            break
    cap.release()


def get_image_from_rpi(camera) -> bytes:
    """
    从 PiCamera 摄像头读取一张图片
    :param camera:
    :return:
    """
    stream = BytesIO()
    # camera = PiCamera()
    # camera.start_preview()
    # sleep(2)
    camera.capture(stream, format='jpeg')
    stream.seek(0)
    return stream.read()


def get_image_from_opencv(cap) -> bytes:
    """借助 opencv 从摄像头读取图片"""
    ret, frame = cap.read()
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_bytes = cv2.imencode('.jpg', image_rgb)[1].tobytes()
    return image_bytes


def get_image(cap):
    """
    从摄像头获取一张图片，返回的是 二进制格式的图片文件

    :param cap: 摄像头对象
    :return: 返回的是 二进制格式的图片文件
    """
    if config.is_rpi:
        return get_image_from_rpi(cap)
    else:
        return get_image_from_opencv(cap)


def display_bytes_image(obj: bytes):
    """展示二进制格式的图片"""
    stream = BytesIO()
    stream.write(obj)
    stream.seek(0)
    im = Image.open(stream)
    im.show()
    stream.close()


if __name__ == '__main__':
    cap = init_camera()
    ib = get_image(cap)
    display_bytes_image(ib)
