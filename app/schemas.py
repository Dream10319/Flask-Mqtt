from marshmallow import Schema, fields

class VehicleSchema(Schema):
    id = fields.UUID()
    name = fields.Str()

class RaceSchema(Schema):
    id = fields.UUID()
    vehicle_id = fields.UUID()
    name = fields.Str()
    date = fields.DateTime()

class SensorDataSchema(Schema):
    id = fields.UUID()
    race_id = fields.UUID()
    distance = fields.Float()
    speed = fields.Float()
    date = fields.DateTime()
    battery = fields.Float()
    track = fields.Int()

class StatsRaceSchema(Schema):
    id = fields.UUID()
    race_id = fields.UUID()
    distance = fields.Float()
    speed_max = fields.Float()
    speed_average = fields.Float()
    battery_max = fields.Int()
    battery_min = fields.Int()
    time = fields.Int()
    date = fields.DateTime()
