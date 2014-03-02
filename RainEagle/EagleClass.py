
import socket
import sys
import os
import time
import xml.etree.ElementTree as ET


__all__ = ['Eagle']

def et2d(et) :
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
		    d[child.tag].append(et2d(child))
		else :
		    d[child.tag] = et2d(child)
	    else :
		if child.tag in d :
		    d[child.tag].append(child.text)
		else :
		    d[child.tag] = child.text
    return d



#
# Simple Base class for ISY Class
class Eagle(object) :

    def __init__(self, **kwargs):
	self.debug = kwargs.get("debug", 0)

	if self.debug :
	    print self.__class__.__name__, __name__
	self.addr = kwargs.get("addr", os.getenv('EAGLE_ADDR', None))
	self.port = kwargs.get("port", os.getenv('EAGLE_PORT', 5002))
	self.soc = None


    def connect(self) :
	self.soc = socket.create_connection( (self.addr, self.port), 10)

#	self.soc_rf = self.soc.makefile("rb")
#	self.soc_wf = self.soc.makefile("wb")

    def disconnect(self):

#        try :
#            if self.soc_rf :
#                self.soc_rf.close()
#                self.soc_rf = False
#        except IOError :
#            pass
# 
#        try :
#            if self.soc_wf :
#                self.soc_wf.close()
#                self.soc_wf = False
#        except IOError :
#            pass
# 
        try :
            if self.soc :
                self.soc_sock.close()
                self.soc_sock = False
        except IOError :
            pass

    def _reconnect(self):
        self.disconnect()
        self.connect()


    def _send_comm(self, cmd, **kwargs):

	commstr = "<LocalCommand>\r\n "
	commstr += "<Name>{0!s}</Name>\r\n".format(cmd)
	for k, v in kwargs.items() :
	    commstr += "<{0}>{1!s}</{0}>\r\n".format(k, v)
	commstr += "</LocalCommand>\r\n"

#+	 self.soc.send(commstr)
	print "commstr : ", commstr

#	self.soc_wf.write(commstr)
#	self.soc_wf.flush()

#+	time.sleep(1)

	replystr = ""
#+	while 1 :
#+	    buf = self.soc.recv(1000)
#+	    if not buf:
#+		break
#+	    replystr += buf

	return replystr 
	 

