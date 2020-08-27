from os import getenv

from python_http_client import Client
from ruuvitag_sensor.ruuvi import RuuviTagSensor

client = Client(host=getenv('SENSOR_REGISTRY_HOST'))

def handle_ruuvi_data(found_data):
  data = found_data[1]

  if data.get('data_format') != 5:
    return

  mac = data.get('mac')

  post_sensor_data('Ruuvi {}'.format(mac), data)

def post_sensor_data(sensor_id, value):
  data = [
    {'name': 'temperature', 'value': value.get('temperature')},
    {'name': 'humidity', 'value': value.get('humidity')},
    {'name': 'pressure', 'value': value.get('pressure')},
  ]

  print(data)
  client.post(data, request_headers={'x-device-id': sensor_id})

RuuviTagSensor.get_datas(handle_ruuvi_data)
