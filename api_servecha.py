# coding: utf-8

# 发送消息到手机的serve酱上
import config
import requests

secret = 'SCT18221Twcxac0yixLl0pqTELmqtRsI4'  # serve酱的密匙

# def getmessages1():
#     sckey = 'SCT18221Twcxac0yixLl0pqTELmqtRsI4'#serve酱的密匙
#     url = 'https://sctapi.ftqq.com/%s.send?text=识别成功'%sckey
#     #text为推送的title,desp为推送的描述
#     url = 'https://sctapi.ftqq.com/%s.send?text=识别成功&desp=欢迎官腾回家，门已经为您打开,祝您生活快乐'%sckey
#     requests.get(url)
# def getmessages2():
#     sckey = 'SCT18221Twcxac0yixLl0pqTELmqtRsI4'#serve酱的密匙
#     url = 'https://sctapi.ftqq.com/%s.send?text=识别不成功'%sckey
#     #text为推送的title,desp为推送的描述
#     url = 'https://sctapi.ftqq.com/%s.send?text=识别不成功&desp=检测到陌生人脸，对方在尝试进门，请您注意'%sckey
#     requests.get(url)
# def getmessages3():
#     sckey = 'SCT18221Twcxac0yixLl0pqTELmqtRsI4'#serve酱的密匙
#     url = 'https://sctapi.ftqq.com/%s.send?text=识别成功'%sckey
#     #text为推送的title,desp为推送的描述
#     url = 'https://sctapi.ftqq.com/%s.send?text=识别成功&desp=欢迎杨昕鋮回家，门已经为您打开，祝您生活愉快'%sckey
#     requests.get(url)


def push_message(n: str):
    name = config.person_dict.get(n)
    print(n, name)
    if name is None:
        url = f'https://sctapi.ftqq.com/{secret}.send?text=识别不成功&desp=检测到陌生人脸，对方在尝试进门，请您注意!'
    else:
        url = f'https://sctapi.ftqq.com/{secret}.send?text=识别成功&desp=欢迎{name}回家，门已经为您打开，祝您生活愉快!'
    requests.get(url)
        
# if __name__ == '__main__':
#     push_message('a')
