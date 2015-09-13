#!/usr/local/bin/python2.7
"""
    A simple script to generate guuplot data from meter history
"""

__author__ = "Peter Shipley"
__version__ = "0.1.8"


import RainEagle
import time
from pprint import pprint
from RainEagle import Eagle, to_epoch_1970

import json

last_delivered = 0
last_received = 0
max_delta_received = 0
max_delta_delivered = 0
day_delta_received = 0
day_delta_delivered = 0
curr_day = -1


def main(eg) :
    print_data(eg)
    exit(0)


def print_data(eg) :
    rh = eg.get_history_data()
    #+ # endtime=None, frequency=None) :
    global curr_day


    curr_day = time.gmtime(1);

    for dat in rh['HistoryData']['CurrentSummation'] :
        print_currentsummation(dat)

    print "# day_delta_received={0:0.4f}\tday_delta_delivered={1:0.4f} : {2:0.4f}".format(
            day_delta_received,
            day_delta_delivered,
            (day_delta_delivered - day_delta_received))
    print "# max_delta_received={0:0.4f}\tmax_delta_delivered={1:0.4f}".format(
            max_delta_received, max_delta_delivered)


def print_currentsummation(cs) :
    global last_delivered
    global last_received

    global max_delta_received
    global max_delta_delivered
    global day_delta_received
    global day_delta_delivered
    global curr_day

    time_stamp = to_epoch_1970(cs['TimeStamp'])

    multiplier = int(cs['Multiplier'], 16)
    divisor = int(cs['Divisor'], 16)
    delivered = int(cs['SummationDelivered'], 16)
    received = int(cs['SummationReceived'], 16)

    # print "Multiplier=", multiplier, "Divisor=", divisor, "Demand=", demand

    if multiplier == 0 :
        multiplier = 1

    if divisor == 0 :
        divisor = 1

    reading_received = received * multiplier / float(divisor)
    delta_received = (reading_received - last_received)
    last_received = reading_received
    if (delta_received > max_delta_received and delta_received < 1000) :
        max_delta_received = delta_received
        #print "new max_delta_received :", max_delta_received

    reading_delivered = delivered * multiplier / float(divisor)
    delta_delivered = (reading_delivered - last_delivered)
    last_delivered = reading_delivered
    if (delta_delivered > max_delta_delivered and delta_delivered < 1000) :
        max_delta_delivered = delta_delivered
        #print "\t\tnew max_delta_delivered :", max_delta_delivered

    time_struct = time.localtime(time_stamp)
    if curr_day.tm_mday != time_struct.tm_mday :
        curr_day = time_struct
        print "# {0} day_delta_received={1:0.4f}".format( \
                    time.strftime("%a %Y-%m-%d", curr_day),
                    day_delta_received) \
            + "\tday_delta_delivered={0:0.4f}".format(day_delta_delivered) \
            + " : {0:0.4f}".format((day_delta_delivered - day_delta_received))
        day_delta_received = 0
        day_delta_delivered = 0

    day_delta_received += delta_received
    day_delta_delivered += delta_delivered

    print "{0}\t{1:.4f}\t{2:0.4f}\t{3:.4f}\t{4:0.4f}".format(
        time.strftime("%Y-%m-%d %H:%M:%S", time_struct),
        reading_received,
        delta_received,
        reading_delivered,
        delta_delivered)


if __name__ == "__main__":
    # import __main__
    # print(__main__.__file__)
    # print("syntax ok")
    reagle = RainEagle.Eagle(debug=0)
    main(reagle)
    exit(0)
