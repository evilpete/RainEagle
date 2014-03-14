#!/usr/local/bin/python2.7
"""
    A simple script get current meter values
"""

__author__ = "Peter Shipley"
__version__ = "0.1.7"


# import RainEagle
from RainEagle import Eagle, to_epoch_1970
import time
import os
import argparse
from pprint import pprint

debug = 0


def create_parser():
    parser = argparse.ArgumentParser(
		    description="print power meter status")

    parser.add_argument("-a", "--address", dest="addr",
		    default=os.getenv('EAGLE_ADDR', None),
		    help="hostname or IP device")

    parser.add_argument("-p", "--port", dest="port", type=int,
		    default=os.getenv('EAGLE_PORT', 5002),
		    help="command socket port")

    parser.add_argument("-d", "--debug", dest="debug",
		    default=debug, action="count",
		    help="print debug info")

    parser.add_argument("-m", "--mac", dest="mac",
		    help="Eagle radio mac addrress")

    parser.add_argument("-t", "--timeout", dest="timeout",
		    help="Socket timeout")

    parser.add_argument("-v", '--version', action='version',
		    version="%(prog)s {0}".format(__version__) )

    return parser


def main() :

    parser = create_parser()
    args, unknown = parser.parse_known_args()

    print "Args = ", args, vars(args)
    print "unknown = ", unknown
    exit(0)

    eg = Eagle(**vars(args))
    # timeout=45,

    r = eg.get_device_data()

    print_instantdemand(r['InstantaneousDemand'])
    print

    print_currentsummation(r['CurrentSummation'])
    print

    exit(0)


def twos_comp(val, bits=32):
    """compute the 2's compliment of int value val"""
    if( (val&(1<<(bits-1))) != 0 ):
        val = val - (1<<bits)
    return val


def print_currentsummation(cs) :

    multiplier = int(cs['Multiplier'], 16)
    divisor = int(cs['Divisor'], 16)
    delivered = int(cs['SummationDelivered'], 16)
    received = int(cs['SummationReceived'], 16)

    if multiplier == 0 :
        multiplier = 1

    if divisor == 0 :
        divisor = 1

    reading_received = received * multiplier / float (divisor)
    reading_delivered = delivered * multiplier / float (divisor)

    if 'TimeStamp' in cs :
        time_stamp = to_epoch_1970(cs['TimeStamp'])
        print "{0:s} : ".format(time.asctime(time.localtime(time_stamp)))
    print "\tReceived  = {0:{width}.3f} Kw".format(reading_received, width=10)
    print "\tDelivered = {0:{width}.3f} Kw".format(reading_delivered, width=10)
    print "\t\t{0:{width}.3f} Kw".format( (reading_delivered - reading_received), width=14)


def print_instantdemand(idemand) :


    multiplier = int(idemand['Multiplier'], 16)
    divisor = int(idemand['Divisor'], 16)

#    demand = twos_comp(int(idemand['Demand'], 16))

    demand = int(idemand['Demand'], 16)

    if demand > 0x7FFFFFFF:
        demand -= 0x100000000

    if multiplier == 0 :
        multiplier = 1

    if divisor == 0 :
        divisor = 1

    reading = (demand * multiplier) / float (divisor)

    if 'TimeStamp' in idemand :
        time_stamp = to_epoch_1970(idemand['TimeStamp'])
        print "{0:s} : ".format(time.asctime(time.localtime(time_stamp)))

    print "\tDemand    = {0:{width}.3f} Kw".format(reading, width=10)
    print "\tAmps      = {0:{width}.3f}".format( ((reading * 1000) / 240), width=10)


#
if __name__ == "__main__":
    # import __main__
    # print(__main__.__file__)
    # print("syntax ok")
    main()
    exit(0)


