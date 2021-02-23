
from rocket.daisy.utils.types import M_JSON
from rocket.daisy.devices.digital.mcp23XXX import MCP23S17
from rocket.daisy.decorators.rest import request, response


class PiFaceDigital():
    def __init__(self, board=0):
        mcp = MCP23S17(0, 0x20+board)
        mcp.writeRegister(mcp.getAddress(mcp.IODIR, 0), 0x00) # Port A as output
        mcp.writeRegister(mcp.getAddress(mcp.IODIR, 8), 0xFF) # Port B as input
        mcp.writeRegister(mcp.getAddress(mcp.GPPU,  0), 0x00) # Port A PU OFF
        mcp.writeRegister(mcp.getAddress(mcp.GPPU,  8), 0xFF) # Port B PU ON
        self.mcp = mcp
        self.board = board
        
    def __str__(self):
        return "PiFaceDigital(%d)" % self.board 

    def __family__(self):
        return "PiFaceDigital"
    
    def checkChannel(self, channel):
        if not channel in range(8):
            raise ValueError("Channel %d invalid" % channel)
    
    @request("GET", "digital/input/%(channel)d")
    @response("%d")
    def digitalRead(self, channel):
        self.checkChannel(channel)
        return not self.mcp.digitalRead(channel+8)
    
    @request("POST", "digital/output/%(channel)d/%(value)d")
    @response("%d")
    def digitalWrite(self, channel, value):
        self.checkChannel(channel)
        return self.mcp.digitalWrite(channel, value)
    
    @request("GET", "digital/output/%(channel)d")
    @response("%d")
    def digitalReadOutput(self, channel):
        self.checkChannel(channel)
        return self.mcp.digitalRead(channel)
    
    @request("GET", "digital/*")
    @response(contentType=M_JSON)
    def readAll(self):
        inputs = {}
        outputs = {}
        for i in range(8):
            inputs[i] = self.digitalRead(i)
            outputs[i] = self.digitalReadOutput(i)
        return {"input": inputs, "output": outputs}
