

__author__ = 'Peter Shipley <peter.shipley@gmail.com>'
__copyright__ = "Copyright (C) 2014 Peter Shipley" 
__license__ = "BSD"

import socket
import sys
import os
import time
import xml.etree.ElementTree as ET
import urllib
import urllib2
from math import floor
from urlparse import urlparse
import json



from pprint import pprint
 

api_arg_format = {

}

__all__ = ['Eagle', 'to_epoch_1970, to_epoch_2000']

def to_epoch_2000(t) :
    """ converts time stored as
	to unix's epoch of 1970
	offset in seconds from "Jan 1 00:00:00 2000"
    """
    if isinstance(t, time.struct_time ) :
	t = time.mktime(t)
    return t - 946684800


def to_epoch_1970(t) :
    """ converts time stored as
	offset in seconds from "Jan 1 00:00:00 2000"
	to unix's epoch of 1970
    """
    if isinstance(t, (int, long, float) ) :
	return t + 946684800
    if isinstance(t, str) and t.startswith('0x') :
	return 946684800 + int(t, 16)

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

def _tohex(n, width=10) :
    """ convert arg to string with hex representation if possible"""
    if isinstance(n, str) :
	if n.isdigit() :
	    return "{:#{width}x}".format(int(n), width=width)
	else :
	    return n
    if isinstance(n, (int, long) ) :
	return "{:#{width}x}".format(n, width=width)
    if isinstance(n, float) :
	return "{:#{width}x}".format(int(n), width=width)
    return n



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



