"""Simple class for talking to The EAGLE gateway ( RFA-Z109 ) from rainforest automation

"""

import sys
if sys.hexversion < 0x20703f0 :
    sys.stderr.write("You need python 2.7 or later to run this script\n")


from RainEagle.EagleClass import Eagle

__all__ = ['Eagle']



if __name__ == "__main__":
    import __main__
    #print(__main__.__file___)
    print("ISY.__init__")
    print("syntax ok")
    exit(0)



