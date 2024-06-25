import tkinter as tk
import socket

def on_button_click():
    user_input = text_box.get("1.0", tk.END).strip()
    if user_input:
        response = send_to_server(user_input)
        print(f"Response from server: {response}")

def send_to_server(message):
    server_address = ('localhost', 8080)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(server_address)
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024).decode()
    finally:  
        client_socket.close()
    return response

# Create the main window
root = tk.Tk()
root.title("Simple GUI")

# Create a text box
text_box = tk.Text(root, height=10, width=50)
text_box.pack(pady=10)

# Create a button
button = tk.Button(root, text="Submit", command=on_button_click)
button.pack(pady=5)

# Run the application
root.mainloop()