# socket commands as class functions

    def list_devices(self):
	comm_responce = self._send_soc_comm("list_devices")
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
	comm_responce = self._send_soc_comm("get_device_data", MacId=macid)
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
	comm_responce = self._send_soc_comm("get_instantaneous_demand",
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
	if interval not in ['hour', 'day', 'week' ] :
	    raise ValueError("set_time_source interval must be 'hour', 'day' or 'week' ")
	kwargs = {"MacId": macid, "Interval": interval}
	if frequency :
	    kwargs["Frequency"] = str(frequency)
	comm_responce = self._send_soc_comm("get_demand_values", **kwargs)
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
	if interval not in ['day', 'week', 'month', 'year'] :
	    raise ValueError("set_time_source interval must be 'day', 'week', 'month' or 'year'")
	comm_responce = self._send_soc_comm("get_summation_values",
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
	frequency = _tohex(frequency, 4)
	duration = _tohex(duration, 4)

	comm_responce = self._send_soc_comm("get_instantaneous_demand",
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
	comm_responce = self._send_soc_comm("get_fast_poll_status", MacId=macid)
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
	kwargs = {"MacId": macid,}
	kwargs["StartTime"] = _tohex(starttime, 10)
	if endtime :
	    kwargs["EndTime"] = _tohex(endtime, 10)
	if frequency :
	    kwargs["Frequency"] =  _tohex(endtime, 6)
	comm_responce = self._send_soc_comm("get_history_data", **kwargs)
	if comm_responce == None :
	    return None
	etree = ET.fromstring('<S>' + comm_responce + '</S>' )
	rv = _et2d(etree)
	return rv


# http commands as class functions

    def get_setting_data(self) :
	"""
	    get settings
	"""
	comm_responce = self._send_http_comm("get_setting_data")
	return comm_responce

    def get_device_config(self) :
	"""
	    get configs
	"""
	comm_responce = self._send_http_comm("get_device_config")
	return comm_responce

    def get_timezone(self) :
	"""
	    get current timezone configuration
	"""
	comm_responce = self._send_http_comm("get_timezone")
	return comm_responce

    def get_time_source(self, macid=None) :
	"""
	    get time source for device 
	    retrrns value "meter" or "nternet"
	"""
	comm_responce = self._send_http_comm("get_time_source")
	return comm_responce

    def set_remote_management(self, macid=None, status=None) :
	""" set_remote_management
	    enabling ssh & vpn

	    args:
		status		yes|no

	"""
	if status not in ['yes', 'no'] :
	    raise ValueError("set_remote_management status must be 'yes' or 'no'")
	comm_responce = self._send_http_comm("set_remote_management", Status=status)
	return comm_responce


    def set_time_source(self, macid=None, source=None) :
	""" set_time_source
	    set time source

	    args:
		source		meter|internet
	"""
	if status not in ['meter', 'internet'] :
	    raise ValueError("set_time_source Source must be 'meter' or 'internet'")
	comm_responce = self._send_http_comm("set_time_source", Source=source)
	return comm_responce

    def get_price(self) :
	"""
	    get price for kWh
	"""
	comm_responce = self._send_http_comm("get_price")
	return comm_responce

    def set_price(self, price) :
	"""
	    Set price manualy 

	    args:
		price		Price/kWh
	"""
	#if isinstance(price, str) :
	#    price = float(price.lstrip('$'))

	if not isinstance(price, (int, long, float) ) : 
	    raise ValueError("set_price price arg must me a int, long or float")

	trailing_digits     = 0
	multiplier          = 1
	while (((price * multiplier) != (floor(price * multiplier))) and (trailing_digits < 7) ) :
	    trailing_digits += 1
	    multiplier *= 10

	price_adj = "{:#x}".format( int(price * multiplier) )
	tdigits = "{:#x}".format(  trailing_digits )

	comm_responce = self._send_http_comm("set_price", Price=price_adj, TrailingDigits=tdigits)
	return comm_responce


    def set_price_auto(self) :
	"""
	    Set Price from Meter
	"""
	comm_responce = self._send_http_comm("set_price",
	    Price="0xFFFFFFFF",
	    TrailingDigits="0x00")
	return comm_responce

    def factory_reset(self) :
	"""
	    Factory Reset
	"""
	comm_responce = self._send_http_comm("factory_reset")
	return comm_responce


#    def disconnect_meter(self) :
#	"""
#	    disconnect from Smart Meter
#	"""
#	comm_responce = self._send_http_comm("disconnect_meter")
#	return comm_responce



    def cloud_reset(self) :
	"""
	    cloud_reset : Clear Cloud Configuration
	"""
	comm_responce = self._send_http_comm("cloud_reset")
	return comm_responce


    def set_cloud(self, url) :
	"""
	    set cloud Url
	"""
	if url.__len__() > 200 :
	    raise ValueError("Max URL length is 200 characters long.\n")

	urlp = urlparse(url)

	if urlp.port :
	    port = "{:#4x}".format(urlp.port)
	else :
	    port = "0x00"

	hostname = urlp.hostname

	if urlp.scheme :
	    protocol = urlp.scheme
	else :
	    protocol = "http"

	url = urlp.path


	if urlp.username :
	    userid = urlp.username
	else :
	    userid = ""

	if urlp.password :
	    password = urlp.password
	else :
	    password = ""

	comm_responce = self._send_http_comm("set_cloud",
	    Provider="manual",
	    Protocol=protocol, HostName=hostname,
	    Url=url, Port=port,
	    AuthCode="", Email="",
            UserId=userid, Password=password)

	return comm_responce
	    




# Support functions

    def _connect(self) :
	self.soc = socket.create_connection( (self.addr, self.port), self.timeout)

    def _disconnect(self):
        try :
            if self.soc :
                self.soc.close()
                self.soc = False
        except IOError :
            pass


    def _send_http_comm(self, cmd, **kwargs):

	print "\n\n_send_http_comm : ", cmd

	commstr = "<LocalCommand>\n"
	commstr += "<Name>{0!s}</Name>\n".format(cmd)
	commstr += "<MacId>{0!s}</MacId>\n".format(self.macid)
	for k, v in kwargs.items() :
	    commstr += "<{0}>{1!s}</{0}>\n".format(k, v)
	commstr += "</LocalCommand>\n"

	print(commstr)

	url = "http://{0}/cgi-bin/cgi_manager".format(self.addr)

	req = urllib2.Request(url, commstr)
	response = urllib2.urlopen(req)
	the_page = response.read()

	return the_page



    def _send_soc_comm(self, cmd, **kwargs):

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
	# buf_list = []

	try:
	    self._connect()

	    # if cmd == "get_history_data" :
	# 	self.soc.settimeout(45)
	    self.soc.sendall(commstr)
	    if self.debug :
		print "commstr : \n", commstr

	    # time.sleep(1)

	    while 1 :
		buf = self.soc.recv(1000)
		if not buf:
		    break
		replystr += buf
		#buf_list.append(buf)
	    # replystr = ''.join(buf_list)

	except Exception:
	    print("Unexpected error:", sys.exc_info()[0])
	    print "Error replystr = ", replystr
	    replystr = None
	finally:
	    self._disconnect()
	    if self.debug > 1 :
		print "_send_soc_comm replystr :\n", replystr
	    return replystr 


# Do nothing 
# (syntax check) 
# 
if __name__ == "__main__":
    import __main__
    print(__main__.__file__) 
 
    print("syntax ok") 
    exit(0) 
		  

