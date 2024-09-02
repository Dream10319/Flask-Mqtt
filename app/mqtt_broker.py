import paho.mqtt.client as mqtt


MQTT_BROKER = '13.60.74.162'
MQTT_PORT = 1883
MQTT_USER = 'guest'
MQTT_PASSWORD = 'guest'

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} from topic: {msg.topic}")
    # Call MQTT handler function from another module
    from app.mqtt_handler import MQTTHandler
    handler = MQTTHandler(client)
    handler.message_callback(msg.payload.decode(), msg.topic)

def init_broker():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    return client

def subscribe_to_topic(client, topic):
    if client:
        client.subscribe(topic)
    else:
        raise ValueError("MQTT client is not initialized.")
