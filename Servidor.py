import socket
import threading

clients = []

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)
                client.close()

def handle_client(client_socket, client_address):
    print(f"[SERVIDOR] Conexão recebida de {client_address}")
    clients.append(client_socket)
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"[CLIENTE {client_address}] {message}")
            broadcast(f"[CLIENTE {client_address}] {message}", client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

    print(f"[SERVIDOR] Conexão fechada de {client_address}")
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("[SERVIDOR] Servidor iniciado e aguardando conexões...")

    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    start_server()
