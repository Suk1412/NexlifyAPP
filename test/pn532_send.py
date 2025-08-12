import glob
import sys
import time
import serial
from nfc.clf import transport
from nfc.clf import pn532
from struct import pack, unpack


long_preamble = bytearray(10)
ACK = bytearray.fromhex('0000FF00FF00')
get_version_rsp = bytearray.fromhex("0000ff06fad50332")
sam_configuration_rsp = bytearray.fromhex("0000ff02fed5151600")
inlistpassivetarget_rsp = bytearray.fromhex("0000ff0cf4d54b")
InDataExchange_rsp = bytearray.fromhex("0000ff13edd5")


def list_serial_ports():
    ports = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
    return ports


def default_serial():
    SerialPorts = list_serial_ports()
    if SerialPorts:
        iface = SerialPorts[0]
    else:
        iface = "No device found"
    return iface

def read(sock):
     if sock is not None:
          frame = bytearray(sock.read(6))
          if frame is None or len(frame) == 0:
               frame = bytearray(sock.read(6))
          # print("接收帧头",frame.hex())
          if frame.startswith(b"\x00\x00\xff\x00\xff\x00"):
               print("pn532 <--- host:",frame.hex())
               return frame
          LEN = frame[3]
          if LEN == 0xFF:
               frame += sock.read(3)
               LEN = frame[5] << 8 | frame[6]
          frame += sock.read(LEN + 1)
          print("pn532 <--- host:",frame.hex())
          return frame


def send(sock, data):
     sock.write(long_preamble + data)
     print("host ---> pn532:",data.hex())


def recv(sock, cmd_name="All Recv"):
     if cmd_name == "GetFirmwareVersion":
          if not read(sock) == ACK:
               print("未接收到确认ACK")
          if not read(sock).startswith(get_version_rsp):
               print(f"未接收到{cmd_name}")
     if cmd_name == "SAMConfiguration":
          if not read(sock) == ACK:
               print("未接收到确认ACK")
          if not read(sock).startswith(sam_configuration_rsp):
               print(f"未接收到{cmd_name}")
     if cmd_name == "InListPassiveTarget":
          if not read(sock) == ACK:
               print("未接收到确认ACK")
          if not read(sock).startswith(inlistpassivetarget_rsp):
               print(f"未接收到{cmd_name}")
     if cmd_name == "InDataExchange":
          if not read(sock) == ACK:
               print("未接收到确认ACK")
          if not read(sock)[5:8].hex() == "d54100":
               print(f"未接收到{cmd_name}")
     if cmd_name == "ReadRegister":
          if not read(sock) == ACK:
               print("未接收到确认ACK")
          if not read(sock)[5:8].hex() == "d50780":
               print(f"未接收到{cmd_name}")
     if cmd_name == "WriteRegister":
          if not read(sock) == ACK:
               print("未接收到确认ACK")
          if not read(sock)[5:8].hex() == "d50922":
               print(f"未接收到{cmd_name}")
     if cmd_name == "All Recv":
          if not read(sock) == ACK:
               print("未接收到确认ACK")
          if not read(sock):
               print(f"未接收到{cmd_name}")
      
               
def hex_to_list(hex_str):
     byte_list = [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]
     return byte_list

def calculate_checksum(data_bytes):
    s = sum(data_bytes)
    return (~s + 1) & 0xFF

def Data_Splicing(data):
     Preamble = 0x00
     Start_Code1 = 0x00
     Start_Code2 = 0xff
     LEN = len(data)
     LCS = (0x100 - len(data)) & 0xFF
     PD = data
     DCS = calculate_checksum(PD)
     End_Code = 0x00
     return bytearray([Preamble, Start_Code1, Start_Code2, LEN, LCS, *PD, DCS, End_Code])


# SOF = bytearray.fromhex('0000FF')
# def Data_Splicing(cmd_code, cmd_data):
#      if len(cmd_data) < 254:
#           head = SOF + bytearray([len(cmd_data)+2]) + bytearray([254-len(cmd_data)])
#      else:
#           head = SOF + b'\xFF\xFF' + pack(">H", len(cmd_data)+2)
#           head.append((256 - sum(head[-2:])) & 0xFF)

