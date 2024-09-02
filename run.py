from app import create_app
from app.mqtt_broker import subscribe_to_topic
from app import mqtt_client
import os

app = create_app()

if __name__ == '__main__' :
    # Subscribe to MQTT topics
    
    subscribe_to_topic(mqtt_client, "esp32Bis/#")  # Subscribe to all topics under "esp32Bis"
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
