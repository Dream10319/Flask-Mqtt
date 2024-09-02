from app.models import SensorData
from uuid import UUID
from app import db
from app import app
import datetime

sensor_data_map = {}

class MQTTHandler:
    def __init__(self, client):
        self.client = client
        # sensor_data_map = {}

    def message_callback(self, message, topic):
        with app.app_context():
            print(f"Processing message: {message} from topic: {topic}")
            global sensor_data_map
            race_id = sensor_data_map.get("race", {}).get("race_id", None)
            if not race_id and topic != "esp32Bis/race":
                print("RaceID not set yet, waiting for RaceID")
                return

            try:
                if topic == "esp32Bis/race":
                    sensor_data_map["race"] = {"race_id": message}
                elif topic in ["esp32Bis/speed", "esp32Bis/distance", "esp32Bis/battery", "esp32Bis/track"]:
                    value = float(message)
                    if topic == "esp32Bis/speed":
                        sensor_data_map["race"]["speed"] = value
                    elif topic == "esp32Bis/distance":
                        sensor_data_map["race"]["distance"] = round(value)
                    elif topic == "esp32Bis/battery":
                        sensor_data_map["race"]["battery"] = round(value)
                    elif topic == "esp32Bis/track":
                        sensor_data_map["race"]["track"] = round(value)
                if all(key in sensor_data_map.get("race", {}) for key in ["race_id", "speed", "distance", "battery"]):
                    sensor_data = SensorData(
                        race_id=sensor_data_map["race"]["race_id"],
                        distance=sensor_data_map["race"]["distance"],
                        speed=sensor_data_map["race"]["speed"],
                        date=datetime.datetime.now(),
                        battery=sensor_data_map["race"]["battery"],
                        track=sensor_data_map["race"].get("track", 0)
                    )
                    db.session.add(sensor_data)
                    db.session.commit()
                    print(f"Sensor data added successfully: {sensor_data}")
                    sensor_data_map = {}

            except Exception as e:
                print(f"Error processing message: {e}")

    def get_sensor_data_by_id(self, race_id):
        return SensorData.query.filter_by(race_id=race_id).all()

    def get_speed_last_ten_min(self, race_id):
        # Implement the SQLAlchemy query for speed in the last ten minutes
        pass

    def get_consumption_last_ten_min(self, race_id):
        # Implement the SQLAlchemy query for consumption in the last ten minutes
        pass
