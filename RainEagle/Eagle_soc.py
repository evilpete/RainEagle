#import time
import socket
import sys
import os
import xml.etree.ElementTree as ET


from pprint import pprint

class Eagle_soc(object) :
    def __init__(self, **kwargs):

        self.macid = kwargs.get("mac", None)
        self.addr = kwargs.get("addr", os.getenv('EAGLE_HOST', None))
        self.port = kwargs.get("port", os.getenv('EAGLE_PORT', 5002))

	if self.addr is None :
	    self.addr = "eagle-000942.local"

        self.timeout = kwargs.get("timeout", 10)
	pass


    def list_devices(self, macid=None):
        """
            Send the LIST_DEVICES command
            returns information about the EAGLE device

        """
        comm_responce = self._send_soc_comm("list_devices", MacId=macid)
        if self.debug :
            print "comm_responce =", comm_responce
        if comm_responce is None:
            raise RainEagleResponseError("list_devices : Null reply")
        etree = ET.fromstring('<S>' + comm_responce + '</S>')
        rv = _et2d(etree)
#        if self.macid is None :
#            self.macid = rv['DeviceInfo']['DeviceMacId']
        return rv

    # 3
    def get_device_data(self, macid=None) :
        """ Send the GET_DEVICE_DATA command to get a data dump """
        if macid is None :
            macid = self.macid
        comm_responce = self._send_soc_comm("get_device_data", MacId=macid)
        if comm_responce is None:
            raise RainEagleResponseError("get_device_data : Null reply")
        if self.debug :
            print comm_responce
        etree = ET.fromstring('<S>' + comm_responce + '</S>')
        rv = _et2d(etree)
        return rv

    # 7
    def get_instantaneous_demand(self, macid=None) :
        """ Send the GET_INSTANTANEOUS_DEMAND command
            get the real time demand from the meter

            args:
                MacId   16 hex digits, MAC addr of EAGLE ZigBee radio
        """
        if macid is None :
            macid = self.macid
        comm_responce = self._send_soc_comm("get_instantaneous_demand",
                MacId=macid)
        if comm_responce is None:
            raise RainEagleResponseError("get_instantaneous_demand : Null reply")
        etree = ET.fromstring('<S>' + comm_responce + '</S>')
        rv = _et2d(etree)
        return rv

    # 11
    def get_demand_values(self, macid=None, interval="hour", frequency=None) :
        """ Send the GET_DEMAND_VALUES command
            get a series of instantaneous demand values

            args:
                MacId   16 hex digits, MAC addr of EAGLE ZigBee radio
                Interval        hour | day | week
                [Frequency]     int   seconds between samples
        """
        if macid is None :
            macid = self.macid
        if interval not in ['hour', 'day', 'week' ] :
            raise ValueError("get_demand_values interval must be 'hour', 'day' or 'week' ")
        kwargs = {"MacId": macid, "Interval": interval}
        if frequency :
            kwargs["Frequency"] = str(frequency)
        comm_responce = self._send_soc_comm("get_demand_values", **kwargs)
        if comm_responce is None:
            raise RainEagleResponseError("get_demand_values : Null reply")
        etree = ET.fromstring('<S>' + comm_responce + '</S>')
        rv = _et2d(etree)
        return rv

    # 12
    def get_summation_values(self, macid=None, interval="day") :
        """ Send the GET_SUMMATION_VALUES command
            get a series of net summation values

            args:
                MacId   16 hex digits, MAC addr of EAGLE ZigBee radio
                Interval        day | week | month | year
        """
        if macid is None :
            macid = self.macid
        if interval not in ['day', 'week', 'month', 'year'] :
            raise ValueError("get_summation_values interval must be 'day', 'week', 'month' or 'year'")
        comm_responce = self._send_soc_comm("get_summation_values",
            MacId=macid, Interval=interval)
        if comm_responce is None:
            raise RainEagleResponseError("get_summation_values : Null reply")
        etree = ET.fromstring('<S>' + comm_responce + '</S>')
        rv = _et2d(etree)
        return rv


    # 14
    def set_fast_poll(self, macid=None, frequency="0x04", duration="0xFF") :
        """ Send the SET_FAST_POLL command
            set the fast poll mode on the meter

            args:
                MacId   16 hex digits, MAC addr of EAGLE ZigBee radio
                Frequency       0x01 - 0xFF     Freq to poll meter, in seconds
                Duration        0x00 - 0x0F     Duration of fast poll mode, in minutes (max 15)
        """
        if macid is None :
            macid = self.macid
        frequency = _tohex(frequency, 2)
        duration = _tohex(duration, 2)

        comm_responce = self._send_soc_comm("get_instantaneous_demand",
            MacId=macid, Frequency=frequency, Duration=duration)
        if comm_responce is None:
            raise RainEagleResponseError("set_fast_poll : Null reply")
        etree = ET.fromstring('<S>' + comm_responce + '</S>')
        rv = _et2d(etree)
        return rv

    # 15
    def get_fast_poll_status(self, macid=None) :
        """ Send the GET_FAST_POLL_STATUS command
            get the current status of fast poll mode.

            args:
                MacId   16 hex digits, MAC addr of EAGLE ZigBee radio
        """
        if macid is None :
            macid = self.macid
        comm_responce = self._send_soc_comm("get_fast_poll_status", MacId=macid)
        if comm_responce is None:
            return None
        etree = ET.fromstring('<S>' + comm_responce + '</S>')
        rv = _et2d(etree)

        return rv

    # 17
    # needs to be rewritten to stream the data via iter
    def get_history_data(self, macid=None, starttime="0x00000000", endtime=None, frequency=None) :
        """ Send the GET_HISTORY_DATA command
            get a series of summation values over an interval of time
            ( socket command api )

            args:
                MacId   16 hex digits, MAC addr of EAGLE ZigBee radio
                StartTime       the start of the history interval (default oldest sample)
                EndTime         the end of the history interval (default current time)
                Frequency       Requested number of seconds between samples.
        """
        if macid is None :
            macid = self.macid
        kwargs = {"MacId": macid}
        kwargs["StartTime"] = _tohex(starttime, 8)
        if endtime :
            kwargs["EndTime"] = _tohex(endtime, 8)
        if frequency :
            kwargs["Frequency"] = _tohex(endtime, 4)
        comm_responce = self._send_soc_comm("get_history_data", **kwargs)
        if comm_responce is None :
            raise RainEagleResponseError("get_history_data : Null reply")
        etree = ET.fromstring('<S>' + comm_responce + '</S>')
        rv = _et2d(etree)
        return rv

    def _send_soc_comm(self, cmd, **kwargs):

        if cmd == "set_fast_poll" :
            command_tag = "RavenCommand"
        else :
            command_tag = "LocalCommand"

	macid = kwargs.get("MacId", self.macid)


        commstr = "<{0}>\n ".format(command_tag)
        commstr += "<Name>{0!s}</Name>\n".format(cmd)
	if macid is not None :
	    commstr += "<MacId>{0!s}</MacId>\n".format(macid)
        for k, v in kwargs.items() :
	    if k is "MacId" :
		continue
            commstr += "<{0}>{1!s}</{0}>\n".format(k, v)
        commstr += "</{0}>\n".format(command_tag)
        replystr = ""
        # buf_list = []

        try:
            self._connect()

            # if cmd == "get_history_data" :
        #       self.soc.settimeout(45)
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

    def _connect(self) :
        self.soc = socket.create_connection(
                (self.addr, self.port), self.timeout)

    def _disconnect(self):
        try :
            if self.soc :
                self.soc.close()
                self.soc = False
        except IOError :
            pass



