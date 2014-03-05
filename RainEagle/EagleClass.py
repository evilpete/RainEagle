

__author__ = 'Peter Shipley <peter.shipley@gmail.com>'
__copyright__ = "Copyright (C) 2014 Peter Shipley" 
__license__ = "BSD"

import socket
import sys
import os
import time
import xml.etree.ElementTree as ET

from pprint import pprint
 
  


__all__ = ['Eagle']

def _et2d(et) :

    """ Etree to Dict

	converts an ETree to a Dict Tree
	lists are created for duplicate tag

	if there are multiple XML of the name name
	an list array is used
	attrib tags are converted to "tag_name" + "attrib_name"

	if an invalid arg is passed a empty dict is retrurned


	arg: ETree Element  obj

	returns: a dict obj
    """
    d = dict()
    if not isinstance(et, ET.Element) :
	return d
    children = list(et)
    if et.attrib :
	for k, v in list(et.items()) :
	    d[et.tag + "-" + k] =  v
    if children :
	for child in children :
	    if child.tag in d :
		if type(d[child.tag]) != list :
		    t = d[child.tag]
		    d[child.tag] = [t]
	    if list(child) or child.attrib :
		if child.tag in d :
		    d[child.tag].append(_et2d(child))
		else :
		    d[child.tag] = _et2d(child)
	    else :
		if child.tag in d :
		    d[child.tag].append(child.text)
		else :
		    d[child.tag] = child.text
    return d



#
class Eagle(object) :
    """
	Class for talking to Rainforest Automation EAGLE (RFA-Z109)

	args:
	    debug	print debug messages if true
	    addr	address of device
	    port	port on device (default 5002)
	    getmac	connect to device at start up and get macid (default true)

	Currently there is very little error handling ( if any at all )
    """
    def __init__(self, **kwargs):
	self.debug = kwargs.get("debug", 0)

	if self.debug :
	    print self.__class__.__name__, __name__
	self.addr = kwargs.get("addr", os.getenv('EAGLE_ADDR', None))
	self.port = kwargs.get("port", os.getenv('EAGLE_PORT', 5002))
	self.getmac = kwargs.get("getmac", True)
	self.timeout = kwargs.get("timeout", 10)
	self.soc = None
	self.macid = None

	if self.debug :
	    print "Addr :  = ", self.addr
	    print "timeout :  = ", self.timeout
	    print "debug :  = ", self.debug

	# preload
	if self.getmac :
	    self.device_info = self.list_devices()
	    if self.device_info == None :
		raise IOError("Error connecting")
	    if self.debug :
		print "__init__ ",
		pprint(self.device_info)
	    # self.macid =  self.device_info['DeviceInfo']['DeviceMacId']
	    if self.debug :
		print "Init DeviceMacId = ", self.macid



