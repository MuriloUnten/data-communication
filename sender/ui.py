import tkinter as tk
import connection.connection as conn

msg_escrita = None 
msg_criptografada = None 
msg_binario = None 
msg_algoritmo = None 

def on_button_click():
    global msg_criptografada 

    message = msg_text_box.get("1.0",tk.END).strip()
    password = password_text_box.get("1.0", tk.END)
    address = ip_text_box.get("1.0", tk.END)

    msg_criptografada = conn.encrypt_xor_cipher(message, password)
    print(msg_criptografada)
    msg_escrita_label.config(text=msg_criptografada)

    if message:
        conn.send_message(message, password, address)

# Create the main window
root = tk.Tk()
root.title("Simple GUI")

#Create the text boxes
msg_label = tk.Label(root, text="Mensagem")
msg_label.pack(pady=5)

msg_text_box = tk.Text(root, height=10, width=50)
msg_text_box.pack(pady=10)

password_label = tk.Label(root, text="Senha")
password_label.pack(pady=5)

password_text_box = tk.Text(root, height=10, width=50)
password_text_box.pack(pady=10)

ip_label = tk.Label(root, text="Endereço de IP")
ip_label.pack(pady=5)

ip_text_box = tk.Text(root, height=10, width=50)
ip_text_box.pack(pady=10)

# Create the send button
button = tk.Button(root, text="Submit", command=on_button_click)
button.pack(pady=5)

msg_escrita_label = tk.Label(root, text="Mensagem")
msg_escrita_label.pack(pady=5)

# Run the application
root.mainloop()
