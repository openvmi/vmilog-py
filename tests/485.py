import sys

sys.path.append('../src')

from vmi485tousb import UartChannel


if __name__ == "__main__":
    channel = UartChannel()
    channel.endableMock()
    command = bytes([0x01,0x02,0x03,0x04])
    print(channel.queryValue(command=command, responseLength=10))