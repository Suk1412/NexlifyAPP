import struct
import subprocess
import re

def int_to_byte_list(integer_value):
    byte_list = []
    while integer_value > 0:
        byte = integer_value & 0xFF
        byte_list.insert(0, byte)
        integer_value >>= 8
    return byte_list

def decode_access_bits(ac_bytes):
    ac0, ac1, ac2 = ac_bytes  # Byte 6, 7, 8

    c1 = ((ac1 & 0x10) >> 4) | ((ac1 & 0x01) << 1) | ((ac0 & 0x10) >> 2) | ((ac0 & 0x01) << 2)
    c2 = ((ac1 & 0x20) >> 5) | ((ac1 & 0x02))      | ((ac0 & 0x20) >> 3) | ((ac0 & 0x02) << 1)
    c3 = ((ac1 & 0x40) >> 6) | ((ac1 & 0x04) << 1) | ((ac0 & 0x40) >> 4) | ((ac0 & 0x04) << 2)

    # 每两位为一个 block 的 (C1,C2,C3)，block 0~3
    blocks = []
    for i in range(4):
        C1 = (c1 >> i) & 1
        C2 = (c2 >> i) & 1
        C3 = (c3 >> i) & 1
        blocks.append((C1, C2, C3))
    return blocks

# Tg=1
# auth_type=0x60
# block = 0x05
# key=[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
# UID = [0x63, 0xAF, 0x74, 0xDD]

# InDataExchange_cmd = [0xD4, 0x40,] + [Tg] + [auth_type] + [block] + key + UID
# print(InDataExchange_cmd)



# check="^/dev/(ttyUSB|ttyACM)[0-9]+$", check_error="非规范串口"

def A():
    import re
    m = "^\/dev\/(ttyUSB|ttyACM)[0-9]+$"
    pattern = re.compile(m)
    data = "/dev/ttyUSB1"
    if pattern.match(data):
        print("合法")
    else:
        print("不合法")


# def crc16_x25(data: bytes) -> int:
#     poly = 0x8408  # 反转后的 0x1021（LSB-first）
#     crc = 0xFFFF
#     for byte in data:
#         crc ^= byte
#         for _ in range(8):
#             if crc & 0x0001:
#                 crc = (crc >> 1) ^ poly
#             else:
#                 crc >>= 1

#     # 按 X.25 标准：再异或输出值
#     crc ^= 0xFFFF
#     return crc & 0xFFFF
# print(hex(crc16_x25(rid_command)))


def calculate_checksum(data_bytes):
    s = sum(data_bytes)
    return (~s + 1) & 0xFF

def Data_Splicing(data):
     print(data)
     Preamble = 0x00
     Start_Code1 = 0x00
     Start_Code2 = 0xff
     LEN = len(data)
     LCS = (0x100 - len(data)) & 0xFF
     PD = data
     DCS = calculate_checksum(PD)
     End_Code = 0x00
     return bytearray([Preamble, Start_Code1, Start_Code2, LEN, LCS, *PD, DCS, End_Code])

# data = [0xD4, 0x02]
# data = b"\x04\x02"
# print(Data_Splicing(data))
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

def crc16(data):
    crc = 0xFFFF
    polynomial = 0x1021
    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1
            crc &= 0xFFFF
    return crc




def crc16(data):
    crc = 0xFFFF
    polynomial = 0x1021
    for byte in data:
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1
            crc &= 0xFFFF
    return crc



data = b"\x93pc\xaft\xdde"
data = b"\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"
data = b"\x00"
data = b"\x60\x05"
def calculate_crc(data, size, reg):
    for octet in data[:size]:
        for pos in range(8):
            bit = (reg ^ ((octet >> pos) & 1)) & 1
            reg = reg >> 1
            if bit:
                reg = reg ^ 0x8408
    return reg

def _checksum(checksum_packet: bytes) -> int:
    """Calculate CRC_B as defined in ISO/IEC 14443-3 (Annex B)."""
    crc = 0x6363  # Initial value
    poly = 0x8408  # Reversed polynomial for CRC-16-CCITT
    for byte in checksum_packet:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
    return crc & 0xFFFF

print(hex(calculate_crc(data, 7, 0x6363)))
print(hex(_checksum(data)))