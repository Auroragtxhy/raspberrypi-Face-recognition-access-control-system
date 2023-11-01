import bluetooth
import config


def servo_init():
    """初始化指令"""
    if not config.is_rpi:
        print('初始化指令')
        return
    bd_addr = "98:DA:50:00:25:64"  # arduino连接的蓝牙模块的地址
    port = 1

    sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))  # 创建连接

    sock.send("1")  # 发送数据
    sock.close()  # 关闭连接


def bt_open():
    """开门指令"""
    if not config.is_rpi:
        print('开门指令')
        return
    bd_addr = "98:DA:50:00:25:64" 
    port = 1

    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((bd_addr, port)) 

    sock.send("2") 
    sock.close() 


def bt_close():
    """关门指令"""
    if not config.is_rpi:
        print('关门指令')
        return
    bd_addr = "98:DA:50:00:25:64" 
    port = 1

    sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    sock.connect((bd_addr, port)) 

    sock.send("3") 
    sock.close()

