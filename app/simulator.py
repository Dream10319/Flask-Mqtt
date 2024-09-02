import paho.mqtt.client as mqtt
import random
import time
import uuid

# Configuration du broker MQTT
MQTT_BROKER = "13.60.74.162"  # Remplace par l'adresse de ton broker
MQTT_PORT = 1883
MQTT_TOPIC_RACE = "esp32Bis/race"
MQTT_TOPIC_SPEED = "esp32Bis/speed"
MQTT_TOPIC_DISTANCE = "esp32Bis/distance"
MQTT_TOPIC_BATTERY = "esp32Bis/battery"


# Fonction pour générer des données aléatoires au format float
def generate_random_data():

    race_id = "16776471-3eeb-4483-aed2-4f79e42f736f"
    speed = random.uniform(0, 100)  # Vitesse entre 0 et 100
    distance = random.uniform(0, 1000)  # Distance entre 0 et 1000
    battery = random.uniform(0, 100)  # Niveau de batterie entre 0 et 100
    return {
        "race_id": race_id,
        "speed": speed,
        "distance": distance,
        "battery": battery
    }


# Fonction de publication
def publish_data(client):
    while True:
        data = generate_random_data()

        # Formater les valeurs en chaînes de caractères avec 2 chiffres après la virgule
        race_id_str = str(data["race_id"])
        speed_str = format(data["speed"], ".2f")
        distance_str = format(data["distance"], ".2f")
        battery_str = format(data["battery"], ".2f")

        # Publication sur les différents topics avec les chaînes formatées
        print(f"Publication de la race id : {race_id_str}")
        client.publish(MQTT_TOPIC_RACE, race_id_str)

        print(f"Publication de la vitesse : {speed_str}")
        client.publish(MQTT_TOPIC_SPEED, speed_str)

        print(f"Publication de la distance : {distance_str}")
        client.publish(MQTT_TOPIC_DISTANCE, distance_str)

        print(f"Publication du niveau de batterie : {battery_str}")
        client.publish(MQTT_TOPIC_BATTERY, battery_str)

        time.sleep(5)  # Attendre 2 secondes avant de publier à nouveau


# Configuration du client MQTT
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Lancer la publication des données
publish_data(client)
