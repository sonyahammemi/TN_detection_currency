import paho.mqtt.client as mqtt
import json

BROKER = "broker.hivemq.com"
PORT = 1883

TOPIC_DETECTION = "tn/currency/detection"
TOPIC_COMMAND = "tn/currency/command"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)
client.loop_start()

def send_command(action):
    payload = {
        "action": action
    }
    client.publish(TOPIC_COMMAND, json.dumps(payload))
