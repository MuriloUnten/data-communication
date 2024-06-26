import tkinter as tk
import connection.connection as conn
import threading
import time

HOST = conn.getIp()
receive_thread = None
receive_thread_running = threading.Event()

def on_button_click():
    global receive_thread
    print("Button clicked")

    password = password_text_box.get("1.0", tk.END).strip()
    if receive_thread is None or not receive_thread.is_alive():
        receive_thread = threading.Thread(target=receive_message, args=(password,))
        receive_thread_running.set()  # Set the event to start the thread
        receive_thread.start()
    else:
        print("Receive thread is already running")
        stop_receive_thread()


def receive_message(password):
    try:
        while receive_thread_running.is_set():
            message = conn.receive(password)
            msg_escrita_label.config(text="Mensagem: " + message)
            receive_thread.start()
            print("Receiving")
            time.sleep(1)
    except Exception as e:
        print(f"Error receiving message: {e}")

def stop_receive_thread():
    global receive_thread
    if receive_thread is not None and receive_thread.is_alive():
        receive_thread_running.clear()
        receive_thread.join()
        print("Receive thread stopped")

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

msg_escrita_label = tk.Label(root, text="Mensagem: ")
msg_escrita_label.pack(pady=5)

# Create the send button
button = tk.Button(root, text="Submit", command=on_button_click)
button.pack(pady=5)

# Run the application
root.mainloop()
