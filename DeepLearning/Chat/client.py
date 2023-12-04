import socket
import threading

# 서버 설정
SERVER_IP = '127.0.0.1'  # 서버 IP 주소
SERVER_PORT = 12345        # 서버 포트 번호

# 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버에 연결
client_socket.connect((SERVER_IP, SERVER_PORT))

# 서버로부터 메시지를 받아 처리하는 함수
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            # 서버에서 보낸 메시지를 파싱하여 클라이언트 번호를 추출
            if message.startswith('클라이언트 번호:'):
                client_number = int(message.split(':')[1].strip())
                print(f'당신의 클라이언트 번호는 {client_number}입니다.')
            else:
                print(message)
        except Exception as e:
            print(f'에러 발생: {e}')
            client_socket.close()
            break

# 메시지 수신 및 전송 쓰레드 시작
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# 사용자로부터 메시지를 입력받아 서버로 전송
while True:
    message = input()
    # 사용자가 "exit"를 입력하면 클라이언트 종료
    if message.lower() == 'exit':
        client_socket.send(message.encode('utf-8'))
        client_socket.close()
        break
    # 그 외의 경우에는 메시지를 서버로 전송
    client_socket.send(message.encode('utf-8'))