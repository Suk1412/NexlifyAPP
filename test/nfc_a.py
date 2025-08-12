

from nfc import clf
from nfc.clf import transport
from nfc.clf import pn532
from nfc.clf import TimeoutError
import time

import glob
from typing import Optional

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



ttype = "ttt"
device_name = default_serial()
tty = transport.TTY(device_name)
device = pn532.init(tty)
device._path = device_name
print("device_path: %s" % device._path)
select_sense = {"106A": device.sense_tta,
                "212F": device.sense_ttf,
                "424F": device.sense_ttf,
                "106B": device.sense_ttb}
target = clf.RemoteTarget("106A")
print(target.brty)

for i in range(5):
    target = select_sense[target.brty](target)
    if target is not None:
        print("card selected!")
        print("target: %s" % target)
        break
    else:
        print("no card selected!")
        print("target: %s" % target)


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
import struct


def get_select_uid_cmd():
    select_data = b"\x93\x70\x63\xaf\x74\xdd"
    BCC = struct.pack("B", 0x63^0xaf^0x74^0xdd)
    data = select_data + BCC
    return data

# data = get_select_uid_cmd()
# data = b"\x30\x00"
data = b"\x60\x05\xff\xff\xff\xff\xff\xff\x63\xaf\x74\xdd"
data = b"\x00\x01\x63\xAF\x74\xDD\x00\x00\x00\x00\x01\xFE\x73\x00\x00\x00\x01\x46\x66\x6D\x01\x01\x11\x03\x02\x00\x80"
def transform(data, timeout = 0):
    print("--------------------------------------------------------------",ttype)
    ret = device.send_cmd_recv_rsp(target, data, timeout, ttype = ttype)
    print("ret"*30,ret)
    return ret

try:
    for count in range(1):
        try:
            print("变异")
            transform(data)
        except TimeoutError as exc:
            target = select_sense[target.brty](target)
            if target is None:
                error_message = f"device not found"
            else:
                continue
except KeyboardInterrupt as e:
    print("user broken !")


time.sleep(0.1)
device.close()
    
