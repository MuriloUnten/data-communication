import socket

HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as reciever_socket:
    reciever_socket.bind((HOST, PORT))
    
    reciever_socket.listen()
    print(f"Listening on {HOST}:{PORT}...")

    client_socket, client_address = reciever_socket.accept()
    print(f"Accepted connection from {client_address}")

    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Received message: {data.decode()}")

    client_socket.close()