#      data = bytearray([0xD4, cmd_code]) + cmd_data
#      tail = bytearray([(256 - sum(data)) & 0xFF, 0])
#      frame = head + data + tail
#      return frame





GetFirmwareVersion_cmd = [0xD4, 0x02]
SAMConfiguration_cmd = [0xD4, 0x14, 0x01, 0x14, 0x01]
InListPassiveTarget_cmd = [0xD4, 0x4A, 0x01, 0x00]
InDataExchange_cmd = [
    0xD4, 0x40,  # InDataExchange
    0x01,        # Tg = 1
    0x60,        # Authenticate using Key A
    0x00,        # Block number to authenticate
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,  # Key A (6 bytes)
    0x64, 0xb5, 0xc0, 0x8e  # UID of the card (4 bytes)
]  



port = default_serial()
baudrate = 115200
tty = serial.Serial(port, baudrate, timeout=0.05)
tty.reset_input_buffer()


def GetFirmwareVersion():
     send_name = "GetFirmwareVersion"
     print("*"*30)
     print(f"获取固件版本号:{send_name}命令")
     get_version_cmd = Data_Splicing(GetFirmwareVersion_cmd)
     send(tty, get_version_cmd)
     recv(tty, send_name)

def SAMConfiguration():
     send_name = "SAMConfiguration"
     print("*"*30)
     print(f"获取固件版本号:{send_name}命令")
     get_version_cmd = Data_Splicing(SAMConfiguration_cmd)
     send(tty, get_version_cmd)
     recv(tty, send_name)

def InListPassiveTarget():
     send_name = "InListPassiveTarget"
     print("*"*30)
     print(f"扫描并侦测附近目标:{send_name}命令")
     sam_configuration_cmd = Data_Splicing(InListPassiveTarget_cmd)
     send(tty, sam_configuration_cmd)
     recv(tty, send_name)


def InDataExchange_Auth(Tg=1, auth_type=0x60, block = 0x05, key=[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], UID = [0x63, 0xAF, 0x74, 0xDD]):
     InDataExchange_cmd = [0xD4, 0x40,] + [Tg] + [auth_type] + [block] + key + UID
     send_name = "InDataExchange"
     print("*"*30)
     print(f"发送认证命令:{send_name}命令，块号{block}")
     auth_cmd = Data_Splicing(InDataExchange_cmd) 
     send(tty, auth_cmd)
     recv(tty, send_name)

def InDataExchange_Read(block=5):
     InDataExchange_cmd = [0xD4, 0x40, 0x01, 0x30, block]
     send_name = "InDataExchange"
     print("*"*30)
     print(f"发送数据命令:{send_name}命令,读取块号{block}的数据")
     auth_cmd = Data_Splicing(InDataExchange_cmd) 
     send(tty, auth_cmd)
     recv(tty, send_name)

def InDataExchange_write(block = 0x05):
     InDataExchange_cmd = [0xD4, 0x40, 0x01, 0xA0, block, 0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF]
     send_name = "InDataExchange"
     print("*"*30)
     print(f"发送数据命令:{send_name}命令,往块号{block}写入数据")
     auth_cmd = Data_Splicing(InDataExchange_cmd) 
     send(tty, auth_cmd)
     recv(tty, send_name)

def InJumpForDEP():
     InJumpForDEP_cmd = [0xD4, 0x56, 0x01, 0x02, 0x01, 0x02, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A]
     InJumpForDEP_cmd = [0xD4, 0x56, 0x00, 0x01, 0x63, 0xAF, 0x74, 0xDD, 0x00, 0x00, 0x00, 0x00, 0x01, 0xFE, 0x73, 0x00,
                         0x00, 0x00, 0x01, 0x46, 0x66, 0x6D, 0x01, 0x01, 0x11, 0x03, 0x02, 0x00, 0x80]
     # InJumpForDEP_cmd = [0xD4, 0x56, 0x00, 0xFF, 0xFF, 0x00, 0x01, 0x00]
     send_name = "All Recv"
     print("*"*30)
     print(f"发送数据命令:{send_name}命令")
     auth_cmd = Data_Splicing(InJumpForDEP_cmd) 
     send(tty, auth_cmd)
     recv(tty, send_name)


