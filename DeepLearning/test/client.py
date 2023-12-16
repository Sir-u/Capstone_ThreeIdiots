import socket
import threading

import sys
sys.path.append("../Capstone_ThreeIdiots/DeepLearning/test/")
import talkBot

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))
client_messages = []  # Client-side message storage
queryFlag = False


def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith('클라이언트 번호:'):
                client_number = int(message.split(':')[1].strip())
                print(f'당신의 클라이언트 번호는 {client_number}입니다.')
            else:
                print(f'상대방 >> {message}')
                talkBot.messageDict.append(message)  # Store received message
        except Exception as e:
            print(f'에러 발생: {e}')
            client_socket.close()
            break

def send_messages():
    while True:
        message = input()
        if message.lower() == 'exit':
            client_socket.send(message.encode('utf-8'))
            client_socket.close()
        else:
            client_socket.send(message.encode('utf-8'))
            talkBot.messageDict.append(message)

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()
send_thread = threading.Thread(target=send_messages)
send_thread.start()
talkBot.runGUI()
        