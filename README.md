#Cmx/Meraki Gateway#
Cmx gateway service can be used to work with DevIot, supply the DevIot capability with read device location data, get the number of device in target area and so on

Cmx gateway contain two sensors, one is the cmxarea sensor, this sensor can count all devices in target area. another sensor is cmxdevice, this sensor can which room contain target device. those sensors can be reused by different parameter, so this gateway can support multiple users

you can from [here](https://developer.cisco.com/site/cmx-mobility-services/) to get more detail about CMX

This code also can be as a sample code to show how to use the Gateway Service SDK, use it build a completed gateway service which can work with DevIot

## Table of contents

* [What in this code](#what-in-this-code)
* [Prerequisite](#prerequisite)
* [How to use](#how-to-use)
* [How to test ](#how-to-test )
* [Getting help](#getting-help)

## What in this code
1.the app.py: the app entry

2.setting.cfg: the custom's setting file, you can put all you setting item in this file with json format

3.sensors folder: contain all the sensor logic model, you can use cmx capability to define your own sensor in here

4.logic folder: contain some custom logic, such as how to get the data from cmx

##Prerequisite
1. This sample code base on the Python 2.7.10, please make sure your machine environment have installed [Python2.7](https://www.python.org/downloads/)
2. This sample code use Cisco [cmx](https://developer.cisco.com/site/cmx-mobility-services/) api to count trace device,please make sure you have <br>
Cisco cmx service or you can use cmx sandbox.
3. You need meet all the [prerequisite](https://cto-github.cisco.com/tingxxu/iot-gateway/blob/master/README.md) of Gateway SDK

##How to use
###Use sample code directly

1.Download the this code to your machine.

2.Install the dependency as blow command:
    
    sudo  python setup.py install
   
3.Open the setting.cfg file to configuration
    
    {
    "appname":"IndoorLocation",
    "address":"10.140.92.25:9000",                  #necessary, DevIot platform server address, format should be: ip:port
    "mqtthost":"10.140.92.25:1883",                 #necessary, the DevIot platform MQTT server address, format should be: ip:port
    "service": {
        "address":"10.140.92.53:8080",              #necessary, the cmx service address
        "api":"meraki/api/v1/location/clients",     #necessary, the cmx server api for getting clients
        "authority":"false",                        #necessary, need authority in your serivce
        #"map_name":"System Campus>SHN15>DevNet15A",#necessary, your map/floor name
        "map_name":"",
        "username": "admin",                        #necessary, service account
        "password": "c1sc0123"                      #necessary, service password
    },
    "areas":[                                       #this segment used for the sensor cmxdevice
        {                                           #we define several room to check if the phone in those rooms 
            "name": "DevNet Room",
            "left": 0,
            "top": 0,
            "width": 200,
            "height": 100
            },
        {
            "name": "Lab",
            "left": 500,
            "top": 0,
            "width": 50,
            "height": 50
        },
        {
            "name": "Meeting Room",
            "left": 0,
            "top": 54,
            "width": 50,
            "height": 50
        },
        {
            "name": "Washing Room",
            "left": 200,
            "top": 300,
            "width": 50,
            "height": 50
        }
    ]
}
    
3.Open the terminal window and cd to this folder, type follow command to run it:
    
    python app.py
    
then terminal window ask you for some necessary information, after that the gateway service will start successfully

##How to test 
You can use [mqtool to test you service](https://cto-github.cisco.com/tingxxu/iot-gateway/tree/master/tools) to check the data from your Gateway

## Getting help

If you have questions, concerns, bug reports, etc, please file an issue in this repository's Issue Tracker

## Getting involved

For general instructions on _how_ to contribute, please visit [CONTRIBUTING](CONTRIBUTING.md)

## Open source licensing info

1. [LICENSE](LICENSE)

## Credits and references

None