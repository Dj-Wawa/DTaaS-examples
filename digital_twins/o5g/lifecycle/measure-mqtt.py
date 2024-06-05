import paho.mqtt.client as mqtt
import time
import json
from collections import deque
import numpy as np

# Configuration
BROKER = 'dtaas-digitaltwin.com'
MQTT_USER = 'dtaas'
MQTT_PASS = 'EaGoo9geequishi'
MQTT_PORT = 8091

#BROKER = 'dtl-server-2.st.lab.au.dk'
#MQTT_USER = 'o5g'
#MQTT_PASS = 'Berlin2022#Frankfurt'
#MQTT_PORT = 8090

REQUEST_TOPIC = 'vgiot/ue/metric'
RESPONSE_TOPIC = 'vgiot/dt/alerts'

# Queue to store the time when requests are received
request_timestamps = deque()
# List to store latency measurements
latencies = []

# Callback when the client receives a CONNACK response from the server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc) +" at "+ time.ctime())
    print(f"Message, latency, average, std-dev")
    # Subscribing to the request and response topics
    client.subscribe(REQUEST_TOPIC + '/#', qos=1)
    client.subscribe(RESPONSE_TOPIC + '/#', qos=1)

# Callback when a PUBLISH message is received from the server
def on_message(client, userdata, msg):
    #print(f'message on topic: {msg.topic}')
    current_time = time.time()
    
    if msg.topic.startswith(REQUEST_TOPIC):
        # Log the timestamp when a request is received
        request_timestamps.append(current_time)
        #print(f"Received request at {current_time}")
    
    elif msg.topic.startswith(RESPONSE_TOPIC):
        if request_timestamps:
            # Calculate latency for the corresponding request
            request_time = request_timestamps.popleft()
            latency = (current_time - request_time) * 1000  # Convert to milliseconds
            latencies.append(latency)
            
            # Calculate average and standard deviation
            avg_latency = np.mean(latencies)
            std_latency = np.std(latencies)
            total_messages = len(latencies)
            
            print(f"{total_messages}, {latency}, {avg_latency}, {std_latency}")
            if(total_messages >= 500):
                client.disconnect()
        else:
            print("Received a response but no matching request timestamp")

# Initialize the MQTT client
client = mqtt.Client("measurement")
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, MQTT_PORT, 60)

# Start the MQTT client in a blocking way
client.loop_forever()