# commands as class funtions

    def list_devices(self):
	comm_responce = self._send_comm("list_devices")
	if self.debug :
	    print "comm_responce =", comm_responce
	if comm_responce == None:
	    return None
	etree = ET.fromstring('<S>' + comm_responce + '</S>' )
	rv = _et2d(etree)
	if self.macid == None :
	    self.macid =  rv['DeviceInfo']['DeviceMacId']
	return rv

    # 3 
    def get_device_data(self, macid=None) :
	""" Send the GET_DEVICE_DATA command to get a data dump """
	if macid == None :
	    macid = self.macid
	comm_responce = self._send_comm("get_device_data", MacId=macid)
	if comm_responce == None:
	    return None
	etree = ET.fromstring('<S>' + comm_responce + '</S>' )
	rv = _et2d(etree)
	return rv

    # 10
    def get_instantaneous_demand(self, macid=None) :
	""" Send the GET_INSTANTANEOUS_DEMAND command
	    get the real time demand from the meter

	    args:
		MacId	16 hex digits, MAC addr of EAGLE ZigBee radio
        """
	if macid == None :
	    macid = self.macid
	comm_responce = self._send_comm("get_instantaneous_demand",
		MacId=macid)
	if comm_responce == None:
	    return None
	etree = ET.fromstring('<S>' + comm_responce + '</S>' )
	rv = _et2d(etree)
	return rv

    # 11
    def get_demand_values(self, macid=None, interval="hour", frequency=None ) :
	""" Send the GET_DEMAND_VALUES command 
	    get a series of instantaneous demand values

	    args:
		MacId	16 hex digits, MAC addr of EAGLE ZigBee radio
		Interval	hour | day | week
		[Frequency]	int   seconds between samples
        """
	if macid == None :
	    macid = self.macid
	kwargs = {"MacId": macid, "Interval": interval}
	if frequency :
	    kwargs["Frequency"] = frequency
	comm_responce = self._send_comm("get_demand_values", **kwargs)
	if comm_responce == None:
	    return None
	etree = ET.fromstring('<S>' + comm_responce + '</S>' )
	rv = _et2d(etree)
	return rv

    # 12
    def get_summation_values(self, macid=None, interval="day") :
	""" Send the GET_SUMMATION_VALUES command 
	    get a series of net summation values

	    args:
		MacId	16 hex digits, MAC addr of EAGLE ZigBee radio
		Interval	day | week | month | year
        """
	if macid == None :
	    macid = self.macid
	comm_responce = self._send_comm("get_summation_values",
	    MacId=macid, Interval=interval )
	if comm_responce == None:
	    return None
	etree = ET.fromstring('<S>' + comm_responce + '</S>' )
	rv = _et2d(etree)
	return rv

    # 14
    def set_fast_poll(self, macid=None, frequency="0x04", duration="0xFF") :
	""" Send the SET_FAST_POLL command
	    set the fast poll mode on the meter

	    args:
		MacId	16 hex digits, MAC addr of EAGLE ZigBee radio
		Frequency	0x01 - 0xFF	Freq to poll meter, in seconds
		Duration	0x00 - 0x0F	Duration of fast poll mode, in minutes (max 15) 
	"""
	if macid == None :
	    macid = self.macid
	if isinstance(frequency, int) :
	    frequency = "{:#04x}".format(m)
	if isinstance(duration, int) :
	    frequency = "{:#04x}".format(m)

	comm_responce = self._send_comm("get_instantaneous_demand",
	    MacId=macid, Frequency=frequency, Duration=duration)
	if comm_responce == None:
	    return None
	etree = ET.fromstring('<S>' + comm_responce + '</S>' )
	rv = _et2d(etree)
	return rv

    # 15
    def get_fast_poll_status(self, macid=None) :
	""" Send the GET_FAST_POLL_STATUS command
	    get the current status of fast poll mode.

	    args:
		MacId	16 hex digits, MAC addr of EAGLE ZigBee radio
	"""
	if macid == None :
	    macid = self.macid
	comm_responce = self._send_comm("get_fast_poll_status", MacId=macid)
	if comm_responce == None:
	    return None
	etree = ET.fromstring('<S>' + comm_responce + '</S>' )
	rv = _et2d(etree)
	return rv


    # 17
    def get_history_data(self, macid=None, starttime="0x00000000", endtime=None, frequency=None ) :
	""" Send the GET_HISTORY_DATA command
	    get a series of summation values over an interval of time

	    args:
		MacId	16 hex digits, MAC addr of EAGLE ZigBee radio
		StartTime	the start of the history interval (default oldest sample)
		EndTime		the end of the history interval (default current time)
		Frequency	Requested number of seconds between samples.
	"""
	if macid == None :
	    macid = self.macid
	kwargs = {"MacId": macid, "StartTime": starttime}
	if endtime :
	    kwargs["EndTime"] = endtime
	if frequency :
	    kwargs["Frequency"] = frequency
	comm_responce = self._send_comm("get_history_data", **kwargs)
	if comm_responce == None :
	    return None
	etree = ET.fromstring('<S>' + comm_responce + '</S>' )
	rv = _et2d(etree)
	return rv


    # Support functions

    def _connect(self) :
	self.soc = socket.create_connection( (self.addr, self.port), 10)

    def _disconnect(self):
        try :
            if self.soc :
                self.soc.close()
                self.soc = False
        except IOError :
            pass


    def _send_comm(self, cmd, **kwargs):

	if cmd == "set_fast_poll" :
	    command_tag = "RavenCommand"
	else :
	    command_tag = "LocalCommand"


	commstr = "<{0}>\n ".format(command_tag)
	commstr += "<Name>{0!s}</Name>\n".format(cmd)
	for k, v in kwargs.items() :
	    commstr += "<{0}>{1!s}</{0}>\n".format(k, v)
	commstr += "</{0}>\n".format(command_tag)
	replystr = ""

	try:
	    self._connect()

	    if cmd == "get_history_data" :
		self.soc.settimeout(45)
	    self.soc.sendall(commstr)
	    if self.debug :
		print "commstr : \n", commstr

	    # time.sleep(1)

	    while 1 :
		buf = self.soc.recv(1000)
		if not buf:
		    break
		replystr += buf

	except Exception:
	    print("Unexpected error:", sys.exc_info()[0])
	    print "Error replystr = ", replystr
	    replystr = None
	finally:
	    self._disconnect()
	    if self.debug > 1 :
		print "_send_comm replystr :\n", replystr
	    return replystr 

    def to_unix_time(self, t) :
	""" converts time stored as
	    offset in seconds from "Jan 1 00:00:00 2000"
	    to unix's epoch of 1970
	"""
	if isinstance(t, (int, long, float) ) :
	    return t + 946684800
	if isinstance(t, str) and t.startswith('0x') :
	    return 946684800 + int(t, 16)

# Do nothing 
# (syntax check) 
# 
if __name__ == "__main__":
    import __main__
    print(__main__.__file__) 
 
    print("syntax ok") 
    exit(0) 
		  

