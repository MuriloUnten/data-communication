import tkinter as tk
import connection.connection as conn
import threading
import time
from queue import Queue

HOST = conn.getIp()
receive_thread = None
receive_thread_running = threading.Event()
password = None
passwordQueue = Queue()
messageQueue = Queue()

msg_escrita = None
msg_criptografada = None
msg_binario = None
msg_algoritmo = None
msg_decriptada = None

canvas_width = 720
canvas_height = 80
canvas_height_b8zs = 120


def on_button_click():
    global receive_thread, passwordQueue, messageQueue, password
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
    global passwordQueue
    if not messageQueue.empty():
        message = messageQueue.get()
        if message:
            global msg_escrita
            global msg_criptografada
            global msg_binario
            global msg_algoritmo
            global msg_decriptada
            global password

            if password:
                msg_escrita_label.config(text="Mensagem: " + message)
                print("Receiving")

                msg_algoritmo = message
                plot_graph_b8zs(msg_algoritmo, canvas_msg_algoritmo)

                msg_criptografada = conn.binary_to_string(conn.decode_b8zs(message))
                plot_graph(msg_criptografada, canvas_msg_criptografada)
                msg_decodificada_label.config(text="Mensagem decodificada: " + msg_criptografada)

                msg_decriptada = conn.decrypt_xor_cipher(msg_criptografada, password)
                plot_graph(msg_decriptada, canvas_msg_decriptada)
                msg_decriptada_label.config(text="Mensagem decriptada: " + ascii(msg_decriptada))
    if receive_thread_running.is_set():
        root.after(100, checkForMessageUpdate)  # Schedule the next check


def stop_receive_thread():
    global receive_thread
    if receive_thread is not None and receive_thread.is_alive():
        receive_thread_running.clear()  # Clear the event to stop the thread
        receive_thread.join()
        print("Receive thread stopped")


def plot_graph(message, canva):
    canva.delete("all")
    dot_size = 0
    dot_spacing = 0
    x_pos = axis_padding + dot_spacing

    bit_value = conn.binaryString(message)
    print(bit_value)
    bit_int = []
    print("len(bit_value): ", len(bit_value))
    for i in range(len(bit_value)):
        bit_int.append(int(bit_value[i]))

    dot_size = round((canvas_width - 20) / (len(bit_int) * 2), 2)
    if dot_size > 10:
        dot_size = 10

    dot_spacing = round((canvas_width - 20) / (len(bit_int)), 2)

    print(dot_size, dot_spacing)
    for bit in bit_int:
        y_pos = canva.winfo_height() - axis_padding
        y_pos -= (canva.winfo_height() - axis_padding) / 2 * bit  # Adjust offset based on each bit value

        canva.create_oval(x_pos - dot_size, y_pos - dot_size,
                          x_pos + dot_size, y_pos + dot_size,
                          fill="black")
        x_pos += dot_spacing


def plot_graph_b8zs(inputStr, canva):
    canva.delete("all")
    dot_size = 0
    dot_spacing = 0
    x_pos = axis_padding + dot_spacing

    dot_size = round((canvas_width - 20) / (len(inputStr) * 2), 2)
    if dot_size > 10:
        dot_size = 10

    dot_spacing = round((canvas_width - 20) / (len(inputStr)), 2)

    for char in inputStr:
        position = None
        if char == "+":
            position = 2
        elif char == "0":
            position = 1
        else:
            position = 0

        y_pos = canva.winfo_height() - axis_padding
        y_pos -= (canva.winfo_height() - axis_padding) / 3 * position

        canva.create_oval(x_pos - dot_size, y_pos - dot_size,
                          x_pos + dot_size, y_pos + dot_size,
                          fill="black")
        x_pos += dot_spacing


def draw_x_axis(canvas, canvas_width, y_pos):
    canvas.create_line((0, y_pos, canvas_width, y_pos), fill="black")
    canvas.create_text(canvas_width - 10, y_pos + 5, text="X", fill="black", anchor="se")


def draw_y_axis(canvas, canvas_height, x_pos):
    canvas.create_line((x_pos, 0, x_pos, canvas_height), fill="black")
    canvas.create_text(x_pos - 5, 10, text="Y", fill="black", anchor="nw")


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

msg_codificada_label = tk.Label(root, text="Mensagem codificada: ")
msg_codificada_label.pack(pady=5)

canvas_msg_algoritmo = tk.Canvas(root, width=canvas_width, height=canvas_height_b8zs, bg="white")
canvas_msg_algoritmo .pack()
axis_padding = 20
draw_x_axis(canvas_msg_algoritmo, canvas_width, canvas_msg_algoritmo.winfo_height() - axis_padding)
draw_y_axis(canvas_msg_algoritmo, canvas_height_b8zs, axis_padding)

msg_decodificada_label = tk.Label(root, text="Mensagem decodificada: ")
msg_decodificada_label.pack(pady=5)

canvas_msg_criptografada = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas_msg_criptografada.pack()
axis_padding = 20
draw_x_axis(canvas_msg_criptografada, canvas_width, canvas_msg_criptografada.winfo_height() - axis_padding)
draw_y_axis(canvas_msg_criptografada, canvas_height, axis_padding)

msg_decriptada_label = tk.Label(root, text="Mensagem decriptada: ")
msg_decriptada_label.pack(pady=5)

canvas_msg_decriptada = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas_msg_decriptada.pack()
axis_padding = 20
draw_x_axis(canvas_msg_decriptada, canvas_width, canvas_msg_decriptada.winfo_height() - axis_padding)
draw_y_axis(canvas_msg_decriptada, canvas_height, axis_padding)

# Run the application
root.mainloop()
