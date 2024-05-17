"""
author: waliori
"""
from machine import Pin, I2C
import time
import ustruct
import math

class Accelerometer:
    # Constants
    ADXL345_ADDRESS = 0x53
    ADXL345_POWER_CTL = 0x2D
    ADXL345_DATA_FORMAT = 0x31
    ADXL345_DATAX0 = 0x32

    # Initialization with configurable thresholds
    def __init__(self, sda, scl, freq):
        # Initialize I2C
        self.i2c = I2C(1, sda=sda, scl=scl, freq=freq)
        # Initialize ADXL345
        self.init_adxl345()

    def init_adxl345(self):
        self.i2c.writeto_mem(self.ADXL345_ADDRESS, self.ADXL345_POWER_CTL, bytearray([0x08]))  # Measurement mode
        self.i2c.writeto_mem(self.ADXL345_ADDRESS, self.ADXL345_DATA_FORMAT, bytearray([0x0B]))  # Full resolution, +/- 16g

    def read_accel_data(self):
        data = self.i2c.readfrom_mem(self.ADXL345_ADDRESS, self.ADXL345_DATAX0, 6)
        x, y, z = ustruct.unpack('<3h', data)
        return x, y, z