def ReadRegister():
     cmd_list = [0XD4,0X06,0X63,0X02,0X63,0X03,0X63,0X05]
     send_name = "ReadRegister"
     print("*"*30)
     print(f"发送数据命令:{send_name}命令")
     cmd_req = Data_Splicing(cmd_list) 
     send(tty, cmd_req)
     recv(tty, send_name)

def WriteRegister():
     cmd_list = [0XD4,0X08,0X63,0X02,0X80,0X63,0X03,0X00,0X63,0X05,0X4F]
     send_name = "WriteRegister"
     print("*"*30)
     print(f"发送数据命令:{send_name}命令")
     cmd_req = Data_Splicing(cmd_list) 
     send(tty, cmd_req)
     recv(tty, send_name)

def SendCMD(hex_str):
     cmd_list = hex_to_list(hex_str)
     send_name = "All Recv"
     print("*"*30)
     cmd_req = Data_Splicing(cmd_list) 
     send(tty, cmd_req)
     recv(tty, send_name)

def crc_b(data: bytes) -> int:
    """Calculate CRC_B as defined in ISO/IEC 14443-3 (Annex B)."""
    crc = 0x6363  # Initial value
    poly = 0x8408  # Reversed polynomial for CRC-16-CCITT
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1

    return crc & 0xFFFF

if __name__ == '__main__':
     GetFirmwareVersion()
     SAMConfiguration()
     InListPassiveTarget()
     # InDataExchange_Auth()
     # InDataExchange_Read()
     InJumpForDEP()
     # ReadRegister()
     # WriteRegister()

     # SendCMD(hex_str="d406630263036305")


     num = 0
     if num == 1:
          print("初始化--"*10)
          SendCMD(hex_str="d44a0100")
          SendCMD(hex_str="d4066303")
          SendCMD(hex_str="d408630300")
          print("发包--"*10)
          SendCMD(hex_str="d406630263036305")
          SendCMD(hex_str="d40863028063030063054f")
          SendCMD(hex_str="d432020a0b01")
          
          SendCMD(hex_str="d44278")

          SendCMD(hex_str="d44a0100")
          SendCMD(hex_str="d4066303")
          SendCMD(hex_str="d408630300")

     if num == 2:
          SendCMD(hex_str="d414011401")
          SendCMD(hex_str="d44a0100")
          SendCMD(hex_str="d4423002")

     if num == 3:
          # cmd_list = ["d402",
          #             "d406630263036305",
          #             "d40863028063030063054f",
          #             "d432020a0b01",
          #             "d4423002",
          #             "d44a0100",
          #             "d4066303",
          #             "",
          #             "",
          #             "",
          #             "",
          #             ""]
          cmd_list = ["d402"
                      "d41220",
                         "d43202000b0a",
                         "d4320400",
                         "d43205010001",
                         "d4320a59f43f114d85616f266287",
                         "d4320b69ff3f114185616f",
                         "d4320cff0485",
                         "d4320d85158a8508b28501da",
                         "d4086316ff",
                         "d4320102",]
          for i in cmd_list:
               if i != "":
                    SendCMD(hex_str=i)
     if num == 4:
          """swift读取卡片"""
          "0000ff08f8"
          "0000ffffff0109f6"
          cmd_list = ["d40000000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9fa0a1a2a3a4a5a6a7a8a9aaabacadaeafb0b1b2b3b4b5b6b7b8b9babbbcbdbebfc0c1c2c3c4c5c6c7c8c9cacbcccdcecfd0d1d2d3d4d5d6d7d8d9dadbdcdddedfe0e1e2e3e4e5e6e7e8e9eaebecedeeeff0f1f2f3f4f5f6f7f8f9fafbfcfdfeff000102030405",]
          for i in cmd_list:
               if i != "":
                    SendCMD(hex_str=i)
               print(hex(len(i)))
    
     
     # def SendCMD(hex_str):
     #      send_name = "All Recv"
     #      print("*"*30)
     #      send(tty, hex_str)
     #      recv(tty, send_name)

     # C = bytes(hex_to_list("02000b0a"))
     # print(C)
     # A = Data_Splicing(cmd_code=0x32, cmd_data=C)
     # print(A)
     # SendCMD(hex_str=A)

     # data = len(hex_to_list("02000b0a"))
     # print(hex(data+2),hex(254-data))







