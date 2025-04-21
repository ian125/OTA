import paho.mqtt.client as mqtt
import os

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connect to broker with result code" + str(rc))
    else:
        print(f"Connection failed with code {rc}")

def on_disconnect(client, userdata, rc):
    print("Dissconnected from broker, code :", rc)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print(f"Message recieved on topic {msg.topic} : {payload}")
    except:
        print(f"Error decoding message : {e}")

def receive_message_to_broker(broker_ip, username, passsword, topic, port = 1883):
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    client.username_pw_set(username, passsword)

    client.connect(broker_ip, port=port)

    client.subscribe(topic)
    print(f"Subscribe to topic : {topic}")

    client.loop_forever()

if __name__ == "__main__":
    topic = "mos"
    broker_ip = '192.168.137.166'
    username = input("Enter username : ")
    passsword = input("Enter password : ")
    receive_message_to_broker(broker_ip, username, passsword, topic)