import machine
import ubinascii


ESSID = "JP_network"
PASSWORD = "chemistry is fun"
MQTT_SERVER = "192.168.0.106"

CLIENT_ID = ubinascii.hexlify(machine.unique_id())

TOPIC_TEMPERATURE = "home/weather_station/temperature"
TOPIC_PRESSURE = "home/weather_station/pressure"
TOPIC_HUMIDITY = "home/weather_station/humidity"
TOPIC_ILLUMINANCE = "home/weather_station/illuminance"

SDA_PIN = 21
SCL_PIN = 22
