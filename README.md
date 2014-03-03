
Python Class for utilizing the Rainforest Automation Eagle ( RFA-Z109 ) socket API


    import import RainEagle

    raineagle = RainEagle.Eagle( debug=0 , addr="10.1.1.39")
    ret_data = eg.list_devices()

    print "device MacID = ", ret_data['DeviceInfo']['DeviceMacId']




Rainforest Automation Documentation
-----------------------------------

* Developer Portal http://rainforestautomation.com/developer


* socket interface  API http://rainforestautomation.com/sites/default/files/docs/eagle_socket_api_09.pdf
 

