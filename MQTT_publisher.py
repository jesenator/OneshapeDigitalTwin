import paho.mqtt.client as mqtt
import keyboard
import time

client_name = "client1"
client = mqtt.Client(client_name)
# client.connect("10.245.82.149")
client.connect("broker.hivemq.com", 1883)

client.publish("test/message", "running " + client_name)

val = 100

def getVals():
    fr = 0
    br = 0
    bl = 0
    fl = 0
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('t'):
            fr = val
        if keyboard.is_pressed('r'):
            fl = val
        if keyboard.is_pressed('f'):
            bl = val
        if keyboard.is_pressed('g'):
            br = val

    except:
        pass

    return fr, br, bl, fl


frLast = 0
brLast = 0
blLast = 0
flLast = 0

while True:

    time.sleep(.05)
    fr, br, bl, fl = getVals()
    if fr != frLast:
        client.publish("car/fr", fr)
    if br != brLast:
        client.publish("car/br", br)
    if bl != blLast:
        client.publish("car/bl", bl)
    if fl != flLast:
        client.publish("car/fl", fl)
    frLast = fr
    brLast = br
    blLast = bl
    flLast = fl
