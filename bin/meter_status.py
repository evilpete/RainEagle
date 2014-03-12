#!/usr/local/bin/python2.7
"""
    A simple script get current meter values
"""
	 
__author__ = "Peter Shipley"

import sys
sys.path.append('/usr/home/shipley/Projects/Eagle') # temp


# import RainEagle
from RainEagle import Eagle, to_epoch_1970
import time
from pprint import pprint
import json

last_delivered = 0
debug = 0


def main() :
    eg = Eagle( debug=debug , addr="10.1.1.39")
    # timeout=45,

    # print "\nlist_devices :"
    # r = eg.list_devices()
    # print "pprint 2"
    # pprint(r)



    print "\nget_device_data :"
    r = eg.get_device_data()
    print

    # pprint(r['InstantaneousDemand'])
    print_instantdemand( r['InstantaneousDemand'])
    print

    # pprint(r['CurrentSummation'])
    print_currentsummation(r['CurrentSummation'])
    print

    exit(0)

def twos_comp(val, bits=32):
    """compute the 2's compliment of int value val"""
    if( (val&(1<<(bits-1))) != 0 ):
	val = val - (1<<bits)
    return val

def print_currentsummation(cs) :

    multiplier=int(cs['Multiplier'], 16)
    divisor=int(cs['Divisor'], 16)
    delivered=int(cs['SummationDelivered'], 16)
    received=int(cs['SummationReceived'], 16)

    if multiplier == 0 :
	multiplier=1

    if divisor == 0 :
	divisor=1

    reading_received =  received * multiplier /  float (divisor )
    reading_delivered = delivered * multiplier /  float (divisor )

    time_stamp = to_epoch_1970(cs['TimeStamp'])

    print time.asctime(time.localtime(time_stamp)), " : "
    print "\tReceived =", reading_received, "Kw"
    print "\tDelivered=", reading_delivered, "Kw"
    print "\t\t\t", (reading_delivered - reading_received)


#    print "{0}\t{1:.4f}\t{2:0.4f}\t{3:.4f}".format(
#	time.strftime("%Y-%m-%d %H:%M:%S", time_struct), 
#	reading_received, 
#	reading_delivered, 
#	(reading_delivered - reading_received) )


def print_instantdemand(idemand) :

    time_stamp = to_epoch_1970(idemand['TimeStamp'])

    multiplier=int(idemand['Multiplier'], 16)
    divisor=int(idemand['Divisor'], 16)
#    demand =  twos_comp(int(idemand['Demand'], 16))
    demand=int(idemand['Demand'], 16)
    if demand > 0x7FFFFFFF:
	demand -= 0x100000000

    # print "Multiplier=", multiplier, "Divisor=", divisor, "Demand=", demand
 
    if multiplier == 0 :
	multiplier=1

    if divisor == 0 :
	divisor=1

    reading =  (demand * multiplier) /  float (divisor )

    print time.asctime(time.localtime(time_stamp)), " : "
    print "\tDemand=", reading, "Kw"
    print "\tAmps  = {:.3f}".format( ((reading * 1000) / 240) )



def print_reading(eg, rd) :
    for dat in rd['Reading'] :
	the_time = time.asctime(time.localtime(  to_epoch_1970(dat['TimeStamp'])  ) )
	print the_time, "Type=", dat['Type'], "Value=",  dat['Value']

# 
if __name__ == "__main__":
    # import __main__
    # print(__main__.__file__) 
    # print("syntax ok") 
    main()
    exit(0) 


