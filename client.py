import socket

def send_Image():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    message_to_server = "!image"
    client_socket.send(message_to_server.encode())

    file = open("Images\\2.jpg", 'rb')

    image_data = file.read(2048)
    while image_data:
        client_socket.send(image_data)
        image_data = file.read(2048)
    file.close()
    client_socket.close()

def dialogue(num):
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    message_to_server1 = "!message" + num
    client_socket.send(message_to_server1.encode())

    message_from_server = client_socket.recv(2048).decode()
    print(message_from_server)

    client_socket.close()

if __name__ == '__main__':
    send_Image()
    dialogue("4762911")
    send_Image()
    dialogue("4762911")