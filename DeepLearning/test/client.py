import socket
import threading
import subprocess

process = subprocess.Popen(["python", "../Capstone_ThreeIdiots/DeepLearning/test/talkBot.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text = True, encoding='utf-8')

SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))
client_messages = []  # Client-side message storage


def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith('클라이언트 번호:'):
                client_number = int(message.split(':')[1].strip())
                print(f'당신의 클라이언트 번호는 {client_number}입니다.')
            else:
                print(f'상대방 >> {message}')
                client_messages.append(message)  # Store received message
        except Exception as e:
            print(f'에러 발생: {e}')
            client_socket.close()
            break

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()


while True:
    output = process.stdout.readline().strip()
    if output == '1':
        print("자식 프로세스에서 '1'을 받았습니다.")
    message = input()
    if message.lower() == 'exit':
        client_socket.send(message.encode('utf-8'))
        client_socket.close()
        process.stdin.close()
        process.terminate()
        for msg in client_messages:
            print(msg)
        break
    else:
        client_socket.send(message.encode('utf-8'))
        client_messages.append(message)
        