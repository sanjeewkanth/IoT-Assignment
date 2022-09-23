import paho.mqtt.client as mqtt
import time
import json

def on_message(client, userdata, message):
    #print(message.payload.decode("utf-8"))
    m_out = json.loads(message.payload.decode("utf-8"))
    m_in = json.dumps(m_out)
    print(m_out)




mqttBroker = "test.mosquitto.org"
client = mqtt.Client("Smartphone")
client.connect(mqttBroker)

client.loop_start()
#client.subscribe("/sanjeewkanth/pc-event")
client.subscribe("/sanjeewkanth/button-event")
client.on_message=on_message
time.sleep(100)
client.loop_stop()
