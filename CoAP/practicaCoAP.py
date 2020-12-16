#!/usr/bin/env python
from sense_hat import SenseHat
import socket
import sys
import json

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri

__author__ = "Pulido Bejarano Raymundo"

client = None
sense = SenseHat()

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
    
    #return (sense.get_humidity(),sense.get_pressure(),sense.get_temperature())
    return {"Humedad":sense.get_humidity(),"Presion":sense.get_pressure(),"Temperature":sense.get_temperature()}

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


def main():
    global client
    path  = None
    payload = GetEnviromentalValues()
    url = "coap://demo.thingsboard.io/api/v1/hgT6xWy23FyQ1lS0zSK4/telemetry"
    host, port, path = parse_uri(url)
    client = HelperClient(server=(host, port))
    for n in range(10):
        client.post(path, json.dumps(payload),no_response=True)
        payload = GetEnviromentalValues()
    
    client.stop()
    
if __name__ == '__main__':
    main()
