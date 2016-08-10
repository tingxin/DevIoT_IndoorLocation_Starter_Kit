__author__ = 'tingxxu'
from DevIoTGateway.gateway import Gateway
from DevIoTGateway.config import config

from logic.helper import ServiceHelper

import time
import os

models = {}
all_logic = {}


def load_sensor_model(model, logic):
    if model.kind not in models:
        models[model.kind] = model
        all_logic[model.kind] = logic


def import_sensor_model():
    current_folder = os.getcwd()
    sensors_folder = current_folder + "/sensors"
    sensor_files = os.listdir(sensors_folder)

    for sensor_file in sensor_files:
        if sensor_file.endswith('.py') and sensor_file.endswith('__.py') is False:
            sensor_info = sensor_file.split('.')
            sensor_name = sensor_info[0]
            if len(sensor_name) < 1:
                continue
            sensor_logic = sensor_name[0].upper() + sensor_name[1:] +"Logic"
            if sensor_name not in models:
                import_sensor = "from sensors.{0:s} import {1:s}, {2:s}".format(sensor_name, sensor_name, sensor_logic)

                exec import_sensor
                add_sensor = "load_sensor_model({0:s},{1:s})".format(sensor_name, sensor_logic)
                exec add_sensor


if __name__ == '__main__':

    import_sensor_model()

    devIot_address = config.get_string("address", "10.140.92.25:9000")
    mqtt_address = config.get_string("mqtthost", "10.140.92.25:1883")
    app_name = config.get_string("appname", "IndoorLocation")
    devIot_account = config.get_info("account", "")

    app = Gateway(app_name, devIot_address, mqtt_address, devIot_account)
    app.is_virtual = True

    for key in models:
        app.register_custom_sensor(models[key])

    app.run()

    while True:
        time.sleep(1.5)
        devices = ServiceHelper.get_all_clients()
        if devices is not None:
            sensors = app.get_sensors()
            for key in sensors:
                sensor = sensors[key]
                all_logic[sensor.kind].update(sensor, devices)





