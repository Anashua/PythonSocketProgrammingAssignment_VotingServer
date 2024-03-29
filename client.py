import socket
import select
import errno
import sys

HEADER_LENGTH=10
IP=socket.gethostname()
PORT =1809

my_username=input("Username: ")

client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((IP,PORT))
client_socket.setblocking(False)

username=my_username.encode("utf-8")
username_header=f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header+username)


# intro_header=client_socket.recv(HEADER_LENGTH)
# intro_length=int(intro_header.decode("utf-8").strip())
# intro=client_socket.recv(intro_length).decode("utf-8")
# print(intro)

while True:
    message=input(f"{my_username} > ")
    if message:
        message=message.encode("utf-8")
        message_header=f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header+message)
    
    try:
        while True:
            username_header=client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print("Connection Closed by the server");
                sys.exit()

            username_length=int(username_header.decode("utf-8").strip())
            username=client_socket.recv(username_length).decode("utf-8")

            message_header=client_socket.recv(HEADER_LENGTH)
            message_length=int(message_header.decode("utf-8").strip())
            message=client_socket.recv(message_length).decode("utf-8")

            print(f"{username} > {message}")
            print("THANKYOU FOR YOUR VOTE:")
            sys.exit()

    except IOError as e:
        if e.errno !=errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("THANKYOU FOR YOUR VOTE:")
            sys.exit()
        continue
    except Exception as e:
        print("General Error: ",str(e))
        sys.exit()        
