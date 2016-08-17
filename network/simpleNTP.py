# this file is fork from micropython/esp8266/scripts/ntptime.py
try:
    import ustruct as struct
except:
    import struct

import lwip

NTP_DELTA = 3155673600

def time(host="pool.ntp.org", timeout=1):
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1b
    addr = lwip.getaddrinfo(host, 123)[0][-1]
    s = lwip.socket(lwip.AF_INET, lwip.SOCK_DGRAM)
    s.settimeout(timeout)
    res = s.sendto(NTP_QUERY, addr)
    msg = s.recv(48)
    s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    return val - NTP_DELTA

