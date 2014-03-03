
import RainEagle
import time
from pprint import pprint

def too_unix_time(t) :
    """ converts time stored as
	offset in seconds from "Jan 1 00:00:00 2000"
	to unix's epoch of 1970
    """
    if isinstance(t, (int, long, float) ) :
	return t + 946684800
    if isinstance(t, str) and t.startswith('0x') :
	return 946684800 + int(t, 16)


eg = RainEagle.Eagle( debug=0 , addr="10.1.1.39")


print "\nlist_devices :"
r = eg.list_devices()
pprint(r)

# print "\nget_device_data :"
# r = eg.get_device_data()
# pprint(r)
# time_stamp_str=r['InstantaneousDemand']['TimeStamp']
# time_stamp = eg.to_unix_time(time_stamp_str)
# print "time = ", time.asctime(time.localtime(time_stamp))


print "\nget_instantaneous_demand :"
r = eg.get_instantaneous_demand()
pprint(r)


print "\nget_demand_values :"
r = eg.get_demand_values(eg.macid, interval="hour")
pprint(r)

print "\nget_summation_values :"
r = eg.get_summation_values(eg.macid, interval="day")
pprint(r)

# set_fast_poll(self, macid=None, frequency, duration) :


print "\nget_fast_poll_status :"
r = eg.get_fast_poll_status(eg.macid)
pprint(r)

etime = eg.to_unix_time( r['FastPollStatus']['EndTime'])
print "EndTime = ", time.asctime(time.localtime(etime))

# def get_history_data(self, macid=None, starttime,
# endtime=None, frequency=None ) :
