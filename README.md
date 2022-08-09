# Simple-Micropython-MCP9600-Library
Simple yet functional MCP9600 Thermocouple IC Amplifier Library.

Simple library for reading and configuring the MCP9600 Thermocouple amplifier. You can read temperatures, set the thermocouple type, and set filters. This library is by no means optimized, it is meant to be readable for new programmers, but is functional. I'm not responsible for any damages or anything caused by this code, it is provided AS IS, use at your own risk. 

I will add more info as sonn as possible, for the moment I think is pretty self explanatory. Cheers!

If you have problems reading data you can try this:
* Check your pull up resistors.
* Check your power supply (voltage/current).
* Try SoftI2C instead. 

This library was tested and developed for Raspberry Pi Pico. But as far as I know you can use it on other Micropython compatible devices.
