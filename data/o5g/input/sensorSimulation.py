#!/usr/bin/python3
import os
import sys
import time
import json
import random
from datetime import datetime
import paho.mqtt.client as mqtt

MQTT_SERVER = os.environ['O5G_MQTT_SERVER']
MQTT_PORT = int(os.environ['O5G_MQTT_PORT'])
MQTT_USER = os.environ['O5G_MQTT_USER']
MQTT_PASS = os.environ['O5G_MQTT_PASS']

MQTT_TOPIC_SENSOR = os.environ['O5G_MQTT_TOPIC_SENSOR']
#MQTT_TOPIC_SENSOR = os.environ['O5G_MQTT_TOPIC_ALERT']

MAX_WALK_SPEED = 2
FLOOR_ELEVATIONS = [-3, 0, 3, 6]

endLoop: int = 0

uesnr = '''f593e018-9c24-11ed-8ec3-00155d03fb30'''


def main() -> int:

  print('''UE Metric Topic''')
  uemep = mqtt.Client("uemetric_", uesnr) #create new instance
  uemep.username_pw_set(MQTT_USER, MQTT_PASS)
  uemep.connect(MQTT_SERVER, MQTT_PORT, 60)  # connect to broker
  uemep.loop_start()

  # endLoopmuss nicht syncronisiert werden.
  #  Es ist egal ob nun eine Metric mehroderweniger angeliefert wird
  iot_data = {  'measurements': {  'measurements': [  {  'channelIndex': 0
                                                       , 'timestamp':    0
                                                       , 'gasName':      "ch4"
                                                       , 'valueState':   "Valid"
                                                       , 'value':        { 'value': 2500, 'numDigits': 1, 'unit': "PPM"}
                                                       , 'alarmState':   { 'category': "CatNone", 'ackState': "NotAcknowledgable"}
                                                      }
                                                    , {  'channelIndex': 2
                                                       , 'timestamp':    0
                                                       , 'gasName':      "ch4"
                                                       , 'valueState':   "Valid"
                                                       , 'value':        { 'value': 1800, 'numDigits': 1, 'unit': "PPM"}
                                                       , 'alarmState':   { 'category': "CatNone", 'ackState': "NotAcknowledgable"}
                                                      }
                                                    , {  'channelIndex': 4
                                                       , 'timestamp':    0
                                                       , 'gasName':      "CO"
                                                       , 'valueState':   "Valid"
                                                       , 'value':        { 'value': 1800, 'numDigits': 1, 'unit': "PPM"}
                                                       , 'alarmState':   { 'category': "CatNone", 'ackState': "NotAcknowledgable"}
                                                      }
                                                   ]
                                 , 'dLightStatus': False
                                 , 'position': {  'latitude': 53.83867539593222
                                                , 'longitude': 10.660090262678677
                                                , 'elevation': 20
                                               }
                                 , 'device': "Direct_to_cloud_1"
                                }
              , 'device':  uesnr
             }
  lat = 53.0
  lon = 11.0
  level = 0
  while (endLoop == 0):
    # Der Gas Sensor bewegt sich

    lat += random.uniform(-MAX_WALK_SPEED, MAX_WALK_SPEED)
    lon += random.uniform(-MAX_WALK_SPEED, MAX_WALK_SPEED)
    if random.random() > 0.8:
      level = random.choice([max(0,level - 1), min(level + 1, len(FLOOR_ELEVATIONS) - 1)])


    iot_data['measurements']['position']['latitude'] = lat
    iot_data['measurements']['position']['longitude'] = lon
    iot_data['measurements']['position']['elevation'] = FLOOR_ELEVATIONS[level]  # random.choice([-3, 0, 3, 6])
    for metric in iot_data['measurements']['measurements'] :
      metric['value']['value'] = metric['value']['value'] + (random.random()-0.5)
      metric['timestamp']      = int(datetime.now().strftime("%s"))

    # telegraf muss dan auf vgiot/ue/#/metric subscriben
    topic = MQTT_TOPIC_SENSOR + '/' + uesnr
    uemep.publish(topic, json.dumps(iot_data))
    # print("Publishing to " + topic)
    print(json.dumps(iot_data))
    time.sleep(5)

  uemep.loop_stop()
  uemep.disconnect()


  return 0

if __name__ == '__main__':
  import sys
  sys.exit(main())
