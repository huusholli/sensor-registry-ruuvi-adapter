import os

from python_http_client import Client
from ruuvitag_sensor.ruuvi import RuuviTagSensor
from tinydb import TinyDB
from tinydb import Query

client = Client(host=os.environ['SENSOR_REGISTRY_HOST'])
db = TinyDB('data/database.json')

def handle_ruuvi_data(found_data):
  data = found_data[1]

  if data.get('data_format') != 5:
    return

  mac = data.get('mac')

  register_ruuvi_sensor_data(mac, 'temperature', data)
  register_ruuvi_sensor_data(mac, 'humidity', data)
  register_ruuvi_sensor_data(mac, 'pressure', data)

def register_ruuvi_sensor_data(mac, sensor_type, data):
  sensor = get_local_sensor(mac, sensor_type) or register_sensor(mac, sensor_type)
  post_sensor_data(sensor.get('sensor_id'), data.get(sensor_type))

def get_local_sensor(mac, sensor_type):
  Sensor = Query()
  return db.get((Sensor.mac == mac) & (Sensor.sensor_type == sensor_type))

def register_sensor(mac, sensor_type):
  data = {'type': sensor_type, 'offlineTimeout': 30, 'group': 'RuuviTag ' + mac}

  response = client.sensors.post(request_body=data)
  sensor = {'mac': mac, 'sensor_type': sensor_type, 'sensor_id': response.to_dict.get('id')}

  db.insert(sensor)
  return sensor

def post_sensor_data(sensor_id, value):
  data = {'value': value}
  client.sensors._(sensor_id).data.post(data)

RuuviTagSensor.get_datas(handle_ruuvi_data)
