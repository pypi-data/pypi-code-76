# coding: utf-8
"""
Python script for requesting datapoints from 1-wire-protocol sensors and
report it to an InfluxDB-bucket.
"""
import time
from w1thermsensor import W1ThermSensor, Sensor
from .helpers import PysentelConfig, InfluxDataIngest


def main():
    """
    Main function. Run continuously with the provided sleep-delay interval.
    """
    # Initialize configurations
    config = PysentelConfig()

    # Initialize InfluxDB connection
    influxdb = InfluxDataIngest(url=config.influxdb['url'],
                                org=config.influxdb['org'],
                                bucket=config.influxdb['bucket'],
                                token=config.influxdb['token'])

    # Run loop as long as this service is running
    while True:
        datapoints = []
        # Initialize 1-wire and get available sensors
        for sensor in W1ThermSensor.get_available_sensors([Sensor.DS18B20]):
            # Append all sensor datapoints to ingest-list with correct
            # informations
            datapoints.append({
                'measurement': 'temperature',
                'tags': {
                    'location': config.sensors[sensor.id],
                    'type': sensor.type.name,
                    'sensor-id': sensor.id},
                'fields': {
                    'value': sensor.get_temperature()}
            })

        # Ingest data
        influxdb.write_points(datapoints)

        time.sleep(config.interval)
