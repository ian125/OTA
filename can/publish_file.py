import paho.mqtt.client as mqtt
import os #파일 접근 시 
import base64 #이미지 파일 인코딩/디코딩

name_topic = 'updates/name'
file_topic = 'updates/file'
broker_ip = '192.168.137.166'

def make_message(file_path):
    try:
        with open(file_path, 'rb') as file:
            message = base64.b64encode(file.read())
        return message
    except FileNotFoundError as e:
        print("Error : ",e)
        raise
    

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connect to broker with result code" + str(rc))
    else:
        print(f"Connection failed with code {rc}")

def on_disconnect(client, userdata, rc):
    print("Dissconnected from broker, code :", rc)

def on_publish(client, userdata, mid):
    print(f"Message {mid} published successfully")


def send_file_to_broker(file_path, broker_ip, username, passsword, port = 1883):
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish

    client.username_pw_set(username, passsword)

    client.connect(broker_ip, port=port)

    message = make_message(file_path)
    file_name = os.path.basename(file_path)

    print(file_name)

    client.loop_start()

    client.publish(name_topic, file_name, qos=2)
    client.publish(file_topic, message, qos=2)
    #qos = 0 : 파일 손상 여부 상관 없이 1번만 전송
    #qos = 1 : 파일 반복 전송
    #qos = 2 : ACK 활용 정확하게 한번만 전송송 
    client.loop_stop()

    print(f"success sending file(updates/name) : {file_name}")
    client.disconnect()

if __name__ == "__main__":
    topic = "mos"
    broker_ip = '192.168.137.166'
    username = input("Enter username : ")
    passsword = input("Enter password : ")
    file_path = input("Enter file path to publish : ")
    send_file_to_broker(file_path, broker_ip, username, passsword)