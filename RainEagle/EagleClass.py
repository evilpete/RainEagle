
import socket
import sys
import os
import time

__all__ = ['Eagle']

class Eagle(object) :

    def __init__(self, **kwargs):
	self.debug = kwargs.get("debug", 0)

	if self.debug :
	    print self.__class__.__name__, __name__
	self.addr = kwargs.get("addr", os.getenv('EAGLE_ADDR', None))
	self.port = kwargs.get("port", 5002)
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
	 

# command as class funtions

    def list_devices(self):
	comm_responce = self._send_comm("list_devices")
	return comm_responce

    # 3 
    def get_device_data(self, macid) :
	""" Send the GET_DEVICE_DATA command to get a data dump """
	comm_responce = self._send_comm("get_device_data", MacId=macid)
	return comm_responce

    # 10
    def get_instantaneous_demand(self, macid, interval) :
	""" Send the GET_INSTANTANEOUS_DEMAND command to get the real time demand from the meter"""
	comm_responce = self._send_comm("get_instantaneous_demand",
	    MacId=macid, Interval=interval)
	return comm_responce

    # 11
    def get_demand_values(self, macid, interval, frequency=None ) :
	""" Send the GET_DEMAND_VALUES command to get a series of instantaneous demand values"""
	kwargs = {"MacId": macid, "Interval": interval}
	if frequency :
	    kwargs["Frequency"] = frequency
	comm_responce = self._send_comm("get_demand_values", **kwargs)
	return comm_responce

    # 12
    def get_summation_values(self, macid, interval) :
	""" Send the GET_SUMMATION_VALUES command to get a series of net summation values """
	comm_responce = self._send_comm("get_summation_values",
	    MacId=macid, Interval=interval )
	return comm_responce

    # 14
    def set_fast_poll(self, macid, frequency, duration) :
	""" set the fast poll mode on the meter. """
	comm_responce = self._send_comm("get_instantaneous_demand",
	    MacId=macid, Frequency=frequency, Duration=duration)
	return comm_responce

    # 15
    def get_fast_poll_status(self, macid) :
	""" get the current status of fast poll mode. """
	comm_responce = self._send_comm("get_fast_poll_status", MacId=macid)
	return comm_responce


    # 17
    def get_history_data(self, macid, starttime, endtime=None, frequency=None ) :
	""" get a series of summation values over an interval of time """
	kwargs = {"MacId": macid, "StartTime": starttime}
	if endtime :
	    kwargs["EndTime"] = endtime
	if frequency :
	    kwargs["Frequency"] = frequency
	comm_responce = self._send_comm("get_fast_poll_status", **kwargs)
	return comm_responce

# Do nothing 
# (syntax check) 
# 
if __name__ == "__main__":
    import __main__
    print(__main__.__file__) 
 
    print("syntax ok") 
    exit(0) 
		  

