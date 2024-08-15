import threading
import tkinter
from tkinter import *
from PIL import Image, ImageTk
import os
import socket

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

path = "Image_from_client.jpg"
host = "10.100.102.3"  # as both code is running on same pc
port = 12345  # socket server port number

server_socket = socket.socket()  # instantiate

server_socket.bind((host, port))

server_socket.listen()

print("listening...")

class ChatApplication:

    def __init__(self, user):
        self.window = Tk()
        self.user = user
        self._setup_main_window()
        self.flag_activate_button = False
        self.flag_dectivate_button = False

    def run(self):
        self.window.mainloop()


    def close(self):
        self.window.destroy()

    def _setup_main_window(self):
        self.window.title("MY_GUI")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)

        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text=f'Welcome {self.user}', font=FONT_BOLD, pady=10)

        head_label.place(width=465, height=50)

        # tiny divider
        line1 = Label(self.window, width=450, bg=BG_GRAY)
        line1.place(relwidth=1, rely=0.07, relheight=0.012)
        line2 = Label(self.window, width=450, bg=BG_GRAY)
        line2.place(relwidth=4, rely=0.139, relheight=0.012)

        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.68, relwidth=1, rely=0.15)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        self.text_widget.configure(state=NORMAL)
        self.text_widget.configure(state=DISABLED)
        self.text_widget.see(END)

        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        #Text
        text = Text(bottom_label, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,font=FONT, padx=5, pady=5)
        text.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        text.configure(cursor="arrow", state=DISABLED)

        text.configure(state=NORMAL)
        text.configure(state=DISABLED)
        text.see(END)

        text.configure(state=NORMAL)
        text.insert(END, 'If you want to activate the alarm click on')
        text.insert(END, '\n')
        text.insert(END , 'Activate if not click on Deactivate:')
        text.configure(state=DISABLED)
        text.see(END)

        # Activate button
        activate_button = Button(bottom_label, text="Activate", font=FONT_BOLD, width=20, bg=BG_GRAY, command=self.Activate_button_pressed)
        activate_button.place(relx=0.77, rely=0.008, relheight=0.025, relwidth=0.22)

        # Deactivate button
        deactivate_button = Button(bottom_label, width=20, bg=BG_GRAY,text="Deactivate",font=FONT_BOLD, command=self.Deactivate_button_pressed)
        deactivate_button.place(relx=0.77, rely=0.047, relheight=0.025, relwidth=0.22)

    def Activate_button_pressed(self):
        if os.path.exists(path):
            self.flag_activate_button = True
            os.remove(path)

    def Deactivate_button_pressed(self):
        if os.path.exists(path):
            self.flag_dectivate_button = True
            os.remove(path)

def Server():
    while True:
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        message_from_client = conn.recv(2048).decode()
        if message_from_client == "!image":
            print(message_from_client)
            Get_image(conn)
        elif message_from_client[:8] == "!message":
            print(message_from_client[:8])
            msg = message_from_client[8:]
            print(msg)
            app_login.text_widget.configure(state=NORMAL)
            app_login.text_widget.insert(END, "A foreign vehicle has been detected in your private")
            app_login.text_widget.insert(END, '\n')
            app_login.text_widget.insert(END, "parking lot with its number " + msg)
            app_login.text_widget.insert(END, '\n')
            app_login.text_widget.configure(state=DISABLED)
            app_login.text_widget.see(END)
            while ((app_login.flag_dectivate_button == False) and (app_login.flag_activate_button == False)):
                continue
            if app_login.flag_activate_button == True:
                message_to_client = "activate"
                conn.send(message_to_client.encode())
            if app_login.flag_dectivate_button == True:
                message_to_client = "deactivate"
                conn.send(message_to_client.encode())
            app_login.flag_activate_button = False
            app_login.flag_dectivate_button = False
        conn.close()

def Get_image(connection):
    file = open(path, "wb")
    image_chunk = connection.recv(2048)
    while image_chunk:
        file.write(image_chunk)
        image_chunk = connection.recv(2048)
    file.close()


# step 5 - start reviving msg from client in different thread!!
t1 = threading.Thread(target=Server)
t1.start()
app_login = ChatApplication("Server")
app_login.run()