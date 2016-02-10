# Python class for Rainforest Eagle

Python Class for utilizing the Rainforest Automation Eagle ( RFA-Z109 ) socket API

This is the DEV BRANCH it may not work ( pull requests welcome )

version = "0.1.8"

Example :

```python
    import RainEagle

    raineagle = RainEagle.Eagle( debug=0 , addr="10.1.1.39")
    ret_data = eg.list_devices()

    print "device MacID = ", ret_data['DeviceInfo']['DeviceMacId']
```

API Call list :

```python



    # Web/Ajax API based calls
    get_device_list()

    get_gateway_info(MacID)

    get_demand_values(MacId, interval='hour', frequency=None)
    get_device_config(MacId)
    get_historical_data(period='day')

    get_price(MacId)
    set_price(MacID, Price, TrailingDigits)
    get_price_blocks(MacID)
    set_price_auto(MacID)

    set_multiplier_divisor(MacId, Multiplier, Divisor)

    get_setting_data(MacID)

    get_usage_data(MacID)
    get_raw_data(MacId, Type, Period)

    get_time_source(MacId)
    set_time_source(MacId, Source='internet|meter')
    get_timezone(MacId)
    set_timezone(MacId, OlsonName)

    get_message(MacId)
    set_message_read(MacId)
    confirm_message(MacId, Id)

    set_remote_management(macid, status='on|off')


    get_reset_state(MacID)
    clear_reset_state(MacID)
    cloud_reset(MacId)
    factory_reset(MacID)

    add_cloud(MacId, Provider, Description, HostName, Protocol, [Url], [Port])
    drop_cloud(Provider)
    set_cloud(MacId, Provider)
    disconnect_meter(MacId)

    get_auth(MacId)
    set_auth(MacId, Status='off|on')

    check_update(MacID)
    clear_update_state(MacID)
    get_update_state(MacId)
    start_update(MacID)
    set_update_schedule(MacId, Frequency, Mode, Enabled)

    get_fast_poll_status(MacId)
    set_fast_poll(MacId)

    get_uploaders(MacID)

    # Cloud API based calls
    get_network_info([Protocol], [MacId])
    list_network()
    get_network_status([Protocol], [MacId])
    get_instantaneous_demand(MacId)
    get_price(MacId)
    get_message(MacId)
    confirm_message(MacId, Id)
    get_current_summation(MacId)
    get_history_data(MacId, StartTime, [EndTime], [Frequency])
    set_schedule(DeviceMacId, Event, Frequency, Enabled)
    get_schedule(DeviceMacId, [Event])
    reboot(MacId, Target)
    get_demand_peaks()
    get_mdns_status(Enabled='Y|N')
    configure_mdns(MacId, Enabled='Y|N')

    # Socket API based commands (deprecated protocol)
    list_devices()
    get_device_data(macid)
    get_history_data(macid, starttime='0x00000000', endtime=None, frequency=None)
    get_instantaneous_demand(macid)
    get_summation_values(macid, interval='day')
    get_fast_poll_status(macid)
    set_fast_poll(macid, frequency='0x04', duration='0xFF')

```

API Calls return dictionarys containing data results,
raises exception or returns None if error

## External Documentation

* Developer Portal http://rainforestautomation.com/developer

* socket interface  API http://rainforestautomation.com/sites/default/files/docs/eagle_socket_api_09.pdf
 

