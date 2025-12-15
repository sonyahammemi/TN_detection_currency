# ============================================================
# detect_live_publish.py
# YOLOv8 + MQTT + Screenshot annoté
# ============================================================

import cv2
import json
import os
import time
from datetime import datetime
from ultralytics import YOLO
import paho.mqtt.client as mqtt

# ===================== BASE DIR =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ===================== MQTT =====================
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "tn/currency/detection"

# ===================== SCREENSHOTS =====================
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

SCREENSHOT_INTERVAL = 3
last_screenshot_time = 0
img_counter = 0

# ===================== CLASSES =====================
CLASS_NAMES = {
    0: "1 dinar",
    1: "10 dinars",
    2: "10 millimes",
    3: "100 millimes",
    4: "2 dinars",
    5: "20 dinars",
    6: "20 millimes",
    7: "200 millimes",
    8: "5 dinars",
    9: "50 dinars",
    10: "50 millimes",
    11: "500 millimes"
}

# ===================== MODEL =====================
model = YOLO("best.pt")

# ===================== MQTT CLIENT =====================
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# ===================== CAMERA =====================
cap = cv2.VideoCapture(0)
print("📷 Webcam ouverte — appuyez sur q pour quitter")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, conf=0.5)

    detection_found = False
    detected_class_name = None
    confidence = 0.0

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])

            if confidence < 0.6:
                continue

            detected_class_name = CLASS_NAMES.get(cls_id, "Inconnu")
            detection_found = True

    current_time = time.time()

    if detection_found and (current_time - last_screenshot_time > SCREENSHOT_INTERVAL):
        annotated_frame = results[0].plot()
        img_counter += 1

        filename = f"{detected_class_name}_{img_counter}.jpg"
        img_path = os.path.join(SCREENSHOT_DIR, filename)
        cv2.imwrite(img_path, annotated_frame)

        message = {
            "monnaie_detectee": detected_class_name,
            "confiance": round(confidence, 3),
            "date_heure": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "image_path": img_path  
        }

        mqtt_client.publish(MQTT_TOPIC, json.dumps(message, ensure_ascii=False))
        print("📤 MQTT envoyé :", message)

        last_screenshot_time = current_time

    cv2.imshow("Détection Monnaie Tunisienne", results[0].plot())

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
mqtt_client.disconnect()
print("🛑 Programme arrêté")
