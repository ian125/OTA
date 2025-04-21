import paho.mqtt.client as mqtt
import os
def on_connect(client,userdata,flags,rc):
    if rc == 0:
        print("connected to broker")
    else:
        print(f"Connection failed with code {rc}")

def on_disconnect(client,userdata,rc):
    print(f"Disconnected with code {rc}")

def on_message(client,userdata,msg):
    try:
        payload = msg.payload.decode()
        print(f"Message received on topic {msg.topic}: {payload}")
    except Exception as e:
        print(f"Error decoding message: {e}")

def receive_message_to_broker(broker_ip, username, password, topic, port = 1883):
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    
    client.username_pw_set(username, password)

    client.connect(broker_ip, port = port)

    client.subscribe(topic)
    print(f"Subscribed to topic: {topic}")

    client.loop_forever()

if __name__ == "__main__":
    broker_ip = '192.168.194.1'
    topic = 'message'
    username = input("Enter username: ")
    password = input("Enter password: ")
    receive_message_to_broker(broker_ip, username, password, topic)