
import RainEagle
from pprint import pprint


eg = RainEagle.Eagle( debug=1 )

r = eg.list_devices()
pprint(r)

r = eg.get_device_data("EE:24:01:05:50:23")
pprint(r)
