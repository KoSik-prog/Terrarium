#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        sensors
# Purpose:
#
# Author:      KoSik
#
# Created:     27.08.2022
# Copyright:   (c) kosik 2022
# -------------------------------------------------------------------------------
try:
    import sys
    import smbus
    import board
    import busio
    import adafruit_veml6075
    import time
    import datetime
    from terrarium import *
    from lib.system import *
    from lib.log import *
except ImportError:
    print("Import error - sensors")

class Sensors:
    uva = 0.0
    uvb = 0.0
    uvi = 0.0
    dataArrayUVA = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    dataArrayUVB = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    dataArrayTempTop = [0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    dataArrayTempBottom = [0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    dataArrayHumiTop = [0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    dataArrayHumiBottom = [0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, address_temp_top, address_temp_bottom):
        self.i2cBus = None
        self.address_temp_top = address_temp_top
        self.address_temp_bottom = address_temp_bottom

    def sensors_thread(self):
        while terrarium.runFlag == True:
            #self.read_light_index() turned off!!!!!!!!!!!!!!!!!!
            self.uvi = 0.5 # delete!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.read_temperatures()
            self.send_data_to_terrarium()
            terrarium.sensorsLastUpdateTime = datetime.datetime.now()
            time.sleep(1)

    def send_data_to_terrarium(self):
        terrarium.uva = self.uva
        self.add_to_array(self.dataArrayUVA, self.uva)
        terrarium.uvb = self.uvb
        self.add_to_array(self.dataArrayUVB, self.uvb)
        terrarium.uvi = self.uvi
        if self.are_sensors_ok == False:
            system.restart('RESET! -> sensors error')

    def read_light_index(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        veml6075 = adafruit_veml6075.VEML6075(i2c, integration_time=100)
        time.sleep(0.1)
        try:
            self.uva = veml6075.uva
            if self.uva < 0:
                self.uva = 0
            self.uvb = veml6075.uva
            self.uvi = veml6075.uv_index
        except NameError:
            log.add_log('i2c bus error!')
            log.add_error_log('i2c bus error!')
            veml6075 = adafruit_veml6075.VEML6075(i2c, integration_time=100)
            time.sleep(0.1)
            self.uvb = veml6075.uvb
            self.uvi = veml6075.uv_index
        del veml6075
        del i2c

    def read_temperatures(self):
        self.i2c_bus_init()
        self.run_temperature_sensor(self.address_temp_top)
        self.run_temperature_sensor(self.address_temp_bottom)
        time.sleep(0.5)
        terrarium.temperatureTop, terrarium.humidityTop = self.read_temp_humi(
            self.address_temp_top)
        terrarium.temperatureBottom, terrarium.humidityBottom = self.read_temp_humi(
            self.address_temp_bottom)
        self.add_to_array(self.dataArrayTempTop, terrarium.temperatureTop)
        self.add_to_array(self.dataArrayTempBottom,
                          terrarium.temperatureBottom)
        self.i2c_bus_deinit()

    def are_sensors_ok(self):
        resultTempSensors = self.are_temp_sensors_ok()
        resultLightSensor = True # = self.are_light_sensor_ok()
        #print('temp sens:' + str(resultTempSensors) + ' / light: ' + str(resultLightSensor))
        if resultTempSensors == False or resultLightSensor == False:
            return False
        else:
            return True

    def are_temp_sensors_ok(self):
        resultTempTop = self.is_measurement_ok(self.dataArrayTempTop)
        resultTempBottom = self.is_measurement_ok(self.dataArrayTempBottom)
        resultHumiTop = self.is_measurement_ok(self.dataArrayHumiTop)
        resultHumiBottom = self.is_measurement_ok(self.dataArrayHumiBottom)
        if resultTempTop == True or resultTempBottom == True or resultHumiTop == True or resultHumiBottom == True:
            return True
        else:
            return False

    def are_light_sensor_ok(self):
        resultUVA = self.is_measurement_ok(self.dataArrayUVA)
        resultUVB = self.is_measurement_ok(self.dataArrayUVB)

        zeroCheckresult = 0
        for i in range(len(self.dataArrayUVA)):
            if self.dataArrayUVA[i] == 0.0:
                zeroCheckresult += 1
        if resultUVA == True or resultUVB == True or zeroCheckresult == len(self.dataArrayUVA):
            return True
        else:
            return False

    def is_measurement_ok(self, array):
        diff = 0

        for i in range(len(array) - 1):
            if array[i] == array[i + 1]:
                diff += 1
        # if the result is equal to the number of comparisons it returns False as an error
        if diff == (len(array) - 1):
            return False
        else:
            return True

    def add_to_array(self, array, value):
        self.remove_from_array(array)
        self.save_in_array(array, value)

    def save_in_array(self, array, value):
        array.append(value)

    def remove_from_array(self, array):
        array.pop(0)

    def i2c_bus_init(self):
        self.i2cBus = smbus.SMBus(1)
        time.sleep(0.1)

    def i2c_bus_deinit(self):
        del self.i2cBus  # delete object

    def run_temperature_sensor(self, address):
        self.i2cBus.write_i2c_block_data(address, 0x2C, [0x06])
        time.sleep(0.5)

    def read_temp_humi(self, address):
        try:
            self.data = self.i2cBus.read_i2c_block_data(address, 0x00, 6)
        except IOError:
            log.add_log('i2c error!')
            log.add_error_log('i2c bus error!')
        temp = ((((self.data[0] * 256.0) + self.data[1]) * 175) / 65535.0) - 45
        humi = 100 * (self.data[3] * 256 + self.data[4]) / 65535.0
        return temp, humi


sensors = Sensors(0x44, 0x45)
