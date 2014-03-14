# Python class for Rainforest Eagle

Python Class for utilizing the Rainforest Automation Eagle ( RFA-Z109 ) socket API


version = "0.1.7"

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
    get_device_data(macid)
    get_history_data(macid, starttime='0x00000000', endtime=None, frequency=None)
    get_instantaneous_demand(macid)
    get_summation_values(macid, interval='day')
    get_fast_poll_status(macid)
    set_fast_poll(macid, frequency='0x04', duration='0xFF')


    # Web API based calls
    cloud_reset()
    confirm_message(id)
    factory_reset()
    get_demand_values(macid, interval='hour', frequency=None)
    get_device_config()
    get_device_list()
    get_gateway_info()
    get_historical_data(period='day')
    get_message()
    get_price()
    set_price(price)
    set_price_auto()
    get_remote_management()
    get_setting_data()
    get_usage_data()
    get_time_source(macid)
    set_time_source(macid, source='internet')
    get_timezone()
    get_uploader()
    get_uploaders()
    set_cloud(url, authcode='', email='')
    set_message_read()
    set_remote_management(macid, status='on')

```

API Calls return dictionarys containing data results,
raises exception or returns None if error

## External Documentation

* Developer Portal http://rainforestautomation.com/developer

* socket interface  API http://rainforestautomation.com/sites/default/files/docs/eagle_socket_api_09.pdf
 

