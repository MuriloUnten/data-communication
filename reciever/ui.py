import tkinter as tk
import connection.connection as conn

HOST = conn.getIp()

def on_button_click():
    print("Button clicked")
    password = password_text_box.get("1.0", tk.END).strip()
    conn.recieve(password)
    print("Recieving")

# Create the main window
root = tk.Tk()
root.title("Simple GUI")

#Create the text boxes
msg_label = tk.Label(root, text="Mensagem: ")
msg_label.pack(pady=5)

password_label = tk.Label(root, text="Senha")
password_label.pack(pady=5)

password_text_box = tk.Text(root, height=10, width=50)
password_text_box.pack(pady=10)

ip_label = tk.Label(root, text="Endereço de IP: " + HOST)
ip_label.pack(pady=5)

msg_escrita_label = tk.Label(root, text="Mensagem")
msg_escrita_label.pack(pady=5)

# Create the send button
button = tk.Button(root, text="Submit", command=on_button_click)
button.pack(pady=5)

# Run the application
root.mainloop()
