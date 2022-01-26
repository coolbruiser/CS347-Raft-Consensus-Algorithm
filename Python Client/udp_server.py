# python3 tkinter application for communicating with network

from tkinter import *
import tkinter.font as tkFont
import socket
import threading
import math
import time

from multilistbox import MultiListbox

# Sends command when Send pressed

def send_command():
    global index, value
    index_val = index.get()
    value_val = value.get()

    try:
        if (int(index_val) >= 0) & (int(index_val) < 10):
            string = str(int(index_val)) + ' ' + str(int(value_val))
            client_send_socket.sendto(bytes(string, 'utf-8'),
                    (client_ip, client_send_port))
        else:
            print('Error:\tInvalid Input')
    except:
        print('Error:\tInvalid Input')


# Takes incoming packets, splits up and places in correct text box

def handle_packets(client_receive_socket):
    while True:  # Wait for response (updated list)
        (data, addr) = client_receive_socket.recvfrom(1024)  # buffer size is 1024 bytes
        try:
            decoded = data.decode()

            if 'Started' in decoded:
                con.configure(text='Connected', bg='green')
                continue

            if 'Ended' in decoded:
                con.configure(text='Disconnected', bg='red')
                continue

            split_decoded = decoded.split(':')
            text_boxes[int(data.decode()[0])].insert(0, ('-', '-', '-',
                    split_decoded[1], str(round(time.time(), 2))))

            con.configure(text='Connected', bg='green')
        except:
            print('Error:\tDecode Error')

def main():

    # Initialise thread for receiving packets

    receiver = threading.Thread(target=handle_packets,
                                args=(client_receive_socket, ),
                                daemon=True)
    receiver.start()

    # Begin UI loop

    root.mainloop()


if __name__ == '__main__':

    # IP of ESP and port used

    client_ip = '127.0.0.1'
    client_receive_port = 12345
    client_send_port = 12346

    # Define UDP socket and bind to port

    client_receive_socket = socket.socket(socket.AF_INET,
            socket.SOCK_DGRAM)  # UDP
    client_receive_socket.bind((client_ip, client_receive_port))

    client_send_socket = socket.socket(socket.AF_INET,
            socket.SOCK_DGRAM)  # UDP

    # Interface colours

    textCol = '#DDDDFF'
    bgCol = '#190C1C'

    # Tkinter interface construction

    root = Tk()
    root.geometry('1280x720')

    # Root frame

    root_frame = Frame(root, bg=bgCol)
    root_frame.place(relx=.5, rely=.5, anchor='center')

    fontStyle = tkFont.Font(family='Piboto', size=16)
    titleFont = tkFont.Font(family='Piboto', size=32)

    root.configure(background=bgCol)

    root.title('ESP Interface')

    root_title = Label(root_frame,
                       text='Raft Consensus Algorithm Interface',
                       font=titleFont)
    root_title.configure(foreground=textCol, background=bgCol)
    root_title.grid(row=0, column=3)

    con = Button(root_frame, text='Disonnected', bg='red',
                 borderwidth=0, highlightthickness=0)
    con.grid(row=0, column=1)

    # Input frame

    input_frame = Frame(root_frame, bg=bgCol)
    input_frame.grid(row=1, column=1)

    input_title = Label(input_frame, text='Input', font=titleFont)
    input_title.configure(foreground=textCol, background=bgCol)
    input_title.grid(row=0, column=1)

    index_label = Label(input_frame, text='Index', font=fontStyle)
    index_label.configure(foreground=textCol, background=bgCol)
    index_label.grid(row=1, column=1)

    index = Entry(input_frame, borderwidth=0)
    index.grid(row=2, column=1)

    value_label = Label(input_frame, text='Value', font=fontStyle)
    value_label.configure(foreground=textCol, background=bgCol)
    value_label.grid(row=3, column=1)

    value = Entry(input_frame, borderwidth=0)
    value.grid(row=4, column=1)

    button_sep = Frame(input_frame, width=40, height=40,
                       background=bgCol)
    button_sep.grid(row=5, column=1)

    b = Button(input_frame, text='Send', command=send_command,
               borderwidth=0, highlightthickness=0)
    b.grid(row=6, column=1)

    # Border frames

    component_split = Frame(root_frame, width=50, height=40,
                            background=bgCol)
    component_split.grid(row=500, column=2)

    # details frame

    details_frame = Frame(root_frame, bg=bgCol)
    details_frame.grid(row=1, column=3)

    details_split = Frame(details_frame, width=40, height=0,
                          background=bgCol)
    details_split.grid(row=500, column=2)

    text_boxes = []

    for i in range(0, 6):
        label = Label(details_frame, text='Server ' + str(i),
                      font=fontStyle)

        label.configure(foreground=textCol, background=bgCol)
        label.grid(row=3 * math.floor(i / 2), column=3 * (i - 2
                   * math.floor(i / 2)) + 1)

        text_box = MultiListbox(details_frame, (('State', 7), ('Term',
                                7), ('Vote', 7), ('Array', 18),
                                ('Epoch Time', 18)))
        text_box.grid(row=1 + 3 * math.floor(i / 2), column=3 * (i - 2
                      * math.floor(i / 2)) + 1)

        text_boxes.append(text_box)

    main()
