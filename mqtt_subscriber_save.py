import json
import sqlite3
import paho.mqtt.client as mqtt
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "web_app", "detections.db")

print(" DB utilisée :", DB_PATH)

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "tn/currency/detection"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            monnaie TEXT,
            confidence REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Table detections prête")

def on_connect(client, userdata, flags, rc):
    print("✅ MQTT connecté")
    client.subscribe(MQTT_TOPIC)
    print(" Abonné à", MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(" Message brut reçu :", msg.payload)

    data = json.loads(msg.payload.decode())

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "INSERT INTO detections (monnaie, confidence, timestamp) VALUES (?, ?, ?)",
        (
            data["monnaie_detectee"],
            data["confiance"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    conn.commit()

    # 🔍 Vérification directe
    c.execute("SELECT COUNT(*) FROM detections")
    total = c.fetchone()[0]

    conn.close()

    print(f"✅ INSERT OK | Total lignes DB = {total}")

init_db()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
