
import os
import time
import xml.etree.ElementTree as ET
import urllib
import urllib2
# import base64
from six.moves import configparser

__all__ = ['to_epoch_2000', 'to_epoch_1970', '_tohex', '_twos_comp', '_et2d', '_get_config']

def to_epoch_2000(t) :
    """ converts time stored as
        to unix's epoch of 1970
        offset in seconds from "Jan 1 00:00:00 2000"
    """
    if isinstance(t, time.struct_time) :
        t = time.mktime(t)
    return t - 946684800


def to_epoch_1970(t) :
    """ converts time stored as
        offset in seconds from "Jan 1 00:00:00 2000"
        to unix's epoch of 1970
    """
    if isinstance(t, (int, long, float)) :
        return t + 946684800
    if isinstance(t, str) and t.startswith('0x') :
        return 946684800 + int(t, 16)

def _et2d(et) :

    """ Etree to Dict

        converts an ETree to a Dict Tree
        lists are created for duplicate tag

        if there are multiple XML of the same name
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
            d[et.tag + "-" + k] = v
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


def _twos_comp(val, bits=32):
    """compute the 2's compliment of int value val"""
    if( (val&(1<<(bits-1))) != 0 ):
        val = val - (1<<bits)
    return val


def _tohex(n, width=8) :
    """
        convert arg to string with hex representation if possible

        use twos-complement for negitive 32bit numbers

        use int class to convert whatever is handed to us
    """
    if isinstance(n, str) and n.startswith('0x') :
        return(n)

    i = int(n)

    # add two for the "0x"
    width += 2

    if (i > 2147483647) or (i < -2147483648) :
        warn("_tohex : signed int to large (" + str(n) + ")\n",
                        RuntimeWarning, stacklevel=2)

    if i < 0 :
        i += 0x100000000

    return  "{:#0{width}x}".format(int(i), width=width)


def _get_config(config_path=None, opt=None):
    if not config_path:
        config_path = os.path.sep.join(('~', '.config', 'eagle', 'config'))
 
    defaults = {}
    config_file = os.path.expanduser(config_path)
    print "config_file", config_file
    if os.path.exists(config_file):
        config = configparser.SafeConfigParser()
        config.read([config_file])
	defaults.update(dict(config.defaults()))
        if config.has_section('eagle'):
            defaults.update(dict(config.items('eagle')))
        if opt is not None and config.has_section(opt):
		defaults.update(dict(config.items(opt)))
 
    return defaults
#


