import os
import socket

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen()
    while True:
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
        message_from_client = conn.recv(2048).decode()
        if message_from_client == "!image":
            print(message_from_client)
            Get_image(conn)
        elif message_from_client[0:8] == "!message":
            print(message_from_client[8:])
            message_to_client = input("To activate the alarm type !activate to deatcivate type !deactivate: ")
            while message_to_client != "!activate" and message_to_client != "!deactivate":
                message_to_client = input("To activate the alarm type !activate to deatcivate type !deactivate: ")
            conn.send(message_to_client.encode())
        conn.close()  # close the connection


def Get_image(connection):
    file = open('server_image.jpg', "wb")
    image_chunk = connection.recv(2048)
    while image_chunk:
        file.write(image_chunk)
        image_chunk = connection.recv(2048)
    file.close()

if __name__ == '_main_':
    server_program()