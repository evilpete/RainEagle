#!/usr/bin/env python

"""
based on TalkToEagle.py
"""


import socket
import sys
import time

my_macid = "0xd8d5b90000001296"



# Enter your Eagle's IP below
Eagle_IP = "10.1.1.39"

## list_devices

s = socket.create_connection( (Eagle_IP, 5002), 10)
print  s
time.sleep(1)

sendstr = "<LocalCommand>\n<Name>list_devices</Name>\n</LocalCommand>\n"

s.sendall(sendstr)
print
print "sending to Eagle: \n\r"
print sendstr
print

time.sleep(1)

print "Eagle response: \n\r"

while 1:
    buf = s.recv(1000)
    if not buf:
        break
    sys.stdout.write(buf)

s.close()


## get_history_data

s = socket.create_connection( (Eagle_IP, 5002), 10)
print  s

time.sleep(1)

sendstr = "<LocalCommand>\n<Name>get_history_data</Name>\n<MacId{0}</MacId>\n<StartTime>0x00000000</StartTime>\n</LocalCommand>\n".format(my_macid)

s.sendall(sendstr)
print
print "sending to Eagle: \n\r"
print sendstr
print

time.sleep(1)

print "Eagle response: \n\r"

while 1:
    buf = s.recv(1000)
    if not buf:
        break
    sys.stdout.write(buf)

s.close()


exit(0)
