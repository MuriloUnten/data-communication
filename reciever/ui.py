import tkinter as tk
import connection.connection as conn
import threading
import time
from queue import Queue

HOST = conn.getIp()
receive_thread = None
receive_thread_running = threading.Event()
passwordQueue = Queue()
messageQueue = Queue()

def on_button_click():
    global receive_thread, passwordQueue, messageQueue
    print("Button clicked")

    password = password_text_box.get("1.0", tk.END).strip()
    passwordQueue.put(password)

    if receive_thread is None or not receive_thread.is_alive():
        receive_thread_running.set()  # Set the event to start the thread
        receive_thread = threading.Thread(target=receive_message, args=(passwordQueue, messageQueue))
        receive_thread.start()
    else:
        print("Receive thread is already running")

def receive_message(passwordQueue, messageQueue):
    try:
        while receive_thread_running.is_set():
            root.after(100, checkForMessageUpdate)  # Schedule the next check
            conn.receive(passwordQueue, messageQueue)
    except Exception as e:
        print(f"Error receiving message: {e}")


def checkForMessageUpdate():
    global messageQueue
    if not messageQueue.empty():
        message = messageQueue.get()
        if message:
            msg_escrita_label.config(text="Mensagem: " + message)
            print("Receiving")
    if receive_thread_running.is_set():
        root.after(100, checkForMessageUpdate)  # Schedule the next check

def stop_receive_thread():
    global receive_thread
    if receive_thread is not None and receive_thread.is_alive():
        receive_thread_running.clear()  # Clear the event to stop the thread
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
