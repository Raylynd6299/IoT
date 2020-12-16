from sense_hat import SenseHat
import paho.mqtt.client as mqttClient
import time
import json
import argparse
import sys
import signal
import os

"""

Practica 3: Utilizando los sensores de la tarjeta Sense HAT, obtener las mediciones de:
    -   Humedad
    -   Presion 
    -   Temperatura
    -   Velocidad
    -   Orientacion
    -   Magnetometro(Compass)
"""

"""
Gestion de Argumentos
    -   All     ->  Se mandaran las varibles de entorno y de movimiento
    -   Ent     ->  Se enviaran las variables de entorno (Presion,Temperatura,Humedad)
    -   Mov     ->  Se enviaran las variables de movimiento (Magnetometro,Gyroscopio,Acceleracion)
"""
parser = argparse.ArgumentParser()
parser.add_argument("Vars",help="Designe que variables se enviaran All, Ent, Mov")

"""
Variables Globales
    -   Gestion de MQTT
    -   Sense Hat
    -   Argumentos
"""

args = parser.parse_args()       
sense = SenseHat()
connected = False  
BROKER_ENDPOINT = "industrial.api.ubidots.com"  
PORT = 1883
MQTT_USERNAME = "BBFF-4aGyXQAP2KKxtwunvmyKsUHs87BVwe"  #Token
MQTT_PASSWORD = ""
TOPIC = "/v1.6/devices/"
DEVICE_LABEL = "Raspberry-Ray"
Varibles_Labels = []
mqtt_client_G = None
Activo = True


"""
Gestion de Señales
    -   SIGINT      ->  Señal generada cuando el usuario termina un proceso usando Ctrl+C
"""
def GestionarSeñal(signum,stack):
    global mqtt_client_G,Activo
    if mqtt_client_G != None:
        mqtt_client_G.disconnect()
        mqtt_client_G.loop_stop()
    print("\nCerrando Canal de Comunicacion\n")
    Activo = False
    sys.exit(os.EX_OK)
 
signal.signal(signal.SIGINT,GestionarSeñal)


"""
    Funciones de Coneccion MQTT
"""

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[INFO] Conectado con el Broker")
        global connected  
        connected = True  
    else:
        print("[INFO] Error, conexion fallida")

def on_publish(client, userdata, result):
    print("[INFO] Publicado!")

def connect(mqtt_client, mqtt_username, mqtt_password, broker_endpoint, port):
    global connected

    if not connected:
        mqtt_client.username_pw_set(mqtt_username, password=mqtt_password)
        mqtt_client.on_connect = on_connect
        mqtt_client.on_publish = on_publish
        mqtt_client.connect(broker_endpoint, port=port)
        mqtt_client.loop_start()

        attempts = 0

        while not connected and attempts < 5:  # Waits for connection
            print("[INFO] Intentando Conectar...")
            time.sleep(1)
            attempts += 1

    if not connected:
        print("[ERROR] No se pudo conectar con el Broker")
        return False

    return True

def publish(mqtt_client, topic, payload):
    try:
        mqtt_client.publish(topic, payload)
    except Exception as e:
        print(f"[ERROR] Tuvimos un error, detalles: \n{e}")


"""
    Funciones del SenseHat
"""
    
def GetEnviromentalValues():
    """
        return -> Humedad, Presion, Temperatura
        
        Humedad         -> Humedad Relativa al ambiente
        Presion         -> Presion actual en Milibars
        Temperatura     -> Obtiene la temperatura del ambiente en Grados Celsius
        
    """
    global sense
    
    return (sense.get_humidity(),sense.get_pressure(),sense.get_temperature())

def GetMoveValues_raw():
    """
        return -> (OrientatioAxis),(GyroscopioAxis),(AccelertionAxis)
        
        OrientatioAxis      -> (Pitch (X), Roll (Y), Yaw (Z)) axis 
        GyroscopioAxis      -> (X,Y,Z) representing the rotational intensity of the axis in radians per second.
        AccelertionAxis     -> (X,Y,Z) representing the acceleration intensity of the axis in Gs.
        
    """
    global sense
    sense.set_imu_config(True,True,True)
    OrientatioAxis  = tuple(sense.get_orientation().values())
    GyroscopioAxis  = tuple(sense.get_gyroscope_raw().values())
    AccelertionAxis = tuple(sense.get_accelerometer_raw().values()) 
    
    return (OrientatioAxis,GyroscopioAxis,AccelertionAxis)
    
def GetMoveValues():
    """
        return -> compass,(Gyroscope),(Accelerometer)
        
        compass         -> The direction of North
        Gyroscope       -> (Pitch (X), Roll (Y), Yaw (Z)) Representing the angle of the axis in degrees.
        Accelerometer   -> (Pitch (X), Roll (Y), Yaw (Z)) Representing the angle of the axis in degrees.
    """
    global sense
    
    Gyroscope = tuple(sense.get_gyroscope().values())
    Acceleration = tuple(sense.get_accelerometer().values())
    
    return (sense.get_compass(),Gyroscope,Acceleration)

"""
    Funcion main
"""
def main(mqtt_client):
    global Varibles_Labels,args,MQTT_USERNAME,MQTT_PASSWORD,BROKER_ENDPOINT,PORT,connected,DEVICE_LABEL,TOPIC
    values = ()
    
    #Designar que variables seran enviadas
    if (args.Vars == "All"):
        Varibles_Labels = ["Humedad","Presion","Temperatura","Orientacion","Gyroscopio","Acceleracion"]
        values = GetEnviromentalValues()
        values = values + GetMoveValues_raw()
    elif(args.Vars == "Ent"):
        Varibles_Labels = ["Humedad","Presion","Temperatura"]
        values = GetEnviromentalValues()
    elif(args.Vars == "Mov"):
        Varibles_Labels = ["Orientacion","Gyroscopio","Acceleracion"]
        values = GetMoveValues_raw()
    else:
        print("Error en el parametro, ingrese un valor correcto!")
        sys.exit(1)
    
    #Creando Payload 
    payload = {}
    for indice,variable in enumerate(Varibles_Labels):
        payload[variable] = values[indice]

    payload = json.dumps(payload)
    topic = "{}{}".format(TOPIC, DEVICE_LABEL)

    if not connected:  # Connects to the broker
        connect(mqtt_client, MQTT_USERNAME, MQTT_PASSWORD,BROKER_ENDPOINT, PORT)

    # Publicando valores
    print(f"[INFO] Intentando publicar el payload:\n{payload}")
    
    publish(mqtt_client, topic, payload)

if __name__ == '__main__':        
    #global mqtt_client_G
    mqtt_client = mqttClient.Client()
    mqtt_client_G = mqtt_client
    while Activo:
        main(mqtt_client)
        time.sleep(1)    