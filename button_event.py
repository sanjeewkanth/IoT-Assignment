import paho.mqtt.client as mqtt
import pyfirmata, pyfirmata.util
import time
import sys
import json




mqttBroker = "test.mosquitto.org"
client = mqtt.Client("button-event")
client.connect(mqttBroker)

board = pyfirmata.Arduino('COM4', baudrate=57600)

iterator = pyfirmata.util.Iterator(board)
iterator.start()

#time.sleep(1)

button = board.get_pin('d:2:i')

#time.sleep(1)
button.enable_reporting()

for i in range(100):
    print ("Button state: %s" % button.read())
    # The return values are: True False, and None
    if str(button.read()) == 'True':
        print ("Button pressed")
        btn_time = time.time()
        while str(button.read()) == 'True':
            print("Button is being pressed")
            btn1_time = time.time()
            if btn1_time - btn_time > 5:
                print("Button pressed ", round((btn1_time-btn_time)*1000))

                button_event = {
                    "event": "button_press",
                    "duration": round((btn1_time-btn_time)*1000)
                }
                m_out=json.dumps(button_event)
                client.publish("/sanjeewkanth/button-event", m_out)
                sys.exit()

    elif str(button.read()) == 'False':
        print ("Button not pressed")
    else: 
        print ("Button was never pressed")
    board.pass_time(0.5)


board.exit()


