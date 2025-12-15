
📌 Objectif

Développer une application web moderne permettant :

L’affichage des détections

L’analyse statistique

L’envoi de commandes vers l’objet connecté

🧱 Architecture Web

Framework : Streamlit

Base de données : SQLite

Communication IoT : MQTT

🛠️ Technologies utilisées

Python

Streamlit

Pandas

SQLite

Paho-MQTT

📂 Structure
web_app/
│── app.py
│── database.py
│── mqtt_client.py
│── styles.css
│── detections.db
│── requirements.txt


▶️ Lancement de l’application
pip install -r requirements.txt
streamlit run app.py
🖥️ Fonctionnalités

Dashboard interactif

Tableau des détections

Graphiques statistiques

Boutons de commande (ouvrir porte, fermer, alerte)

Export CSV