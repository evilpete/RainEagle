# Python class for Rainforest Eagle

Python Class for utilizing the Rainforest Automation Eagle ( RFA-Z109 ) socket API


Example :

```python
    import RainEagle

    raineagle = RainEagle.Eagle( debug=0 , addr="10.1.1.39")
    ret_data = eg.list_devices()

    print "device MacID = ", ret_data['DeviceInfo']['DeviceMacId']
```

API Call list :

```python

    # Socket API based commands
    list_devices()
    get_demand_values(macid=None, interval='hour', frequency=None)
    get_device_data(macid=None)
    get_history_data(macid=None, starttime='0x00000000', endtime=None, frequency=None)
    get_instantaneous_demand(macid=None)
    get_summation_values(macid=None, interval='day')
    get_fast_poll_status(macid=None)
    set_fast_poll(macid=None, frequency='0x04', duration='0xFF')


    # Web API based calls
    def get_setting_data(macid=None)
    def get_device_config(macid=None)
    def get_timezone(macid=None)
    def get_time_source(macid=None)
    def set_remote_management(macid=None, status="Yes")
    def set_time_source(macid=None, source="internet")
    def get_price(macid=None)
    def set_price(macid=None, price)
    def set_price_auto(macid=None)
    def factory_reset(macid=None)
    def cloud_reset(macid=None)
    def set_cloud(macid=None, url)

```

API Calls return dictionarys containing data results,
raises exception or returns None if error

## External Documentation

* Developer Portal http://rainforestautomation.com/developer

* socket interface  API http://rainforestautomation.com/sites/default/files/docs/eagle_socket_api_09.pdf
 

