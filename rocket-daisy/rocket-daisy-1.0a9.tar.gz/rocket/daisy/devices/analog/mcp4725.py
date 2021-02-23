
from rocket.daisy.utils.types import toint
from rocket.daisy.devices.i2c import I2C
from rocket.daisy.devices.analog import DAC


class MCP4725(DAC, I2C):
    def __init__(self, slave=0x60, vref=3.3):
        I2C.__init__(self, toint(slave))
        DAC.__init__(self, 1, 12, float(vref))
        
    def __str__(self):
        return "MCP4725(slave=0x%02X)" % self.slave

    def __analogRead__(self, channel, diff=False):
        d = self.readBytes(3)
        value = (d[1] << 8 | d[2]) >> 4
        return value
        
    
    def __analogWrite__(self, channel, value):
        d = bytearray(2)
        d[0] = (value >> 8) & 0x0F
        d[1] = value & 0xFF
        self.writeBytes(d)