# commands as class funtions

    def list_devices(self):
	comm_responce = self._send_comm("list_devices")
	# temp debug data
	comm_responce = "<DeviceInfo>" \
	    "    <DeviceMacId>0xd8d5b90000000xxx</DeviceMacId>" \
	    "    <InstallCode>0x9ac4382dffa81xxx</InstallCode>" \
	    "    <LinkKeyHigh>7e572b66c5b444xxx</LinkKeyHigh>" \
	    "    <LinkKeyLow>94227dca4e773xxx</LinkKeyLow>" \
	    "    <FWVersion>1.4.27 (5278)</FWVersion>" \
	    "    <HWVersion>1.2.3</HWVersion>" \
	    "    <Manufacturer>Rainforest Automation, I</Manufacturer>" \
	    "    <ModelId>RFA-Z109 EAGLE</ModelId>" \
	    "    <DateCode>20130308PO020621</DateCode>" \
	    "</DeviceInfo>\n" 

	etree = ET.fromstring('<S>' + comm_responce + '</S>' )
	rv = et2d(etree)
	return rv

    # 3 
    def get_device_data(self, macid) :
	""" Send the GET_DEVICE_DATA command to get a data dump """
	comm_responce = self._send_comm("get_device_data", MacId=macid)
	# temp debug data
	comm_responce = "<NetworkInfo>" \
	    "  <DeviceMacId>0xd8d5b90000000xxx</DeviceMacId>" \
	    "  <Status>Rejoining</Status>" \
	    "  <MeterMacId>0x001350030011bxxx</MeterMacId>" \
	    "  <ExtPanId>0x7fffffffffffffff</ExtPanId>" \
	    "  <ShortAddr>0x0000ffff</ShortAddr>" \
	    "  <Channel>24</Channel>" \
	    "  <LinkStrength>156</LinkStrength>" \
	    "</NetworkInfo>" \
	    "<DeviceInfo>" \
	    "  <DeviceMacId>0xd8d5b90000000xxx</DeviceMacId>" \
	    "  <InstallCode>0x9ac4382dffa81xxx</InstallCode>" \
	    "  <LinkKeyHigh>7e572b66c5b44xxx</LinkKeyHigh>" \
	    "  <LinkKeyLow>94227dca4e773xxx</LinkKeyLow>" \
	    "  <FWVersion>1.4.27 (5278)</FWVersion>" \
	    "  <HWVersion>1.2.3</HWVersion>" \
	    "  <Manufacturer>Rainforest Automation, I</Manufacturer>" \
	    "  <ModelId>RFA-Z109 EAGLE</ModelId>" \
	    "  <DateCode>20130308PO020621</DateCode>" \
	    "</DeviceInfo>" \
	    "<InstantaneousDemand>" \
	    "  <DeviceMacId>0xd8d5b90000000xxx</DeviceMacId>" \
	    "  <MeterMacId>0x001350030011bxxx</MeterMacId>" \
	    "  <Demand>0x00000bf1</Demand>" \
	    "  <TimeStamp>0x195193e3</TimeStamp>" \
	    "  <Multiplier>0x00000001</Multiplier>" \
	    "  <Divisor>0x000003e8</Divisor>" \
	    "  <DigitsRight>0x00000003</DigitsRight>" \
	    "  <DigitsLeft>0x0000000f</DigitsLeft>" \
	    "  <SuppressLeadingZero>0x0001</SuppressLeadingZero>" \
	    "</InstantaneousDemand>" 

	etree = ET.fromstring('<S>' + comm_responce + '</S>' )
	rv = et2d(etree)
	return rv

    # 10
    def get_instantaneous_demand(self, macid, interval) :
	""" Send the GET_INSTANTANEOUS_DEMAND command to get the real time demand from the meter"""
	comm_responce = self._send_comm("get_instantaneous_demand",
	    MacId=macid, Interval=interval)
	etree = ET.fromstring('<S>' + comm_responce + '</S>' )
	rv = et2d(etree)
	return rv

    # 11
    def get_demand_values(self, macid, interval, frequency=None ) :
	""" Send the GET_DEMAND_VALUES command to get a series of instantaneous demand values"""
	kwargs = {"MacId": macid, "Interval": interval}
	if frequency :
	    kwargs["Frequency"] = frequency
	comm_responce = self._send_comm("get_demand_values", **kwargs)
	etree = ET.fromstring('<S>' + comm_responce + '</S>' )
	rv = et2d(etree)
	return rv

    # 12
    def get_summation_values(self, macid, interval) :
	""" Send the GET_SUMMATION_VALUES command to get a series of net summation values """
	comm_responce = self._send_comm("get_summation_values",
	    MacId=macid, Interval=interval )
	etree = ET.fromstring('<S>' + comm_responce + '</S>' )
	rv = et2d(etree)
	return rv

    # 14
    def set_fast_poll(self, macid, frequency, duration) :
	""" set the fast poll mode on the meter. """
	comm_responce = self._send_comm("get_instantaneous_demand",
	    MacId=macid, Frequency=frequency, Duration=duration)
	etree = ET.fromstring('<S>' + comm_responce + '</S>' )
	rv = et2d(etree)
	return rv

    # 15
    def get_fast_poll_status(self, macid) :
	""" get the current status of fast poll mode. """
	comm_responce = self._send_comm("get_fast_poll_status", MacId=macid)
	etree = ET.fromstring('<S>' + comm_responce + '</S>' )
	rv = et2d(etree)
	return rv


    # 17
    def get_history_data(self, macid, starttime, endtime=None, frequency=None ) :
	""" get a series of summation values over an interval of time """
	kwargs = {"MacId": macid, "StartTime": starttime}
	if endtime :
	    kwargs["EndTime"] = endtime
	if frequency :
	    kwargs["Frequency"] = frequency
	comm_responce = self._send_comm("get_fast_poll_status", **kwargs)
	etree = ET.fromstring('<S>' + comm_responce + '</S>' )
	rv = et2d(etree)
	return rv

# Do nothing 
# (syntax check) 
# 
if __name__ == "__main__":
    import __main__
    print(__main__.__file__) 
 
    print("syntax ok") 
    exit(0) 
		  

