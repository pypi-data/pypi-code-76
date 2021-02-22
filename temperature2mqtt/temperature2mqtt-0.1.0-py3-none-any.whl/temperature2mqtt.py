import json
import paho.mqtt.client as mqtt
import time
import argparse
import temperature2mqtt.temperatureReader
from temperature2mqtt.temperatureReader import TemperatureProxy

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        return
        
    if rc == 5:
        print("Username or password incorrect.")
    else:
        print(f"Error connecting to MQTT. RC: {rc}")


def set_username_pw():
    if args.username is not None:
        mqtt_client.username_pw_set(args.username, args.password)

parser = argparse.ArgumentParser(description="DHT22 temperatre to MQTT")
parser.add_argument("-host", required=True)
parser.add_argument("-username")
parser.add_argument("-password")
parser.add_argument("-pin", required=True, type=int)
parser.add_argument("-topic", required=True)

args = parser.parse_args()

mqtt_client = mqtt.Client()
set_username_pw()
mqtt_client.on_connect = on_connect

mqtt_client.connect(args.host)
mqtt_client.loop_start()

reader = TemperatureProxy(args.pin)

while True:
    humidity, temperature = reader.read_temperature()
    data = dict()
    data['temperature'] = temperature
    data['humidity'] = humidity

    mqtt_client.publish(args.topic, json.dumps(data))
    print(temperature)

    time.sleep(30)

