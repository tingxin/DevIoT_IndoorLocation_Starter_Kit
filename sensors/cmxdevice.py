__author__ = 'tingxxu'

import sys

from DevIoTGateway.sensor import Sensor, SProperty, SSetting
from DevIoTGateway.config import config

from logic.sensorlogic import SensorLogic

floor = config["service"]["map_name"]

default_location = {"location": "others"}
areas = []
for area in config["areas"]:
    areas.append(area)

cmxdevice = Sensor("cmxdevice", "cmxdevice_1", "Personal Device")

location_property = SProperty("location", 1, [], areas[0]["name"])
location_property.description = "location of the device in %s" % floor
cmxdevice.add_property(location_property)
for area in areas:
    location_property.range.append(area["name"])

x_property = SProperty("x", 0, None, 0)
x_property.description = "x-coordinate of the device in %s" % floor
cmxdevice.add_property(x_property)

y_property = SProperty("y", 0, None, 0)
y_property.description = "y-coordinate of the device in %s" % floor
cmxdevice.add_property(y_property)

mac_address_setting = SSetting("mac_address", 1, None, "34:a3:95:90:25:89", True)

mac_address_setting.description = "the ip address of user's device"

cmxdevice.add_setting(mac_address_setting)


mapCoordinate = "mapCoordinate"
mapInfo = "mapInfo"


class CmxdeviceLogic(SensorLogic):

    modify_key = "settings"

    @staticmethod
    def modify(sensor, data):
        if data['id'] == sensor.id:
            if CmxdeviceLogic.modify_key in data and data[CmxdeviceLogic.modify_key] is not None:
                updated_settings = {}
                for d_setting in data[CmxdeviceLogic.modify_key]:
                    updated_settings[d_setting["name"]] = d_setting["value"]
                sensor.update_settings(updated_settings)
                return True
        return False

    @staticmethod
    def update(sensor, data):
        if data is not None:

            for device in data:
                try:
                    if device['ipAddress'] is None:
                        continue
                    same_device = False
                    ip_setting = sensor.setting('mac_address').lower()
                    if device['macAddress'] == ip_setting:
                        same_device = True
                    elif device['ipAddress'] == ip_setting:
                        same_device = True
                    elif isinstance(device['ipAddress'], list):
                        if device['ipAddress'][0] == ip_setting:
                            same_device = True
                    if same_device:
                        if device[mapInfo]['mapHierarchyString'] is None or device[mapInfo]['mapHierarchyString'] == floor:

                            new_property_value = {"x": device[mapCoordinate]['x'],
                                                  "y": device[mapCoordinate]['y']}
                            sensor.update_properties(new_property_value)
                            # for area_item in areas:
                            #     if device[mapCoordinate]['x'] >= area_item['left']:
                            #         if device[mapCoordinate]['y'] >= area_item['top']:
                            #             if device[mapCoordinate]['x'] <= area_item['left'] + area_item['width']:
                            #                 if device[mapCoordinate]['y'] <= area_item['top'] + area_item['height']:
                            #                     location_new_value = {"location": area_item["name"]}
                            #                     sensor.update_properties(location_new_value)
                            #                     return
                            if 680 > device[mapCoordinate]['x'] > 450:
                                if abs(device[mapCoordinate]['y'] - 700) <= 20:
                                    location_new_value = {"location": "Meeting Room"}
                                    sensor.update_properties(location_new_value)
                except:
                    print(sys.exc_info()[1])
        sensor.update_properties(default_location)

