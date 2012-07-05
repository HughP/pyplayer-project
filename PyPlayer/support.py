# -*- coding: utf-8 -*-

def S2HMS(t):
# Converts seconds to a string formatted H:mm:ss
    if t > 3600:
        h = int(t/3600)
        r = t-(h*3600)
        m = int(r / 60)
        s = int(r-(m*60))
        return '{0}:{1:02n}:{2:02n}'.format(h,m,s)
    else:
        m = int(t / 60)
        s = int(t-(m*60))
        return '{0}:{1:02n}'.format(m,s)

def strToSec(sec):
# Converts string 3:58 -> int 238
    min = int(sec.split(':')[0])
    min *= 60
    min = min + int(sec.split(':')[1])
    return min


