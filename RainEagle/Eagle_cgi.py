import os
#import time
#import xml.etree.ElementTree as ET
import urllib
import urllib2
import base64
import json

from pprint import pprint

__all__ = ['Eagle_cgi']

class Eagle_cgi(object) :

    def __init__(self, **kwargs):

        self.macid = kwargs.get("mac", None)

        self.debug = kwargs.get("debug", 0)

        self.addr = kwargs.get("addr", os.getenv('EAGLE_ADDR', None))
	self.cloudid = kwargs.get("cloudid", os.getenv('EAGLE_CLOUDID', None))
	self.icode = kwargs.get("icode", os.getenv('EAGLE_ICODE', None))

        if self.addr is None :
	    if self.cloudid is None :
		self.addr = "eagle-{0}.local".format(self.cloudid)
	    else:
		raise AssertionError("no hostname or IP given")


        self.local_url = "http://{0}/cgi-bin/cgi_manager".format(self.addr)

        # preload
        if self.macid is None :
	    if self.cloudid is not None and self.icode is not None:
		self.device_info = self.get_device_list()
		if self.device_info is None :
		    raise IOError("Error connecting")
		if self.debug :
		    print "__init__ ",
		    print self.__class__.__name__, __name__
		    pprint(self.device_info)
		self.macid = self.device_info['device_mac_id[0]']
		if self.debug :
		    print "Init Web DeviceMacId = ", self.macid


    def set_price_auto(self, macid=None) :
        """
            Set Price from Meter

            On Success returns dict with value :
                'set_price_status':     'success'
        """
	return( self._call_cgi("set_price",
		    macid=macid,
                    Price="0xFFFFFFFF",
                    TrailingDigits="0x00"))

    # 5

    def get_device_list(self) :
        """
            Send the LIST_DEVICES command
            returns information about the EAGLE device

        """
        comm_responce = self._send_http_comm("get_device_list")
	print "get_device_list", comm_responce
        return json.loads(comm_responce)

    def get_uploaders(self, macid=None) :
        """
            gets list of uploaders for Web UI

            On Success returns dict with the values (example):
                'uploader[0]':          'none'
                'uploader[1]':          'bidgely'
                'uploader_name[0]':     'None'
                'uploader_name[1]':     'Bidgely Inc.'

        """
        comm_responce = self._send_http_comm("get_uploaders", MacId=macid)
        return json.loads(comm_responce)

    def get_uploader(self, macid=None) :
        """
            gets current uploaders config

            On Success returns dict with the values (example):
                "uploader_timestamp" :  "1394503703"
                "uploader_provider" :   "bidgely"
                "uploader_protocol" :   "https"
                "uploader_hostname" :   "api.bidgely.com"
                "uploader_url" :        "/v1/users/44441b47-1b9a-4a65-8e8c-0efefe05bb88/homes/1/gateways/1"
                "uploader_port" :       "0"
                "uploader_auth_code" :  "44441b47-1b9a-4a65-8e8c-0efefe05bb88"
                "uploader_email" :      ""
                "uploader_user_id" :    ""
                "uploader_password" :   ""
                "uploader_enabled" :    "Y"

            See also set_cloud() to set current uploader cloud config
        """
        comm_responce = self._send_http_comm("get_uploader", MacId=macid)
        return json.loads(comm_responce)


    def set_message_read(self, macid=None) :
        """
            On Success returns dict with the values :
                'remote_management_status' :    'success'

        """
        comm_responce = self._send_http_comm("set_message_read", MacId=macid)
        return json.loads(comm_responce)

    def confirm_message(self, macid=None, id=None) :
        """
        """
        id = _tohex(id)
        comm_responce = self._send_http_comm("confirm_message",
                MacId=macid, Id=id)
        return json.loads(comm_responce)

    def get_message(self, macid=None) :
        """
            On Success returns dict with the values (example):
                "meter_status" :        "Connected"
                "message_timestamp" :   "946684800"
                "message_text" :        ""
                "message_confirmed" :   "N"
                "message_confirm_required" :    "N"
                "message_id" :  "0"
                "message_queue" :       "active"
                "message_priority" :    ""
                "message_read" :        "Y"

        """
        comm_responce = self._send_http_comm("get_message", MacId=macid)
        return json.loads(comm_responce)

    def get_usage_data(self, macid=None) :
        """
            Get current demand usage summation

            On Success returns dict with the values (example):
                'demand' :               '0.4980'
                'demand_timestamp' :     '1394505386'
                'demand_units' :         'kW'
                'message_confirm_required' :     'N'
                'message_confirmed' :    'N'
                'message_id' :           '0'
                'message_priority' :     ''
                'message_queue' :        active'
                'message_read' :         'Y'
                'message_text' :         ''
                'message_timestamp' :    '946684800'
                'meter_status' :         'Connected'
                'price' :                '0.1400'
                'price_label' :          'Set by User'
                'price_units' :          '$'
                'summation_delivered' :  '2667.867'
                'summation_received' :   '37.283'
                'summation_units' :      'kWh'
                'usage_timestamp' :      '1394505386'

        """
        comm_responce = self._send_http_comm("get_usage_data", MacId=macid)
        return json.loads(comm_responce)


    def get_historical_data(self, macid=None, period="day") :
        """
            get a series of summation values over an interval of time
            ( http command api )

            args:
                period          day|week|month|year

            On Success returns dict with the values (example):
                'data_period'            'day'
                'data_size'              '14'
                'timestamp[0]'           '1394422200'
                'timestamp[1]'           '1394425800'
                'timestamp[2]'           '1394429400'
                'timestamp[3]'           '1394433000'
                'timestamp[4]'           '1394436600'
                'timestamp[5]'           '1394440200'
                'timestamp[6]'           '1394443800'
                'timestamp[7]'           '1394447400'
                'timestamp[8]'           '1394451000'
                'timestamp[9]'           '1394454600'
                'timestamp[10]'          '1394458200'
                'timestamp[11]'          '1394461800'
                'timestamp[12]'          '1394465400'
                'timestamp[13]'          '1394469000'
                'value[0]'               '0.429'
                'value[1]'               '0.426'
                'value[2]'               '0.422'
                'value[3]'               '0.627'
                'value[4]'               '0.735'
                'value[5]'               '0.193'
                'value[6]'               '0.026'
                'value[7]'               '-0.985'
                'value[8]'               '-1.491'
                'value[9]'               '-2.196'
                'value[11]'              '-1.868'
                'value[12]'              '-1.330'
                'value[13]'              '-0.870'

        """
        if period not in ['day', 'week', 'month', 'year'] :
            raise ValueError("get_historical_data : period must be one of day|week|month|year")
        comm_responce = self._send_http_comm("get_historical_data", macid=macid, Period=period)
        return json.loads(comm_responce)


    def get_setting_data(self, macid=None) :
        """
            get settings data

            On Success returns dict with value containing setting
            relating to price, uploader, network & device

        """
        comm_responce = self._send_http_comm("get_setting_data", MacId=macid)
	if comm_responce is None or len(comm_responce) == 0 :
	    return(None)
	else :
	    return json.loads(comm_responce)

    def get_device_config(self, macid=None) :
        """
            get remote management status

            On Success returns dict with value 'Y' or 'N' :
               'config_ssh_enabled':    'Y'
               'config_vpn_enabled':    'Y'

        """
	return( self._call_cgi("get_device_config", macid=macid))

    def get_gateway_info(self, macid=None) :
        """
            gets network status

            On Success returns dict with the values (example):
                'gateway_cloud_id':             '00:09:69'
                'gateway_internet_status':      'connected'
                'gateway_ip_addr':              '10.11.12.13'
                'gateway_mac_id':               'D8:D5:B9:00:90:24'

        """
	return( self._call_cgi("get_gateway_info", macid=macid))

    def get_timezone(self, macid=None) :
        """
            get current timezone configuration

            On Success returns dict with the value :
               'timezone_localTime':    '1394527011'
               'timezone_olsonName':    'UTC/GMT'
               'timezone_status':       '2'
               'timezone_utcOffset':    'UTC'
               'timezone_utcTime':      '1394527011'
               'timezone_status':       'success'

        """
	return( self._call_cgi("get_timezone", macid=macid))

    def get_time_source(self, macid=None) :
        """
            get time source for device

            On Success returns dict with value 'internet' or 'meter' :
               'time_source':           'internet'
        """
	return( self._call_cgi("get_time_source", macid=macid))

    def get_remote_management(self, macid=None) :
	return( self._call_cgi("get_remote_management", macid=macid))

    def set_remote_management(self, macid=None, status="on") :
        """ set_remote_management
            enabling ssh & vpn

            args:
                status          on|off

            On Success returns dict with value :
                'remote_management_status':     'success'

        """
        if status not in ['on', 'off'] :
            raise ValueError("set_remote_management status must be 'on' or 'off'")
        comm_responce = self._send_http_comm("set_remote_management",
                    MacId=macid, Status=status)
        return json.loads(comm_responce)


    def set_time_source(self, macid=None, source=None) :
        """ set_time_source
            set time source

            args:
                source          meter|internet

            On Success returns dict with value :
                'set_time_source_status':       u'success'

            On Error returns dict with value :
                'set_time_source_status':       'invalid source name'
        """
        if source not in ['meter', 'internet'] :
            raise ValueError("set_time_source Source must be 'meter' or 'internet'")
        comm_responce = self._send_http_comm("set_time_source",
                    MacId=macid, Source=source)
        return json.loads(comm_responce)

    def get_price(self, macid=None) :
        """
            get price for kWh

            On Success returns (example):
                price':         '0.1300'
                price_label':   'Set by User' or '--'
                price_timestamp': '1394524458'
                price_units':   '$'

            returns empty dict on Error
        """
	return( self._call_cgi("get_price", macid=macid))

    def set_price(self, macid=None, price=None) :
        """
            Set price manualy

            args:
                price           Price/kWh

            On Success returns dict with value :
                'set_price_status':     'success'

        """
        if isinstance(price, str) and price.startswith('$') :
            price = float(price.lstrip('$'))

        if not isinstance(price, (int, long, float)) :
            raise ValueError("set_price price arg must me a int, long or float")
        if (price <= 0):
            raise ValueError("set_price price arg greater then 0")

        trailing_digits     = 0
        multiplier          = 1
        while (((price * multiplier) != (floor(price * multiplier))) and (trailing_digits < 7)) :
            trailing_digits += 1
            multiplier *= 10

        price_adj = "{:#x}".format(int(price * multiplier))
        tdigits = "{:#x}".format(trailing_digits)

        comm_responce = self._send_http_comm("set_price", MacId=macid,
                        Price=price_adj, TrailingDigits=tdigits)
        return json.loads(comm_responce)


    def get_price_blocks(self, macid=None) :
	return( self._call_cgi("get_price_blocks", macid=macid))

    def get_auth(self, macid=None) :
	return( self._call_cgi("get_auth", macid=macid))

    def get_update_state(self, macid=None) :
	return( self._call_cgi("get_update_state", macid=macid))


