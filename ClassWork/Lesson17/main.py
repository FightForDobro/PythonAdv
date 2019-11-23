import socket
from threading import Thread

server_address = ('127.0.0.1', 8091)

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind(server_address)

soc.listen(5)


def client_handler(client_socket, client_address):
    while True:
        print('Something')
        data = client_socket.recv(1024)
        client_socket.send(data[::-1])

        if not data:
            print('DROPPED')
            break


while True:

    client, address = soc.accept()
    print(f'Client {address}')

    Thread(target=client_handler, args=(client, address),
           name=address).start()
