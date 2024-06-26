import tkinter as tk
import connection.connection as conn

msg_escrita = None
msg_criptografada = None
msg_binario = None
msg_algoritmo = None

canvas_width = 720
canvas_height = 80
canvas_height_b8zs = 120

def on_button_click():
    global msg_criptografada
    global msg_escrita
    global canvas_msg_criptografada
    global canvas_msg_escrita

    message = msg_text_box.get("1.0", tk.END).strip()
    password = password_text_box.get("1.0", tk.END).strip()
    address = ip_text_box.get("1.0", tk.END).strip()

    msg_criptografada = conn.encrypt_xor_cipher(message, password)
    msg_algoritmo = conn.encode_b8zs(msg_criptografada)
    print(msg_criptografada)
    msg_escrita_label.config(text=ascii(msg_criptografada))

    if message:
        print(message, password, address)
        conn.send_message(message, password, address)

    msg_escrita = message
    #plot graphs
    plot_graph(message, canvas_msg_escrita)
    plot_graph(msg_criptografada, canvas_msg_criptografada)
    plot_graph_b8zs(msg_algoritmo, canvas_msg_algoritmo)


def plot_graph(message, canva):
    canva.delete("all")
    dot_size = 0
    dot_spacing = 0
    x_pos = axis_padding + dot_spacing

    bit_value = conn.binaryString(message)
    print(bit_value)
    bit_int = []
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

# def binaryString(message):
#     binaryStr = ""
#     for character in message:
#         charAsInt = ord(character)
#         binaryChar = "{0:b}".format(charAsInt)
#         while len(binaryChar) < 8:
#             binaryChar = '0' + binaryChar
#         binaryStr += binaryChar

#     return binaryStr

# Create the main window
root = tk.Tk()
root.title("B8ZS - Comunicação de Dados")

#Create the text boxes
msg_label = tk.Label(root, text="Mensagem")
msg_label.pack(pady=5)

msg_text_box = tk.Text(root, height=10, width = canvas_width)
msg_text_box.pack(pady=10)

# gráfico da mensagem escrita
canvas_msg_escrita = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas_msg_escrita.pack()
axis_padding = 20
draw_x_axis(canvas_msg_escrita, canvas_width, canvas_msg_escrita.winfo_height() - axis_padding)
draw_y_axis(canvas_msg_escrita, canvas_height, axis_padding)

password_label = tk.Label(root, text="Senha")
password_label.pack(pady=5)

password_text_box = tk.Text(root, height=10, width = canvas_width)
password_text_box.pack(pady=10)

# gráfico da mensagem criptografada
canvas_msg_criptografada = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas_msg_criptografada.pack()
axis_padding = 20
draw_x_axis(canvas_msg_criptografada, canvas_width, canvas_msg_criptografada.winfo_height() - axis_padding)
draw_y_axis(canvas_msg_criptografada, canvas_height, axis_padding)

ip_label = tk.Label(root, text="Endereço de IP")
ip_label.pack(pady=5)

ip_text_box = tk.Text(root, height=10, width = canvas_width)
ip_text_box.pack(pady=10)

# Create the send button
button = tk.Button(root, text="Submit", command=on_button_click)
button.pack(pady=5)

msg_escrita_label = tk.Label(root, text="Mensagem")
msg_escrita_label.pack(pady=5)

# gráfico da mensagem criptografada
canvas_msg_algoritmo = tk.Canvas(root, width=canvas_width, height=canvas_height_b8zs, bg="white")
canvas_msg_algoritmo .pack()
axis_padding = 20
draw_x_axis(canvas_msg_algoritmo, canvas_width, canvas_msg_algoritmo.winfo_height() - axis_padding)
draw_y_axis(canvas_msg_algoritmo, canvas_height_b8zs, axis_padding)

# Run the application
root.mainloop()
