import paho.mqtt.client as mqtt
import json
import os

status = 'login'

def change_status(new_status):
    global status
    status = new_status

def on_connect(client, userdata, flags, rc):
    pass

def on_disconnect(client, userdata, rc):
    pass

def on_publish(client, userdata, mid):
    print("Message published with mid: " + str(mid))

def main():
    global status
    broker_ip = '192.168.194.1'
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    change_status('login')

    # Load user data from pwfile.json
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'pwfile.json'), 'r') as f:
        user_data = json.load(f)

    # Load topic data from topic_tier_list.json
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'topic_tier_list.json'), 'r') as f:
        topic_data = json.load(f)

    while status == 'login':
        username = input("Enter username: ")
        password = input("Enter password: ")

        # Validate username and password
        if username in user_data and user_data[username]["pw"] == password:
            user_tier = user_data[username]["Tier"]
            print(f"Login successful. Your Tier: {user_tier}")
        else:
            print("Invalid username or password.")
            continue

        client.username_pw_set(username, password)
        client.connect(broker_ip, port=1883)
        client.loop_start()

        change_status('topic')

        while status == 'topic':
            tier_key = f"Tier-{user_tier}"
            if tier_key in topic_data:
                print("Available topics:")
                for idx, topic in enumerate(topic_data[tier_key]["topics"], start=1):
                    print(f"{idx}: {topic}")
            else:
                print(f"No topics available for Tier-{user_tier}.")
                continue

            topic_idx = input("Enter topic number: ")

            # Validate topic selection
            try:
                topic_idx = int(topic_idx) - 1
                if 0 <= topic_idx < len(topic_data[tier_key]["topics"]):
                    topic = topic_data[tier_key]["topics"][topic_idx]
                    change_status('message')
                else:
                    print("Invalid topic number.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            while status == 'message':
                message = input(f"Enter message to publish {topic}: ")
                client.publish(topic, message)
                client.loop_stop()



if __name__ == "__main__":
    main()