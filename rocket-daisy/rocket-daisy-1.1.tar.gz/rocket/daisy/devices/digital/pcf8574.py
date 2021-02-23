

from rocket.daisy.utils.types import toint
from rocket.daisy.devices.i2c import I2C
from rocket.daisy.devices.digital import GPIOPort

class PCF8574(I2C, GPIOPort):
    FUNCTIONS = [GPIOPort.IN for i in range(8)]
    
    def __init__(self, slave=0x20):
        slave = toint(slave)
        if slave in range(0x20, 0x28):
            self.name = "PCF8574"
        elif slave in range(0x38, 0x40):
            self.name = "PCF8574A"
        else:
            raise ValueError("Bad slave address for PCF8574(A) : 0x%02X not in range [0x20..0x27, 0x38..0x3F]" % slave)
        
        I2C.__init__(self, slave)
        GPIOPort.__init__(self, 8)
        self.portWrite(0xFF)
        self.portRead()
    
    def __str__(self):
        return "%s(slave=0x%02X)" % (self.name, self.slave)
        
    def __getFunction__(self, channel):
        return self.FUNCTIONS[channel]
    
    def __setFunction__(self, channel, value):
        if not value in [self.IN, self.OUT]:
            raise ValueError("Requested function not supported")
        self.FUNCTIONS[channel] = value
        
    def __digitalRead__(self, channel):
        mask = 1 << channel
        d = self.readByte()
        return (d & mask) == mask 

    def __portRead__(self):
        return self.readByte()
    
    def __digitalWrite__(self, channel, value):
        mask = 1 << channel
        b = self.readByte()
        if value:
            b |= mask
        else:
            b &= ~mask
        self.writeByte(b)

    def __portWrite__(self, value):
        self.writeByte(value)
        
class PCF8574A(PCF8574):
    def __init__(self, slave=0x38):
        PCF8574.__init__(self, slave)
        
