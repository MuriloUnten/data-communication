import socket

def send_message(message, key, reciever_addr):
    encrypted_message = encrypt_xor_cipher(message, key)
    serialized_message = encode_b8zs(encrypted_message)

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

    encrypted_message = encrypted_bytes.decode('latin1', errors='ignore')
    print("encrypted:")
    print(ascii(encrypted_message))
    print(encrypted_message)
    return encrypted_message


def encode_b8zs(message):
    binStr = binaryString(message)
    binLength = len(binStr)
    print(binStr)

    output = []
    last1bit = "-"
    zeroCount = 0

    if binStr[0] == "1":
        last1bit = "+"
        output.append(last1bit)
    else:
        output.append("0")
        zeroCount += 1

    for i in range(1, binLength):
        if binStr[i] == "1":
            last1bit = "+" if last1bit == "-" else "-"
            output.append(last1bit)
            zeroCount = 0
        else:
            output.append("0")
            zeroCount += 1
            if zeroCount == 8:
                output[i] = last1bit
                output[i - 4] = last1bit
                tmp = "+" if last1bit == "-" else "-"
                output[i - 1] = tmp
                output[i - 3] = tmp
                zeroCount = 0

    return "".join(output)


def binaryString(message):
    binaryStr = ""
    for character in message:
        charAsInt = ord(character)
        binaryChar = "{0:b}".format(charAsInt)
        while len(binaryChar) < 8:
            binaryChar = '0' + binaryChar
        binaryStr += binaryChar

    return binaryStr


string = "teste"
print(encode_b8zs(string))