#    def set_multiplier_divisor(self, multiplier=1, divisor=1) :
#       """
#           set multiplier and divisor manualy
#       """
#       multiplier = _tohex(multiplier, 8)
#       divisor = _tohex(divisor, 8)
#        comm_responce = self._send_http_comm("set_multiplier_divisor", MacId=macid, Multiplier=multiplier, Divisor=divisor)
#        return json.loads(comm_responce)

    def factory_reset(self, macid=None) :
        """
            Factory Reset
        """
        comm_responce = self._send_http_comm("factory_reset", MacId=macid)
        return json.loads(comm_responce)


#    def disconnect_meter(self, macid=None) :
#       """
#           disconnect from Smart Meter
#       """
#       comm_responce = self._send_http_comm("disconnect_meter", MacId=macid)
#       return json.loads(comm_responce)


    def set_cloud(self, macid=None, url=None, authcode="", email="") :
        """
            set cloud Url

            args:
                url           Url for uploader
                authcode
                email

            See also get_uploader() to retrieve current uploader cloud config
        """
        if url is None :
            raise ValueError("invalid url.\n")

        if url.__len__() > 200 :
            raise ValueError("Max URL length is 200 characters long.\n")

        urlp = urlparse(url)

        if urlp.port :
            port = "{:#04x}".format(urlp.port)
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

        comm_responce = self._send_http_comm("set_cloud", MacId=macid,
                    Provider="manual",
                    Protocol=protocol, HostName=hostname,
                    Url=url, Port=port,
                    AuthCode=authcode, Email=email,
                    UserId=userid, Password=password)
        return json.loads(comm_responce)



    def get_reset_state(self, macid=None) :
        """
            get_reset_state : 
        """
	return( self._call_cgi("get_reset_state", macid=macid))

    def cloud_reset(self, macid=None) :
        """
            cloud_reset : Clear Cloud Configuration
        """
        comm_responce = self._send_http_comm("cloud_reset", MacId=macid)
        return json.loads(comm_responce)


    def _call_cgi(self, callname, macid=None,  **kwargs):
        d = dict()
        if macid is not None :
            d["MacId"] = macid
	elif self.macid is not None :
            d["MacId"] = self.macid

	d.update(kwargs)

        comm_responce = self._send_http_comm(callname, **d)
        return json.loads(comm_responce)

    def _send_http_comm(self, cmd, **kwargs):
	req_headers=dict()

        if self.debug :
            print "\n\n_send_http_comm : ", cmd
            print "self.macid : ", self.macid
            print "kwargs : ", kwargs

	url = self.local_url

	macid = kwargs.get("MacId", None)

        commstr = "<LocalCommand>\n"
        commstr += "<Name>{0!s}</Name>\n".format(cmd)
	if macid is None :
	    macid = self.macid

	if macid is not None :
	    commstr += "<MacId>{0!s}</MacId>\n".format(macid)
	    pass
        for k, v in kwargs.items() :
	    if k is "MacId" :
		continue
            commstr += "<{0}>{1!s}</{0}>\n".format(k, v)
        commstr += "</LocalCommand>\n"

        if cmd == "set_cloud" :
            print(commstr)
            return dict()

        if self.debug :
            print(commstr)

        if self.cloudid is not None :
	    bauth = base64.b64encode( "{0}:{1}".format(self.cloudid, self.icode))
	    req_headers["Authorization"] =  "Basic {0}".format(bauth)

	if self.debug :
	    #print "_send_http_comm: ", url, req_headers
	    pass
	req = urllib2.Request(url, commstr, headers=req_headers)
        response = urllib2.urlopen(req, timeout=10)
	# print response.info()
        the_page = response.read()

        return the_page

