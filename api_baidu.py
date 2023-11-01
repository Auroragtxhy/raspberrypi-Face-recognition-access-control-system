# coding: utf-8
from aip import AipFace
import config
from datetime import datetime
import base64


APP_ID = '23748600'
API_KEY = '8oLKV0GqmGW6DAO2qkgWXB2c'
SECRET_KEY = 'h2PRloq3CRt23izsYkO43lGZhdcry2EG'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)  # 创建一个客户端用以访问百度云
# 图像编码方式
IMAGE_TYPE = 'BASE64'
# 用户组
GROUP = 'GT_01'


def get_current_time():
    n = datetime.now()
    return f'{n.year}年{n.month}月{n.day}日{n.hour}时{n.minute}分{n.second}秒'


def write_log(n: str):
    with open(config.log_file, mode='a', encoding='utf-8') as f:
        f.write(f'[{get_current_time()}]Person: {n}\n')


no_face_detected = 3
face_mismatch = 2
recognized_successful = 1


def recognize(image_byte: bytes):
    """
    调用百度的api进行识别
    :param image_byte: 二进制格式的图片
    :return:
    """
    image_in_base64_string = base64.b64encode(image_byte).decode('utf-8')  # 二进制转 base64
    result = client.search(image_in_base64_string, IMAGE_TYPE, GROUP)  # 在百度云人脸库中寻找有没有匹配的人脸
    if result['error_msg'] == 'SUCCESS':  # 如果成功了
        name = result['result']['user_list'][0]['user_id']  # 获取名字
        score = result['result']['user_list'][0]['score']  # 获取相似度
        if score > 80:  # 如果相似度大于80
            if name in config.person_dict:
                t = recognized_successful
                msg = '人脸识别成功'
            else:
                msg = '人脸不在合法的列表中'
                t = face_mismatch
        else:
            t = face_mismatch
            name = 'unKnown'
            msg = '未知用户'
        # 将人员出入的记录保存到log.log中
        # write_log(n=name)
        write_log(n=config.person_dict.get(name))  # 获取字典中对于的人名
        return t, name, msg
    elif result['error_msg'] == 'pic not has face':
        return no_face_detected, None, '摄像头没没有捕获到人脸'
    else:
        print(result['error_code']+' ' + result['error_code'])
        return no_face_detected, None, '其他故障'


