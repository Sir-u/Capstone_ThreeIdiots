import socket
import threading

import sys
sys.path.append("../Capstone_ThreeIdiots/DeepLearning/")
from config.DatabaseConfig import *
from Database import Database
from datetime import datetime

# 서버 설정
HOST = '127.0.0.1'  # 서버 IP 주소
PORT = 12345         # 포트 번호

# 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 소켓을 주소와 바인딩
server_socket.bind((HOST, PORT))

# 클라이언트 연결 대기
server_socket.listen()

# 연결된 클라이언트들을 저장할 리스트
clients = []
client_count = 0  # 연결된 클라이언트 수를 저장할 변수

db = Database(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME, charset='utf8'
    )

date = datetime.today().strftime("%Y/%m/%d %H:%M")

# 클라이언트와 통신하는 함수
def handle_client(client_socket, addr, client_number):
    print(f'클라이언트 {client_number}로부터의 연결: {addr}')

    # 클라이언트에게 클라이언트 번호 전송
    #client_socket.send(f'당신은 클라이언트 {client_number}입니다.'.encode('utf-8'))

    # 클라이언트가 연결을 끊을 때까지 메시지 수신 및 전송
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            print(f'클라이언트 {client_number}의 연결이 종료되었습니다.')
            clients.remove(client_socket)
            client_socket.close()
            #-------------------------------------------------------------------------------------------------
            # DB 닫기
            db.close() # 디비 연결 끊음
            #-------------------------------------------------------------------------------------------------

            break
        print(f'클라이언트 {client_number} >> {message}')
        #-------------------------------------------------------------------------------------------------
        # DB 데이터 삽입             
        db.insert_message(message, date)
        #-------------------------------------------------------------------------------------------------

        # 연결된 모든 클라이언트에게 메시지 전송
        for client in clients:
            if client != client_socket:
                client.send(message.encode('utf-8'))

# 클라이언트 연결을 수락하고 핸들링하는 함수
def accept_clients():
    global client_count
    while True:
        client_socket, addr = server_socket.accept()
        client_count += 1
        clients.append(client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr, client_count))
        client_handler.start()

# 클라이언트 연결 수락 쓰레드 시작
print('채팅 서버 시작')
accept_thread = threading.Thread(target=accept_clients)
accept_thread.start()
#-------------------------------------------------------------------------------------------------
# DB 열기
db.connect()    # 디비 연결
print('DB 연결 됨')
#-------------------------------------------------------------------------------------------------
