

import time
from rocket.daisy.utils.types import toint
from rocket.daisy.devices.i2c import I2C
from rocket.daisy.devices.analog import PWM

class PCA9685(PWM, I2C):
    MODE1    = 0x00
    PWM_BASE = 0x06
    PRESCALE = 0xFE
    
    M1_SLEEP    = 1<<4
    M1_AI       = 1<<5
    M1_RESTART  = 1<<7
    
    def __init__(self, slave=0x40, frequency=50):
        I2C.__init__(self, toint(slave))
        PWM.__init__(self, 16, 12, toint(frequency))
        self.VREF = 0
        
        self.prescale = int(25000000.0/((2**12)*self.frequency))
        self.mode1 = self.M1_RESTART | self.M1_AI
        
        self.writeRegister(self.MODE1, self.M1_SLEEP)
        self.writeRegister(self.PRESCALE, self.prescale)
        time.sleep(0.01)

        self.writeRegister(self.MODE1, self.mode1)
        
    def __str__(self):
        return "PCA9685(slave=0x%02X)" % self.slave

    def getChannelAddress(self, channel):
        return int(channel * 4 + self.PWM_BASE) 

    def __pwmRead__(self, channel):
        addr = self.getChannelAddress(channel)
        d = self.readRegisters(addr, 4)
        start = d[1] << 8 | d[0]
        end   = d[3] << 8 | d[2]
        return end-start
    
    def __pwmWrite__(self, channel, value):
        addr = self.getChannelAddress(channel)
        d = bytearray(4)
        d[0] = 0
        d[1] = 0
        d[2] = (value & 0x0FF)
        d[3] = (value & 0xF00) >> 8
        self.writeRegisters(addr, d)
