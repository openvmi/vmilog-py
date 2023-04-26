import netifaces as ni
import os


def getIpV4():
    if os.name == 'nt':
        raise Exception("This module not support windows")
    iface = ni.interfaces()
    def inner_get_ip(key):
        adr = ni.ifaddresses(key)
        if ni.AF_INET in adr:
            return adr[ni.AF_INET][0]['addr']
        return None
    desirdIface = ['eth0', 'wlan0']
    for i in desirdIface:
        _ipv4 = inner_get_ip(i)
        if _ipv4 is not None:
            return i, _ipv4
    return None, None
