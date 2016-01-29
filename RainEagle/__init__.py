"""Simple class for talking to The EAGLE gateway ( RFA-Z109 ) from rainforest automation

"""


import sys
if sys.hexversion < 0x20703f0 :
    sys.stderr.write("You need python 2.7 or later to run this script\n")

__revision__ = "$Id: 20140301 $"
__version__ = "0.1.9"
__author__ = 'Peter Shipley <peter.shipley@gmail.com>'
__copyright__ = "Copyright (C) 2015 Peter Shipley"
__license__ = "BSD"


import EagleClass
from EagleClass import Eagle, RainEagleResponseError, Eagle_cloud, Eagle_cgi
from RainEagle.Eagle_util import to_epoch_1970, to_epoch_2000  
from RainEagle.Eagle_cloud import Eagle_cloud
from RainEagle.Eagle_cgi import Eagle_cgi


#from RainEagle.EagleClass import Eagle

__all__ = ['Eagle', 'Eagle_cloud', 'Eagle_cgi', 'RainEagleResponseError', 'to_epoch_1970', 'to_epoch_2000']



if __name__ == "__main__":
    #import __main__
    #print(__main__.__file___)
    print("RainEagle.__init__")
    print("syntax ok")
    exit(0)



