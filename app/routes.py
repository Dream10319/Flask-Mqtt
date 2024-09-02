from flask import Blueprint, request, jsonify
from app.models import Vehicle, Race, SensorData, StatsRace
from app import db, mqtt_client
from app.mqtt_handler import MQTTHandler

routes = Blueprint('routes', __name__)

mqtt_handler = MQTTHandler(mqtt_client)

@routes.route('/vehicle', methods=['POST'])
def add_vehicle():
    data = request.json
    try:
        vehicle = Vehicle(name=data['name'])
        db.session.add(vehicle)
        db.session.commit()
        return jsonify({'message': 'Vehicle successfully added', 'data': vehicle.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@routes.route('/vehicle/<id>', methods=['GET'])
def get_vehicle_by_id(id):
    vehicle = Vehicle.query.get_or_404(id)
    return jsonify({'data': vehicle.to_dict()})

@routes.route('/vehicle/<id>', methods=['DELETE'])
def delete_vehicle_by_id(id):
    vehicle = Vehicle.query.get_or_404(id)
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({'message': 'Vehicle successfully deleted'})

@routes.route('/vehicle/<id>', methods=['PUT'])
def update_vehicle_by_id(id):
    data = request.json
    vehicle = Vehicle.query.get_or_404(id)
    vehicle.name = data['name']
    db.session.commit()
    return jsonify({'message': 'Vehicle successfully updated', 'data': vehicle.to_dict()})

@routes.route('/race', methods=['POST'])
def add_race():
    data = request.json
    try:
        race = Race(vehicle_id=data['vehicle_id'], name=data['name'])
        db.session.add(race)
        db.session.commit()
        return jsonify({'message': 'Race successfully added', 'data': race.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@routes.route('/race/<id>', methods=['GET'])
def get_race_by_id(id):
    race = Race.query.get_or_404(id)
    return jsonify({'data': race.to_dict()})

@routes.route('/race/<id>', methods=['DELETE'])
def delete_race_by_id(id):
    race = Race.query.get_or_404(id)
    db.session.delete(race)
    db.session.commit()
    return jsonify({'message': 'Race successfully deleted'})

@routes.route('/race/<id>', methods=['PUT'])
def update_race_by_id(id):
    data = request.json
    race = Race.query.get_or_404(id)
    race.name = data['name']
    db.session.commit()
    return jsonify({'message': 'Race successfully updated', 'data': race.to_dict()})

@routes.route('/sensor_data', methods=['POST'])
def add_sensor_data():
    data = request.json
    try:
        sensor_data = SensorData(
            race_id=data['race_id'],
            distance=data['distance'],
            speed=data['speed'],
            date=data['date'],
            battery=data['battery'],
            track=data['track']
        )
        db.session.add(sensor_data)
        db.session.commit()
        return jsonify({'message': 'Sensor data successfully added', 'data': sensor_data.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@routes.route('/sensor_data/<race_id>/speed', methods=['GET'])
def get_speed_last_ten_min(race_id):
    data = mqtt_handler.get_speed_last_ten_min(race_id)
    if data:
        return jsonify({'data': data}), 200
    else:
        return jsonify({'message': 'Error fetching speed'}), 500

@routes.route('/sensor_data/<race_id>/consumption', methods=['GET'])
def get_consumption_last_ten_min(race_id):
    data = mqtt_handler.get_consumption_last_ten_min(race_id)
    if data:
        return jsonify({'data': data}), 200
    else:
        return jsonify({'message': 'Error fetching consumption'}), 500

@routes.route('/stats_race', methods=['POST'])
def add_stats_race():
    data = request.json
    try:
        stats_race = StatsRace(
            race_id=data['race_id'],
            distance=data['distance'],
            speed_max=data['speed_max'],
            speed_average=data['speed_average'],
            battery_max=data['battery_max'],
            battery_min=data['battery_min'],
            time=data['time'],
            date=data['date']
        )
        db.session.add(stats_race)
        db.session.commit()
        return jsonify({'message': 'Stats race successfully added', 'data': stats_race.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@routes.route('/stats_race/<id>', methods=['GET'])
def get_stats_race_by_id(id):
    stats_race = StatsRace.query.get_or_404(id)
    return jsonify({'data': stats_race.to_dict()})

@routes.route('/stats_race/<id>', methods=['DELETE'])
def delete_stats_race_by_id(id):
    stats_race = StatsRace.query.get_or_404(id)
    db.session.delete(stats_race)
    db.session.commit()
    return jsonify({'message': 'Stats race successfully deleted'})

@routes.route('/stats_race/<id>', methods=['PUT'])
def update_stats_race_by_id(id):
    data = request.json
    stats_race = StatsRace.query.get_or_404(id)
    stats_race.distance = data['distance']
    stats_race.speed_max = data['speed_max']
    stats_race.speed_average = data['speed_average']
    stats_race.battery_max = data['battery_max']
    stats_race.battery_min = data['battery_min']
    stats_race.time = data['time']
    stats_race.date = data['date']
    db.session.commit()
    return jsonify({'message': 'Stats race successfully updated', 'data': stats_race.to_dict()})
