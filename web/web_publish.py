from flask import Flask, request, redirect, render_template, url_for, flash
import os
import crypto
import paho.mqtt.client as mqtt
import base64 #이미지 파일 인코딩/디코딩

app = Flask(__name__)
# 세션관리용 키
app.secret_key = 'secret_key'

# 현재 디렉토리 기준으로 'upload' 폴더 경로 설정 작성
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'upload')
# 폴더가 없는 경우 폴더를 생성해서 프로그램이 돌아갈 수 있도록 함 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

name_topic = 'updates/name'
file_topic = 'updates/file'

#브로커 ip
broker_ip = '192.168.137.166'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def upload_form():
    return render_template('upload.html')# HTML 파일 경로를 Flask 기본 경로에 맞게 설정

@app.route('/upload', methods=['POST'])
#파일 업로드 시 동작 작성
def upload_file():
    if 'file' not in request.files:
        flash('파일을 선택하세요')
        return redirect(url_for('upload_form'))
    file = request.files['file']
    username = request.form['username']
    password = request.form['password']
    with open("temp_pw.txt", "w") as tmppw:
        tmppw.write(password)
        password_hash = crypto.compute_file_hash("temp_pw.txt")
        os.remove("temp_pw.txt")
        print(f'File : {file.filename}, Username : {username}, Password : {password}')

        with open("pwfile.txt", "r") as pwfile:
            lines = pwfile.readlines()
            for line in lines:
                approved_user = line.split(":")[0].strip()
                approved_pw = line.split(":")[1].strip()
                if username == approved_user and password_hash == approved_pw:
                    print(f"승인된된 사용자 {approved_user}")
                    if file.filename == '':
                        flash('파일이 존재하지 않습니다.')
                        return redirect(url_for('upload_form'))
                    if file :
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                        file.save(file_path)
                        send_file_to_broker(file_path, broker_ip, username, password)
                        flash(f"FILE '{file.filename}'이 성공적으로 업로드 되었습니다.")
                        return redirect(url_for('upload_form'))
            flash('승인되지 않은 사용자입니다.')
            return redirect(url_for('upload_form'))


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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) #외부 장치 접근 허용

