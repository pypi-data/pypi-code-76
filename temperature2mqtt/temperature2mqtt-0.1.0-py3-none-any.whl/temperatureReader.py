

class TemperatureReader:
    def read_temperature(self):
        pass

class TemperatureProxy(TemperatureReader):
    def __init__(self, pin):
        if pin == 99:
            self.reader = TestTemperatureReader()
        else:
            self.reader = TemperatureReaderImpl(pin)

    def read_temperature(self):
        return self.reader.read_temperature()

try:
    import Adafruit_DHT
except ImportError:
    pass
class TemperatureReaderImpl(TemperatureReader):
    def __init__(self, pin):
        self.pin = pin
        self.sensor = Adafruit_DHT.DHT22

    def read_temperature(self):
        return Adafruit_DHT.read_retry(self.sensor, self.pin)

class TestTemperatureReader(TemperatureReader):
    def __init__(self):
        self.min_temperature = -5
        self.max_temperature = 20
        self.temperature = 10
        self.increasing = True

    def read_temperature(self):
        if self.temperature == self.max_temperature:
            self.increasing = False

        if self.temperature == self.min_temperature:
            self.increasing = True

        if self.increasing:
            self.temperature+=0.5

            return 0, self.temperature

        if not self.increasing:
            self.temperature-=0.5

            return 0, self.temperature

