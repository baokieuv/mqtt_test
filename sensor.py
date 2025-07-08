import paho.mqtt.client as mqtt
import random
import json
import time

temp_topic = "iot/sensor/temp"
sensor_lastwill_topic = "iot/sensor/status"
controller_lastwill_topic = "iot/controller/status"
device_lastwill_topic = "iot/device/status"

host = "192.168.112.91"
port = 1883

def on_message(client, userdata, message: mqtt.MQTTMessage):
    try:
        payload = message.payload.decode()
        data = json.loads(payload)
        print(f"Received from topic {message.topic}: {data}")
    except json.JSONDecodeError:
        print("Received invalied JSON")

client = mqtt.Client()

client.will_set(sensor_lastwill_topic, json.dumps({"Sensor" : "Sensor offline"}), 1, True)
client.on_message = on_message

client.connect(host, port)
client.subscribe(controller_lastwill_topic)
client.subscribe(device_lastwill_topic)
client.loop_start()

while True:
    temp = random.randint(20, 50)
    data = {
        "temperature" : temp,
    }
    message = json.dumps(data)
    client.publish(temp_topic, message, 1, True)
    print(f"Publish {data}")
    time.sleep(5)

