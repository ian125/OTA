import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connect to broker with result code" + str(rc))
    else:
        print(f"Connection failed with code {rc}")

def on_disconnect(client, userdata, rc):
    print("Dissconnected from broker, code :", rc)

def on_publish(client, userdata, mid):
    print(f"Message {mid} published successfully")


def send_message_to_broker(message, broker_ip, username, passsword, port = 1883):
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish

    client.username_pw_set(username, passsword)

    client.connect(broker_ip, port=port)

    client.loop_start()

    client.publish(topic, message)
    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    topic = "mos"
    broker_ip = '192.168.137.166'
    username = input("Enter username : ")
    passsword = input("Enter password : ")
    message = input("Enter message to publish : ")
    send_message_to_broker(message, broker_ip, username, passsword)