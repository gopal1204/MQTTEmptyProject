from django.http import HttpResponse
from django.shortcuts import render
from django.template import Template, Context
import datetime
from matplotlib import pyplot as plt
import random
from paho.mqtt import client as mqtt_client
import paho.mqtt.client as mqtt

import time

# python3.6
data = ''

broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx123'
password = 'public123'
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
            global data
            data = msg.payload.decode('utf8')
            # userdata = msg.payload.decode('utf8')
            # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            print(data)

    client.subscribe(topic)
    client.on_message = on_message
    return data

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()



def output(request):

    now = datetime.datetime.now()
    person = "MQTT Results" + data
    context = {
        'person': person,
        'current_date': now.date(),
    }
    return render(request, 'mytemp.html', context)


if __name__ == '__main__':
    run()
    output()
