import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            print("[CLIENTE] Conexão fechada pelo servidor")
            client_socket.close()
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))
    
    print("[CLIENTE] Conectado ao servidor")

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input()
        if message.lower() == 'sair':
            client_socket.close()
            print("[CLIENTE] Desconectado do servidor")
            break
        client_socket.send(message.encode('utf-8'))

if __name__ == "__main__":
    start_client()
