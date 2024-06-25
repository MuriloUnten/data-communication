import tkinter as tk

def on_button_click():
    print("Button clicked")

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

ip_label = tk.Label(root, text="Endereço de IP")
ip_label.pack(pady=5)

ip_text_box = tk.Text(root, height=10, width=50)
ip_text_box.pack(pady=10)

msg_escrita_label = tk.Label(root, text="Mensagem")
msg_escrita_label.pack(pady=5)

# Create the send button
button = tk.Button(root, text="Submit", command=on_button_click)
button.pack(pady=5)

msg_escrita_label = tk.Label(root, text="Mensagem")
msg_escrita_label.pack(pady=5)

# Run the application
root.mainloop()