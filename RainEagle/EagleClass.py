

# import socket
# import sys
import os
#import time
#import xml.etree.ElementTree as ET
#import urllib
#import urllib2
#import base64
#from math import floor
#from urlparse import urlparse
#import json
# from warnings import warn
# from distutils.version import LooseVersion

# from RainEagle.Eagle_soc import Eagle_soc
#from RainEagle.Eagle_util import to_epoch_2000, to_epoch_1970, _tohex, _twos_comp, _et2d
from RainEagle.Eagle_util import to_epoch_2000, to_epoch_1970, _twos_comp, _et2d
from RainEagle.Eagle_cloud import Eagle_cloud
from RainEagle.Eagle_cgi import Eagle_cgi

__author__ = 'Peter Shipley <peter.shipley@gmail.com>'
__copyright__ = "Copyright (C) 2014 Peter Shipley"
__license__ = "BSD"
__version__ = "0.1.9"

min_fw_ver = "2.0.21"


__all__ = ['RainEagleResponseError', 'Eagle', 'Eagle_cloud', 'Eagle_cgi', 'to_epoch_1970, to_epoch_2000']

from pprint import pprint


# api_arg_format = { }


class RainEagleResponseError(RuntimeError):
    """General exception for responce errors
        from Rainforest Automation EAGLE (RFA-Z109)
    """
    pass


#

#class Eagle_util(object):
#    pass




class Eagle(Eagle_cloud, Eagle_cgi):
    """
        Class for talking to Rainforest Automation EAGLE (RFA-Z109)

        args:
            debug       print debug messages if true
            addr        address of device
            port        port on device (default 5002)
            getmac      connect to device at start up and get macid (default true)
            password    Password for HTTP Authentication
            username    Username for HTTP Authentication
            timeout     TCP socket timeout

        Currently there is very little error handling ( if any at all )
    """
    def __init__(self, **kwargs):

        Eagle_cgi.__init__(self, **kwargs)
        Eagle_cloud.__init__(self, **kwargs)

        self.debug = kwargs.get("debug", 0)

        if self.debug:
            print self.__class__.__name__, __name__

        if self.debug:
            print "Addr :  = ", self.addr
            print "debug :  = ", self.debug

        if self.icode is None:
            if self.network_info is not None:
                self.icode = self.network_info['InstallCode'][2:]
                if self.debug:
                    print "Init Main InstallCode = ", self.icode


# socket commands as class functions







# http commands as class functions





# Support functions





# Do nothing
# (syntax check)
#
if __name__ == "__main__":
    import __main__
    print(__main__.__file__)

    print("syntax ok")
    exit(0)


