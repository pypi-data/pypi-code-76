from .pin import Pin

class Output(Pin):
    def verilog_type(self):
        return 'output'
