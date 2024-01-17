import time
import robomaster
from robomaster import conn
from robomaster import robot

from MyQR import myqr
from PIL import Image

# Check the instruction: https://robomaster-dev.readthedocs.io/en/latest/python_sdk/connection.html

def DirectConnection():
    # 如果本地IP 自动获取不正确，手动指定本地IP地址
    # robomaster.config.LOCAL_IP_STR = "192.168.2.20"
    ep_robot = robot.Robot()

    # 指定连接方式为AP 直连模式
    ep_robot.initialize(conn_type='ap')

    version = ep_robot.get_version()
    print("Robot version: {0}".format(version))
    ep_robot.close()

def USBConnection():
    ep_robot = robot.Robot()

    # 指定连接方式为USB RNDIS模式
    ep_robot.initialize(conn_type='rndis')

    version = ep_robot.get_version()
    print("Robot version: {0}".format(version))
    ep_robot.close()

# def NetworkingConnection(qrcodeName):
#     helper = conn.ConnectionHelper()
#     info = helper.build_qrcode_string(ssid="RoboMaster_SDK_WIFI", password="12341234")
#     myqr.run(words=info)
#     time.sleep(1)
#     img = Image.open(qrcodeName)
#     img.show()
#     if helper.wait_for_connection():
#         print("Connected!")
#     else:
#         print("Connect failed!")

if __name__ == '__main__':
    DirectConnection()