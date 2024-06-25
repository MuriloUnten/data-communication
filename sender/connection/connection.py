import socket

def send_message(message, key, reciever_addr):
    encrypted_message = encrypt_xor_cipher(message, key)
    serialized_message = serialize_b8zs(encrypted_message)

    reciever_address = (reciever_addr, 8080)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(reciever_address)
        client_socket.sendall(message.encode())
    except:
        print("Error sending message!")
    finally:  
        client_socket.close()


def encrypt_xor_cipher(message, key):
    message_bytes = bytearray(message, 'utf-8')
    key_bytes = bytearray(key, 'utf-8')

    encrypted_bytes = bytearray(len(message_bytes))
    
    for i in range(len(message_bytes)): 
        encrypted_bytes[i] = message_bytes[i] ^ key_bytes[i % len(key_bytes)]
    
    encrypted_message = encrypted_bytes.decode('utf-8', errors='ignore')
    return encrypted_message


def serialize_b8zs(message):
    pass
