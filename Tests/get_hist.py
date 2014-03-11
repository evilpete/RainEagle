#!/usr/bin/env python

"""
based on TalkToEagle.py
"""


import socket
import sys
import time
import xml.etree.ElementTree as ET

my_macid = "0xd8d5b90000001296"



# Enter your Eagle's IP below
Eagle_IP = "10.1.1.39"

def print_summ(cs) :
    # global last_delivered
    # time_stamp = eg.to_epoch_1970(cs['TimeStamp'])

    _delivered = cs.find('SummationDelivered').text
    _received = cs.find('SummationReceived').text
    _multiplier = cs.find('Multiplier').text
    _divisor = cs.find('Divisor').text

    # print "Multiplier=", _multiplier, "Divisor=", _divisor, "Delivered=", _delivered, "Received=", _received

    multiplier=int(_multiplier, 16)
    divisor=int(_divisor, 16)
    delivered=int(_delivered, 16)
    received=int(_received, 16)
    time_stamp = 946684800 + int(cs.find('TimeStamp').text, 16)

    # print "Multiplier=", multiplier, "Divisor=", divisor, "Delivered=", delivered, "Received=", received, "TimeStamp", time_stamp
 
    if multiplier == 0 :
	multiplier=1

    if divisor == 0 :
	divisor=1

    reading_received =  received * multiplier /  float (divisor )
    reading_delivered =  delivered * multiplier /  float (divisor )
    #reading_delta = (reading_delivered - last_delivered)
    #last_delivered = reading_delivered

    print time.asctime(time.localtime(time_stamp)), " : ", reading_received, "\t", reading_delivered


def print_reading(eg, rd) :
    for dat in rd['Reading'] :
	time_stamp = time.asctime(time.localtime(  to_epoch_1970(dat['TimeStamp'])  ) )

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

sendstr = "<LocalCommand>\n<Name>get_history_data</Name>\n<MacId>{0}</MacId>\n<StartTime>0x00000000</StartTime>\n</LocalCommand>\n".format(my_macid)

s.sendall(sendstr)
print
print "sending to Eagle: \n\r"
print sendstr
print

time.sleep(1)

print "Eagle response: \n\r"

j=0
buf_list = []
while 1:
    buf = s.recv(1000)
    if not buf:
        break
    buf_list.append(buf)
    #sys.stdout.write(buf)
    j = j + 1

result_xml = ''.join(buf_list)
print result_xml
etree = ET.fromstring(result_xml)
for cs in etree.iter('CurrentSummation'):
     print_summ(cs)

print "j =", j

s.close()


#main()
exit(0)
