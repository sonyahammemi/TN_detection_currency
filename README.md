# 💰 TN Currency Detection – IoT & Deep Learning

## 📌 Description générale

Ce projet consiste à concevoir un **objet connecté intelligent** capable de détecter automatiquement des **monnaies tunisiennes** à l’aide du **Deep Learning**, puis de transmettre les résultats via un **broker MQTT cloud** vers une **application web** pour l’affichage, l’analyse et le contrôle.

Le projet a été réalisé dans le cadre du module **MP2L – IoT & Deep Learning**.

---

## 🎯 Objectifs du projet

* Détecter des monnaies tunisiennes à partir d’une webcam
* Utiliser un modèle de Deep Learning (YOLOv8)
* Publier les résultats de détection via MQTT
* Sauvegarder les données dans une base de données
* Afficher les résultats dans une application web interactive
* Envoyer des commandes depuis l’application vers l’objet connecté

---

## 🧠 Technologies utilisées

* **Langage** : Python
* **Deep Learning** : YOLOv8 (Ultralytics)
* **Vision par ordinateur** : OpenCV
* **IoT / Communication** : MQTT (HiveMQ)
* **Web App** : Streamlit
* **Base de données** : SQLite

---

## 🗂️ Structure du projet

```
TN_CURRENCY_DETECTION/
│
├── dataset/                 # Dataset (images + labels)
├── notebook/                # Entraînement du modèle DL
│   └── iot_project.ipynb
├── screenshots/             # Images détectées et annotées
│
├── app.py                   # Application web Streamlit
├── database.py              # Gestion de la base SQLite
├── mqtt_client.py           # Client MQTT (commandes)
├── styles.css               # Style de l’interface web
├── detections.db            # Base de données
│
├── detect_live_publish.py   # Détection en temps réel + Publish MQTT
├── mqtt_subscriber_save.py  # Subscriber MQTT + sauvegarde DB
├── best.pt                  # Modèle YOLOv8 entraîné
├── data.yaml                # Configuration YOLO
│
├── requirements.txt         # Dépendances Python
└── README.md                # Documentation du projet
```

---

## 🟥 Partie 1 : Deep Learning

* Construction d’un dataset de monnaies tunisiennes
* Entraînement d’un modèle YOLOv8 sur Google Colab
* Évaluation et sauvegarde du meilleur modèle (`best.pt`)

📁 Fichier principal : `iot_project.ipynb`

---

## 🟦 Partie 2 : IoT & MQTT

* Mise en place d’un broker MQTT cloud (HiveMQ)
* Publication des résultats de détection dans un topic MQTT
* Réception des données côté backend
* Sauvegarde des détections dans SQLite

📁 Fichiers principaux :

* `detect_live_publish.py`
* `mqtt_subscriber_save.py`

---

## 🟩 Partie 3 : Application Web

* Développement d’une application web avec Streamlit
* Affichage des détections et statistiques
* Envoi de commandes MQTT (ouvrir/fermer porte, alerte)
* Export des données

📁 Fichier principal : `app.py`

---

## ▶️ Lancement du projet

### 1️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2️⃣ Lancer le subscriber MQTT

```bash
python mqtt_subscriber_save.py
```

### 3️⃣ Lancer la détection (publisher)

```bash
python detect_live_publish.py
```

### 4️⃣ Lancer l’application web

```bash
streamlit run app.py
```

---

## ✅ Résultat final

* Détection automatique des monnaies tunisiennes
* Communication IoT temps réel via MQTT
* Application web moderne et interactive
* Projet complet combinant **IA + IoT + Web**

---

👩‍🎓 *Projet réalisé dans le cadre du module MP2L – IoT & Deep Learning*
