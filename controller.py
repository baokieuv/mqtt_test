import paho.mqtt.client as mqtt
import json

control_topic = "iot/control/fan"
temp_topic = "iot/sensor/temp"
sensor_lastwill_topic = "iot/sensor/status"
controller_lastwill_topic = "iot/controller/status"
device_lastwill_topic = "iot/device/status"

host = "192.168.112.91"
port = 1883

def on_message(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    try:
        payload = message.payload.decode()
        data = json.loads(payload)
        print(f"Received from topic {message.topic}: {data}")
        if message.topic == temp_topic:
            if data['temperature'] > 40:
                client.publish(control_topic, json.dumps({"status" : "ON"}), 1, True)
            else:
                client.publish(control_topic, json.dumps({"status" : "OFF"}), 1, True)
        else:
            pass
    except json.JSONDecodeError:
        print("Received invalied JSON")

client = mqtt.Client()

client.will_set(controller_lastwill_topic, json.dumps({"Controller" : "Controller offline"}), 1, True)
client.on_message = on_message

client.connect(host, port)
client.subscribe(temp_topic)
client.subscribe(sensor_lastwill_topic)
client.subscribe(device_lastwill_topic)
client.loop_forever()


