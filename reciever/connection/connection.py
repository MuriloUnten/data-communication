import socket
from queue import Queue

HOSTNAME = socket.gethostname()
# HOST = socket.gethostbyname(HOSTNAME)
HOST = socket.gethostbyname(HOSTNAME)
PORT = 8080

def receive(passwordQueue, messageQueue):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as reciever_socket:
        reciever_socket.bind((HOST, PORT))

        password = passwordQueue.get()

        reciever_socket.listen()
        print(f"Listening on {HOST}:{PORT}...")

        while True:
            while True:
                client_socket, client_address = reciever_socket.accept()
                print(f"Accepted connection from {client_address}")
                data = client_socket.recv(1024)

                if not data:
                    break

                if not passwordQueue.empty():
                    password = passwordQueue.get()

                dataStr = decrypt_xor_cipher(binary_to_string(decode_b8zs(data.decode('latin1'))), password)
                messageQueue.put(dataStr)

                client_socket.close()
                print(f"Received message: {dataStr}")
                messageQueue.put(dataStr)


def decrypt_xor_cipher(message, key):
    message_bytes = bytearray(message, 'utf-8')
    key_bytes = bytearray(key, 'utf-8')

    encrypted_bytes = bytearray(len(message_bytes))

    for i in range(len(message_bytes)):
        encrypted_bytes[i] = message_bytes[i] ^ key_bytes[i % len(key_bytes)]

    encrypted_message = encrypted_bytes.decode('utf-8', errors='ignore')
    # print(ascii(encrypted_message))
    # print(encrypted_message)
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


def binary_to_string(binary_string):
    result = ""
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i + 8]
        decimal_value = int(byte, 2)
        character = chr(decimal_value)
        result += character
    return result

def getIp():
    return HOST

# string = input("encoded text: ")
# key = str(input("key: "))
# print(decrypt_xor_cipher(binary_to_string(decode_b8zs(string)), key))
# recieve()
