from onshape_client.client import Client
import json
base = 'https://cad.onshape.com' # change this if you're using a document in an enterprise (i.e. "https://ptc.onshape.com")


## NEVER SHARE NOTEBOOKS WITH API KEYS
client = Client(configuration={"base_url": base,
                               "access_key": 'UwxVqTCamSWj4ysZR0Mhr8mF',
                               "secret_key": 'pbsrt0Sz3AipOldWDURCE0JqTVQbq63olryiv1MaXqskfY2m'})

def GetSetMates(positions):
    fixed_url = '/api/assemblies/d/did/w/wid/e/eid/matevalues'

    ## CHANGE THE INFORMATION BELOW TO MATCH YOUR ONSHAPE URL
    # my test
    did = '10ed223cd398711ddca751e6'
    wid = 'd65667aedf7fb719ac29cfd0'
    eid = '467c62f9a78873af82febde1'

    # test 2
    # https://rogers.onshape.com/documents/7b2ce3302675d0fe511eac3f/w/da950aaa33c6b77dcef74d3b/e/191688db5f24c58aa91ccc86
    did = '7b2ce3302675d0fe511eac3f'
    wid = 'da950aaa33c6b77dcef74d3b'
    eid = '191688db5f24c58aa91ccc86'
    method = 'GET'

    params = {}
    payload = {}
    headers = {'Accept': 'application/vnd.onshape.v2+json',
               'Content-Type': 'application/vnd.onshape.v2+json'}

    fixed_url = fixed_url.replace('did', did)
    fixed_url = fixed_url.replace('wid', wid)
    fixed_url = fixed_url.replace('eid', eid)

    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers,
                                         body=payload)
    # print(response.data)

    parsed = json.loads(response.data)
    newMates = parsed
    for i in range(len(positions)):
        newMates['mateValues'][i]['rotationZ'] = positions[i]

    # print(newMates)

    method = 'POST'

    params = {}
    payload = newMates
    headers = {'Accept': 'application/vnd.onshape.v2+json',
               'Content-Type': 'application/vnd.onshape.v2+json'}
    response = client.api_client.request(method, url=base + fixed_url, query_params=params, headers=headers,
                                         body=payload)


import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print("==================")
    msg = message.payload.decode("utf-8")
    topic = message.topic
    global speed
    if msg == "testing":
        pass
    elif "br" in topic:
        speeds[0] = int(msg)
    elif "fl" in topic:
        speeds[1] = int(msg)
    elif "fr" in topic:
        speeds[2] = int(msg)
    elif "bl" in topic:
        speeds[3] = int(msg)

    # print("message received =" ,str(msg))
    # print("message topic =",message.topic)
    # # print("message qos=",message.qos)
    # print("message retain flag=",message.retain)

client_name = "digital twin client"
# MQTTclient = mqtt.Client(client_name)
MQTTclient = mqtt.Client(client_name, True, None)
# MQTTclient.connect("10.245.82.149", 1883)
# MQTTclient.connect("broker.hivemq.com", 1883)


MQTTclient.username_pw_set(username="ceeo", password="cee0prek!")
MQTTclient.connect("173.76.110.237")
MQTTclient.on_message=on_message

MQTTclient.publish("test/message", "running " + client_name)

MQTTclient.subscribe("car/#")
MQTTclient.loop_start()

wheels = 4
speeds = [0] * wheels
positions = [0.0] * wheels

while True:
    time.sleep(.1)
    for i in range(len(positions)):
        positions[i]+=speeds[i] / 400
        print(positions[i])
    GetSetMates(positions)

MQTTclient.loop_stop()




# while True:
#     MQTTclient.subscribe("#")
#     MQTTclient.loop(.1)
#     # MQTTclient.loop_start()  # start the loop
#     #
#     # # MQTTclient.publish("car/fl", "OFF")
#     # time.sleep(.1)  # wait/
#     # MQTTclient.loop_stop() #stop the loop

# GetSetMates(0)
