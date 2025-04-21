import paho.mqtt.client as mqtt
import os #파일 접근 시 
import base64 #이미지 파일 인코딩/디코딩

name_topic = 'updates/name'
file_topic = 'updates/file'

username = "admin"
password = "1234"
broker_ip = '192.168.137.166'


temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
os.makedirs(temp_dir, exist_ok=True)

file_name = None
file_data = None

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

def on_message(client, userdata, msg):
    global file_name, file_data
    try:
        payload = msg.payload.decode('utf-8')
        topic = msg.topic

        if topic == name_topic:
            file_name = payload

        elif topic == file_topic:
            file_data = base64.b64decode(payload)
    except Exception as e:
        print("Error : ", e)
    if file_name and file_data:
        file_path = os.path.join(temp_dir, file_name)
        with open(file_path,'wb') as f:
            f.write(file_data)
        print(f"File received and saved as {file_name}")
        file_name =None
        file_data =None

def on_publish(client, userdata, mid):
    print(f"Message {mid} published successfully")

def receive_file_to_broker(broker_ip, username, passsword, port = 1883):
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    client.username_pw_set(username, passsword)

    client.connect(broker_ip, port=port)

    client.subscribe(name_topic)
    client.subscribe(file_topic)

    client.loop_forever()

if __name__ == "__main__":
    receive_file_to_broker(broker_ip, username, password)