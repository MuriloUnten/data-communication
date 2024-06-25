import socket

HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)
PORT = 8080

def recieve():
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


def decrypt_xor_cipher(message, key):
    message_bytes = bytearray(message, 'utf-8')
    key_bytes = bytearray(key, 'utf-8')

    encrypted_bytes = bytearray(len(message_bytes))

    for i in range(len(message_bytes)):
        encrypted_bytes[i] = message_bytes[i] ^ key_bytes[i % len(key_bytes)]

    encrypted_message = encrypted_bytes.decode('utf-8', errors='ignore')
    print(ascii(encrypted_message))
    print(encrypted_message)
    return encrypted_message


def decode_b8zs(encodedStr):
    decodedStr = []
    strLen = len(encodedStr)
    last1bit = "-"

    encodedIter = iter(encodedStr)
    for c in encodedIter:
        if c == "0":
            decodedStr.append("0")
        else:
            if c == last1bit:
                decodedStr.append("0")
                for i in range(4):
                    decodedStr.append("0")
                    next(encodedIter)
            else:
                decodedStr.append("1")
                last1bit = c

    return "".join(decodedStr)

# string = input("encoded text: ")
# print(decode_b8zs(string))
