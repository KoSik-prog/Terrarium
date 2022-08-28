#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        sensors
# Purpose:
#
# Author:      KoSik
#
# Created:     27.08.2022
# Copyright:   (c) kosik 2022
#-------------------------------------------------------------------------------
import sys, smbus, board, busio, adafruit_veml6075, time

from terrarium import *
from libraries.log import *

class sensorsCL:
    UVA = 0.0
    UVB = 0.0
    UVI = 0.0
    data = [0, 0, 0, 0, 0]

    def __init__(self, address_temp_top, address_temp_bottom):
        self.i2cBus = None
        self.address_temp_top = address_temp_top
        self.address_temp_bottom = address_temp_bottom

    def read_light_index(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        veml6075 = adafruit_veml6075.VEML6075(i2c, integration_time = 100)
        time.sleep(0.1)
        try:
            self.UVA = veml6075.uva
            self.UVB = veml6075.uva
            self.UVI = veml6075.uv_index
        except NameError:
            log.add_log('i2c bus error!')
            veml6075 = adafruit_veml6075.VEML6075(i2c, integration_time = 100)
            time.sleep(0.1)
            if veml6075.uva > 0:
                self.UVA = veml6075.uva
            else:
                self.UVA = 0
            self.UVB = veml6075.uvb
            self.UVI = veml6075.uv_index
        del veml6075
        del i2c

    def read_temperatures(self):
        self.i2c_bus_init()
        self.run_temperature_sensor(self.address_temp_top)
        self.run_temperature_sensor(self.address_temp_bottom)
        time.sleep(0.5)
        terrarium.tempG, terrarium.wilgG = self.read_temp_humi(self.address_temp_top)
        terrarium.tempD, terrarium.wilgD = self.read_temp_humi(self.address_temp_bottom)
        self.i2c_bus_deinit()

    def i2c_bus_init(self):
        self.i2cBus = smbus.SMBus(1)
        time.sleep(0.1)
    
    def i2c_bus_deinit(self):
        del self.i2cBus #delete object

    def run_temperature_sensor(self, address):
        self.i2cBus.write_i2c_block_data(address, 0x2C, [0x06])
        time.sleep(0.5)

    def read_temp_humi(self, address):
        try:
            self.data = self.i2cBus.read_i2c_block_data(address, 0x00, 6)
        except IOError:
            log.add_log('i2c error!')
        temp = ((((self.data[0] * 256.0) + self.data[1]) * 175) / 65535.0) - 45
        humi = 100 * (self.data[3] * 256 + self.data[4]) / 65535.0
        return temp, humi

sensors = sensorsCL(0x44, 0x45)