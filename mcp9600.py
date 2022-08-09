"""
Simple Micropython MCP9600 Library
https://github.com/CAATZ/Simple-Micropython-MCP9600-Library

MIT License

Copyright (c) 2022 CAATZ

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import ustruct
import time

class MCP9600:
    
    def __init__(self, i2c, address=0x67):
        self.address = address
        self.i2c = i2c
        
    def sensor_config(self):
        self.i2c.writeto(self.address, b'\x05')
        sensor_config = self.i2c.readfrom(self.address, 1, True)
        return ustruct.unpack('<B', sensor_config)[0]

    def set_type(self, type_str):
        if type_str == 'K':
            self._th_type = 0x00
        elif type_str == 'J':
            self._th_type = 0x10
        elif type_str == 'T':
            self._th_type = 0x20
        elif type_str == 'N':
            self._th_type = 0x30
        elif type_str == 'S':
            self._th_type = 0x40
        elif type_str == 'E':
            self._th_type = 0x50
        elif type_str == 'B':
            self._th_type = 0x60
        elif type_str == 'R':
            self._th_type = 0x70
        else:
            raise RuntimeError("Not a valid sensor type")
        
        temp_data = self.sensor_config() & 0x0F
        
        new_config = temp_data | self._th_type
        
        buffer = bytes([0x05, new_config])
        
        self.i2c.writeto(self.address, buffer)
    
    def set_filter(self, filter_int):
        if (filter_int > 7) or (filter_int < 0):
            raise RuntimeError("Filter out of range")
        
        temp_data = self.sensor_config() & 0xF0
        
        new_config = temp_data | int(filter_int)
        
        buffer = bytes([0x05, new_config])
        
        self.i2c.writeto(self.address, buffer)
              
    def _read_temp(self, command):
        self.i2c.writeto(self.address, command)
        read_bytes = self.i2c.readfrom(self.address, 2)
        
        if(read_bytes[0] & 0x80):
            temperature = (read_bytes[0] * 16) + (read_bytes[1] / 16) - 4096
        else:
            temperature = (read_bytes[0] * 16) + (read_bytes[1] / 16)
        
        return temperature
        
    def read_th_temp(self):
        return self._read_temp(b'\x00')
    
    def read_dt_temp(self):
        return self._read_temp(b'\x01')
    
    def read_ic_temp(self):
        return self._read_temp(b'\x02')
    