from .pin import Pin
class Inout(Pin):
    def verilog_type(self):
        return 'inout'
