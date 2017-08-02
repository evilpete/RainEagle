
import os
#import time
#import xml.etree.ElementTree as ET
# import urllib
import urllib2
#iimport base64
import json
from pprint import pprint
# import ssl
from RainEagle.Eagle_util import _get_config, _tohex


__all__ = ['Eagle_cloud']


class Eagle_cloud(object):

    def __init__(self, **kwargs):

        self.debug = kwargs.get("debug", 0)
        self.network_info = None

        config = _get_config(opt="cloud")
        pprint(config)

        self.cloud_url = config.get("url", "https://rainforestcloud.com:9445/cgi-bin/post_manager")

        #self.cloud_url = "https://10.1.1.39/cgi-bin/post_manager"

        self.icode = kwargs.get("icode",
                                os.getenv('EAGLE_ICODE',
                                          config.get("icode", None)))

        self.macid = kwargs.get("mac",
                                config.get("mac", None))

        self.cloudemail = kwargs.get("username",
                                     os.getenv('EAGLE_EMAIL',
                                               config.get("username", None)))

        self.cloudid = kwargs.get("cloudid",
                                  os.getenv('EAGLE_CLOUDID',
                                            config.get("cloudid", None)))

        self.cloudpass = kwargs.get("cloudpass",
                                    os.getenv('EAGLE_CLOUDPASS',
                                              config.get("cloudpass", None)))


        # preload
        if self.macid is None:
            self.macid = self.getmacid()
            if self.debug:
                print "Init Cloud DeviceMacId = ", self.macid

        if self.icode is None:
            self.icode = self.getinstallcode()
            if self.debug:
                print "Init Cloud DeviceMacId = ", self.macid

        # _save_config(opt=self.cloudid, mac=self.macid, icode=self.icode)

    def getmacid(self):
        if self.macid is not None:
            return self.macid

        if self.network_info is None:
            self.network_info = self.get_network_info()

        if self.network_info is not None and  'DeviceMacId' in self.network_info:
            return self.network_info['DeviceMacId']

        return None

    def getinstallcode(self):
        if self.icode is not None:
            return self.icode

        if self.network_info is None:
            self.network_info = self.get_network_info()

        if self.network_info is not None and  'InstallCode' in self.network_info:
            return self.network_info['InstallCode']

        return None


    # 1
    def get_network_info(self, macid=None, protocol=None):
        """
            get network Status
            args:
                macid           MAC Address of ZigBee radio
                protocol        Type of network interface (only ZigBee supported)
            get network info

            On Success returns dict with value containing setting

        """
        d = dict()
        if macid is not None:
            d["MacId"] = macid
        if protocol is not None:
            d["Protocol"] = protocol

        comm_responce = self._send_cloud_comm("get_network_info", **d)
        print "comm_responce", len(comm_responce)
        if comm_responce is None or len(comm_responce) == 0:
            return None

        r = json.loads(comm_responce)
        if 'NetworkInfo' in r:
            return r['NetworkInfo']

        return None

    # 3
    def list_network(self, macid=None):
        comm_responce = self._send_cloud_comm("list_network")
        ### HACK ALERT
        if comm_responce[0] != "{":
            comm_responce = "{" + comm_responce + "}"
        if comm_responce is None or len(comm_responce) == 0:
            return None

        r = json.loads(comm_responce)
        if 'NetworkList' in r:
            return r['NetworkList']

        return None

    #1
    def get_network_status(self, protocol="ZigBee", macid=None):
        """
            get network Status
            args:
                macid           MAC Address of ZigBee radio
                protocol        Type of network interface (only ZigBee supported)

            On Success returns dict with values containing settings
        """
        return self._call_cloud("get_network_status", "NetworkStatus", macid=macid, protocol=protocol)


    def get_instantaneous_demand(self, macid=None):
        d = dict()
        if self.macid is not None:
            d["MacId"] = macid
        comm_responce = self._send_cloud_comm("get_instantaneous_demand", **d)
        # MacId=macid)
        if comm_responce is None or len(comm_responce) == 0:
            return None

        r = json.loads(comm_responce)
        if 'InstantaneousDemand' in r:
            return r['InstantaneousDemand']

        return None

    def get_price(self, macid=None):
        """
            get price information from the meter
        """
        return self._call_cloud("get_price", "PriceCluster", macid)

    def get_message(self, macid=None):
        """
            get the current text message from the meter
        """
        return self._call_cloud("get_message", "MessageCluster", macid)

    def confirm_message(self, macid=None):
        """
            confirm_message

            confirm the message as indicated by the ID
            get network Status
            args:
                macid           MAC Address of ZigBee radio
                ID              Message ID to confirm (in hex)

        """
        d = dict()
        if macid is not None:
            d["macid"] = macid
        elif self.macid is not None:
            d["macid"] = self.macid
        comm_responce = self._send_cloud_comm("confirm_message", **d)
        return json.loads(comm_responce)

    # 16
    def get_history_data(self, macid=None, StartTime=0x00000000, EndTime=None, Frequency=None):
        """
            get_history_data

            Get a series of summation values over an interval of time

            args:
                macid          MAC Address of ZigBee radio
                StartTime      UTC Time in hex (offset in seconds from 00:00:00 01Jan2000)
                EndTime        UTC Time in hex (offset in seconds from 00:00:00 01Jan2000)
                Frequency      Requested number of seconds between samples

            On Success returns dict with values
        """
        d = dict()

        if macid is not None:
            d["macid"] = macid
        elif self.macid is not None:
            d["macid"] = self.macid

        # TODO add support for time isinstance class
        if StartTime is not None:
            if isinstance(StartTime, int):
                d["StartTime"] = _tohex(StartTime, 8)
            else:
                d["StartTime"] = StartTime

        if EndTime is not None:
            if isinstance(EndTime, int):
                d["EndTime"] = _tohex(EndTime, 8)
            else:
                d["EndTime"] = EndTime

        if Frequency is not None:
            if isinstance(Frequency, int):
                d["Frequency"] = _tohex(Frequency, 4)
            else:
                d["Frequency"] = Frequency

        comm_responce = self._send_cloud_comm("get_history_data", **d)
        print "\n\n=====\ncomm_responce :", comm_responce,"\n=====\n"
        ### HACK ALERT
        if comm_responce[0] != "{":
            comm_responce = "{" + comm_responce + "}"
        # return json.loads(comm_responce)
        # comm_responce is None or not comm_responce:
        if comm_responce is None or len(comm_responce) == 0:
            return None

        r = json.loads(comm_responce)
        if 'HistoryData' in r:
            return r['HistoryData']

        return None

    def set_schedule(self, macid=None, Event=None, Frequency=0x0a, Enabled=None):
        """
            set_schedule

            the set_schedule command to change how the EAGLE polls the meter. The rate at
            which each type of meter reading is polled can be set pass

            args:
                macid          MAC Address of ZigBee radio
                Event          Type of meter reading to schedule
                Frequency      Frequency to poll meter, in seconds (in hex)
                Enabled        Set or Disable polling  (Y|N)

               Valid Event Values:
                    time | message | price | summation |
                    demand | scheduled_prices |
                    profile_data | billing_period | block_period

        """
        d = dict()

        if macid is not None:
            d["DeviceMacId"] = macid
        elif self.macid is not None:
            d["DeviceMacId"] = self.macid

        if Event is not None:
            d["Event"] = Event

        if Frequency is not None:
            if isinstance(Frequency, int):
                d["Frequency"] = _tohex(Frequency, 4)
            else:
                d["Frequency"] = Frequency

        if Enabled is None:
            raise ValueError("\"configure_mdns\" Invalid arg value for 'enabled'")
        if Enabled is True:
            Enabled = 'Y'
        elif Enabled is False:
            Enabled = 'N'

        d["Enabled"] = Enabled
        comm_responce = self._send_cloud_comm("get_schedule", **d)
        # print "comm_responce = ", comm_responce
        ### HACK ALERT
        if comm_responce[0] != "{":
            comm_responce = "{" + comm_responce + "}"
        # return json.loads(comm_responce)
        if comm_responce is None or len(comm_responce) == 0:
            return None

        r = json.loads(comm_responce)
        if 'ScheduleList' in r:
            return r['ScheduleList']

        return None



    def get_schedule(self, macid=None, event=None):
        """
            Send the get_schedule command:
            argse
                mac_id          MAC Address of ZigBee radio
                event           Type event to get schedule info for.
                                If this is omitted, then schedule
                                info for all events is requested

            Valid Events : time | message | price | summation | demand
                            scheduled_prices | profile_data
                            billing_period | block_perios
        """
        d = dict()
        if macid is not None:
            d["DeviceMacId"] = macid
        if event is not None:
            d["Event"] = event
        comm_responce = self._send_cloud_comm("get_schedule", **d)
        ### HACK ALERT
        if comm_responce[0] != "{":
            comm_responce = "{" + comm_responce + "}"
        # return json.loads(comm_responce)
        if comm_responce is None or len(comm_responce) == 0:
            return None

        r = json.loads(comm_responce)
        if 'ScheduleList' in r:
            return r['ScheduleList']

        return None

    def reboot(self, macid=None, Target="All"):
        """
            reboot
            args:
                macid           MAC Address of ZigBee radio
                Target          Part of the device to be restarted:

            Valid Targets : ZigBee | Eagle | All
        """
        d = dict()

        if macid is not None:
            d["macid"] = macid
        elif self.macid is not None:
            d["macid"] = self.macid

        if Target is not None:
            d["Target"] = Target

        comm_responce = self._send_cloud_comm("reboot", **d)
        return json.loads(comm_responce)

    def get_demand_peaks(self):
        comm_responce = self._send_cloud_comm("get_demand_peaks")
        return json.loads(comm_responce)

    def get_mdns_status(self, macid=None):
        comm_responce = self._send_cloud_comm("get_mdns_status")
        return json.loads(comm_responce)

    def configure_mdns(self, enabled=None):
        if enabled is None:
            raise ValueError("\"configure_mdns\" Invalid arg value for 'enabled'")
        if enabled is True:
            enabled = 'Y'
        elif enabled is False:
            enabled = 'N'

        comm_responce = self._send_cloud_comm("configure_mdns", Enabled=enabled)
        return json.loads(comm_responce)

    def get_current_summation(self, macid=None):
        """
            get the total consumption to date as recorded by the meter.

            args:
                mac_id          MAC Address of ZigBee radio
        """
        return self._call_cloud("get_current_summation", "CurrentSummation", macid)

    def _call_cloud(self, callname, datakey, macid=None, **kwargs):
        d = dict()
        if macid is not None:
            d["MacId"] = macid
        elif self.macid is not None:
            d["MacId"] = self.macid

        d.update(kwargs)

        comm_responce = self._send_cloud_comm(callname, **d)

        if comm_responce is None or len(comm_responce) == 0:
            return None

        r = json.loads(comm_responce)
        if datakey in r:
            return r[datakey]

        return None

        # return json.loads(comm_responce)

    def _send_cloud_comm(self, cmd, cloud=None, **kwargs):
        req_headers = dict()

        if self.debug:
            print "\n\n++++\n_send_cloud_comm : ", cmd
            print "kwargs : ", kwargs

        url = self.cloud_url

        commstr = "<Command>\n"
        commstr += "<Name>{0!s}</Name>\n".format(cmd)
        commstr += "<Format>JSON</Format>\n"
        for k, v in kwargs.items():
            if k == "MacId":
                continue
            commstr += "<{0}>{1!s}</{0}>\n".format(k, v)
        commstr += "</Command>\n"

        if self.debug:
            print "commstr :", commstr


            # bauth = base64.b64encode( "{0}:{1}".format(self.username, self.password))
#            if self.debug:
#                print "Authorization string: {:s}".format(bauth)

        req_headers["Cloud-Id"] = self.cloudid
        req_headers["Password"] = self.cloudpass
        req_headers["User"] = self.cloudemail
        #req_headers["Authorization"] = 'Basic MDAwOTQyOmYxODM4NjdmODgwNjRmMmY='


        if self.debug:
            print "_send_cloud_comm: ", url, req_headers
        req = urllib2.Request(url, commstr, headers=req_headers)

        #context = ssl._create_unverified_context()
        #response = urllib2.urlopen(req, timeout=10, context=context)

        response = urllib2.urlopen(req, timeout=30)
        # print response.info()
        the_page = response.read()
	if self.debug:
	    print "\nresponse ---\n", the_page, "\n---\n"
	    print "_send_cloud_comm: DONE\n\n"

        return the_page
