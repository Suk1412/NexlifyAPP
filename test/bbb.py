
import binascii
import re
import crcmod


def test(A,B):
    if A == B:
        print("Equal")
    else:
        print("Not Equal")


def check():
    import re
    m = "^(?:[A-Fa-f0-9]{8}|[A-Fa-f0-9]{14}|[A-Fa-f0-9]{20})$"
    pattern = re.compile(m)

    password = "63af74dd63af74dd"
    if pattern.match(password):
        print("校验正确")
    else:
        print("校验不正确")



def Zigbee_CRC(checksum_packet):
    """Zigbee协议校验和"""
    display_name =  "计算zigbee校验和"
    crc16 = crcmod.mkCrcFun(0x11021, rev=True, initCrc=0x0000, xorOut=0x0000)
    checksum = crc16(checksum_packet) & 0xffff
    return checksum

def StrtoByte_Hex(data: str) -> bytes:
    """ 
        将16进制字符串转化为16进制字节流
    """
    pattern = '^(0x)?[0-9a-fA-F]+$'
    match = re.match(pattern, data)
    if not match:
        raise ValueError("data must be 0x followed by hex digits")
    if data.startswith('0x'):
        data = data[2:]
    if len(data) % 2 == 1:
        data = '0' + data
    hex_data = binascii.a2b_hex(data)
    return hex_data


# data = StrtoByte_Hex("63cc4d2312234fc92f004b1200fc4d6afffe63ab1202fbe30045e6")
# CRC = Zigbee_CRC(data[:-2])
# print(hex(CRC))

import asyncio
import zigpy.config
from bellows.zigbee.application import ControllerApplication
from bellows.types.struct import EmberApsFrame
from bellows.types import EmberStatus




async def A():
    device_config = {
                zigpy.config.CONF_DEVICE_PATH: "/dev/ttyUSB6",
                zigpy.config.CONF_DEVICE_BAUDRATE: 115200,
                zigpy.config.CONF_DEVICE_FLOW_CONTROL: None,
            }
    config = ControllerApplication.SCHEMA({
        "device": device_config,  # 比如: {"path": "/dev/ttyUSB0", "baudrate": 115200}
        "database": "zigbee.db",  # 必须是你上次运行时使用的同一个 database
        "ota": {"providers": []},
        "ezsp_config": {"CONFIG_SECURITY_LEVEL": 0},
    })

    # 创建控制器实例（会自动加载网络）
    app = await ControllerApplication.new(config)

    # 不再调用 form_network()
    # 而是直接检查网络状态，或继续 permitJoining()
    await app._ezsp.permitJoining(255)  # 允许新设备加入



import serial
ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
znp_af_data_request = StrtoByte_Hex("23c89723120000ffff234fc92f004b12000180db86")
print(f"→ Request: {znp_af_data_request}")
ser.write(znp_af_data_request)
response = ser.read_all()
r = response.hex()
if response:
    print(f"← Response: {' '.join(r[i:i+2] for i in range(0, len(r), 2))}")
