import paho.mqtt.client as mqtt
import time
import pyfirmata
import psutil
import json
import sys



def write_json(new_data, filename,title):
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data[title].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

#we connect to the Arduino pin13
pin = 13
#Define the port
port = 'COM4'
#connect Arduino to python through pyfirmata library
board = pyfirmata.Arduino('COM4')
#ON the LED in arduini
board.digital[13].write(1)


#Define the MQTT server and connect to it
mqttBroker = "test.mosquitto.org"
client = mqtt.Client("PC-EVENT")
client.connect(mqttBroker)


#Get the time value
starttime = time.time()
while True:
    #Take the seconds
    X = round(60 -((time.time() - starttime) % 60))
    #if modulus of time equals zero, then it samle data for every 30s
    if X % 30 == 0:
        #Usung psutil library to extract pc data
        CPU = psutil.cpu_percent()
        RAM = psutil.virtual_memory().percent
        #take the round value of time
        time_per = round(time.time())
        #publish the event on MQTT


        cpu_data = str(CPU)
        cpu_per = cpu_data + "%"
        ram_data = str(RAM)
        ram_per = ram_data + "%"

        print("RAM usage is " + cpu_per)
        print("CPU usage is " + ram_per)
        print(time.time())


        pc_event = {
                "cpu":cpu_per,
                "ram": ram_per,
                "timestamp": time_per
            }
        cpu_event = {
                "cpu":cpu_per,
                "timestamp": time_per
            }
        if CPU >= 50:
            m_out=json.dumps(cpu_event)
            client.publish("/sanjeewkanth/pc-event", m_out)
            #client.publish("/sanjeewkanth/pc-event", time_per)
            write_json(cpu_event,'cpu.json','cpu-event')
            print("Just published " + str(CPU) + " to Topic /sanjeewkanth/pc-event")
            print("Just published " + time_per + " to Topic /sanjeewkanth/pc-event")


        #update the JSON file
        write_json(pc_event,'pc.json','pc-event')
        time.sleep(0.7)
    #else:
        #time.sleep(1)
        #make the LED BLINK if the RAM usage is more than 80% 
    if RAM >= 80:
        board.digital[13].write(1)
        time.sleep(1/40)
        board.digital[13].write(0)
        time.sleep(1/40)
    else:
        board.digital[13].write(0)
