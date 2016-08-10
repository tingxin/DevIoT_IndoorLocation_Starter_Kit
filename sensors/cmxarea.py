__author__ = 'tingxxu'

import sys
from DevIoTGateway.sensor import Sensor, SProperty, SSetting
from DevIoTGateway.config import config
from logic.sensorlogic import SensorLogic

floor = config["service"]["map_name"]

cmxarea = Sensor("cmxarea", "cmxarea_1", "Device Count")

count_property = SProperty("count", 0, None, 0)
count_property.description = "count of the device in target area"
cmxarea.add_property(count_property)

x1_setting = SSetting("X1", 0, None, 466, True)
x1_setting.description = "x-coordinate of area"

y1_setting = SSetting("Y1", 0, None, 710, True)
y1_setting.description = "y-coordinate of area"

x2_setting = SSetting("X2", 0, None, 640, True)
x2_setting.description = "x-coordinate of area"

y2_setting = SSetting("Y2", 0, None, 680, True)
y2_setting.description = "y-coordinate of area"

x3_setting = SSetting("X3", 0, None, 480, True)
x3_setting.description = "x-coordinate of area"

y3_setting = SSetting("Y3", 0, None, 720, True)
y3_setting.description = "y-coordinate of area"

x4_setting = SSetting("X4", 0, None, 680, True)
x4_setting.description = "x-coordinate of area"

y4_setting = SSetting("Y4", 0, None, 690, True)
y4_setting.description = "y-coordinate of area"

cmxarea.add_setting(x1_setting)
cmxarea.add_setting(y1_setting)
cmxarea.add_setting(x2_setting)
cmxarea.add_setting(y2_setting)
cmxarea.add_setting(x3_setting)
cmxarea.add_setting(y3_setting)
cmxarea.add_setting(x4_setting)
cmxarea.add_setting(y4_setting)


mapCoordinate = "mapCoordinate"
mapInfo = "mapInfo"

bound = []
bound.append({'x': x1_setting.value, 'y': y1_setting.value})
bound.append({'x': x2_setting.value, 'y': y2_setting.value})
bound.append({'x': x3_setting.value, 'y': y3_setting.value})
bound.append({'x': x4_setting.value, 'y': y4_setting.value})

center_y = 690
center_x = 600
distance = 20


class CmxareaLogic(SensorLogic):

    modify_key = "settings"

    @staticmethod
    def modify(sensor, data):
        if data['id'] == sensor.id:
            if CmxareaLogic.modify_key in data and data[CmxareaLogic.modify_key] is not None:
                updated_settings = {}
                for d_setting in data[CmxareaLogic.modify_key]:
                    updated_settings[d_setting["name"]] = d_setting["value"]
                sensor.update_settings(updated_settings)
                return True
        return False

    @staticmethod
    def update(sensor, data):
        count = 0
        if data is not None:
            for device in data:
                try:
                    if device["ipAddress"] is None:
                        continue
                    if device[mapInfo]['mapHierarchyString'] is None or floor == device[mapInfo]['mapHierarchyString']:
                        in_area = CmxareaLogic.__check_in_area(device[mapCoordinate]['x'], device[mapCoordinate]['y'], bound)
                        if in_area:
                            count += 1
                        if 680 > device[mapCoordinate]['x'] > 470:
                            if abs(device[mapCoordinate]['y'] - 700) <= 20:
                                count += 1

                except:
                    print(sys.exc_info()[1])
        sensor.update_properties({"count": count})


    @staticmethod
    def __check_in_area(x, y, points):
        counter = 0
        p1 = points[0]
        count = len(points)

        for i in range(1, count + 1):
            p2 = points[i % count]
            if y > min(p1["y"], p2["y"]):
                if y <= max(p1["y"], p2["y"]):
                    if x <= max(p1["x"], p2["x"]):
                        if p1["y"] != p2["y"]:
                            inters = (y - p1["y"])*(p2["x"]-p1["x"])/(p2["y"] - p1["y"]) +p1["x"]
                            if p1["x"] == p2["x"] or x <= inters:
                                counter += 1
            p1 = p2

        if counter % 2 == 0:
            return False
        return True
