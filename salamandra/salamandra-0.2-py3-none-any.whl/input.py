from .pin import Pin

class Input(Pin):
    def verilog_type(self):
        return 'input'
