import paho.mqtt.client as mqtt
import json

control_topic = "iot/control/fan"
device_topic = "iot/device/status"
sensor_lastwill_topic = "iot/sensor/status"
controller_lastwill_topic = "iot/controller/status"

host = "192.168.112.91"
port = 1883
status = "OFF"

def on_message(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    try:
        payload = message.payload.decode()
        data = json.loads(payload)
        print(f"Received from topic {message.topic}: {data}")
        if message.topic == control_topic:
            status = data['status']
            print(f"{status}")
        else:
            pass
    except json.JSONDecodeError:
        print("Received invalied JSON")

client = mqtt.Client()

client.will_set(device_topic, json.dumps({"Device" : "Device offline"}), 1, True)
client.on_message = on_message

client.connect(host, port)
client.subscribe(control_topic)
client.subscribe(sensor_lastwill_topic)
client.subscribe(controller_lastwill_topic)
client.loop_forever()