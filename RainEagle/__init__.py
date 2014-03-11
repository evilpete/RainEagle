"""Simple class for talking to The EAGLE gateway ( RFA-Z109 ) from rainforest automation

"""


import sys
if sys.hexversion < 0x20703f0 :
    sys.stderr.write("You need python 2.7 or later to run this script\n")

__revision__ = "$Id: 20140301 $"
__version__ = '0.1.20140301'
__author__ = 'Peter Shipley <peter.shipley@gmail.com>'
__copyright__ = "Copyright (C) 2014 Peter Shipley"
__license__ = "BSD"


import EagleClass
from EagleClass import Eagle, RainEagleResponseError, to_epoch_1970, to_epoch_2000
#from RainEagle.EagleClass import Eagle

__all__ = ['Eagle', 'RainEagleResponseError', 'to_epoch_1970', 'to_epoch_2000']



if __name__ == "__main__":
    #import __main__
    #print(__main__.__file___)
    print("RainEagle.__init__")
    print("syntax ok")
    exit(0)



