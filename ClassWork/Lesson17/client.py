import socket
# from PythonAdv.PythonAdv.ClassWork.Lesson17.exeptions import CostumeStringLengthException

server_address = ('127.0.0.1', 8091)

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soc.connect(server_address)


while True:

    data_to_send = input().encode('utf-8')

    if len(data_to_send) < 1:
        continue

    if data_to_send == b'exit()':
        soc.close()
        break

    soc.send(data_to_send)

    data = soc.recv(1024)

    print(data)
