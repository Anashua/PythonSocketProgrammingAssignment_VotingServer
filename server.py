import socket
import select
import sys


def recieve_msg(client_socket):
    try:
        message_header=client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length=int(message_header.decode("utf-8").strip())
      
        return {"header":message_header,"data":client_socket.recv(message_length).decode("utf-8"),"length":message_length}

    except:
        return False

def voting_server():
    read_sockets,_,exception_sockets=select.select(sockets_list,[],sockets_list)

    for notified_socket in read_sockets:
        if notified_socket== server_socket:
            client_socket,client_address=server_socket.accept()

            user=recieve_msg(client_socket)
            if user is False:
                continue
            sockets_list.append(client_socket)
            clients[client_socket]=user
            voters="The candidates are A , B and C"
            voters=voters.encode("utf-8")
            voters_header=f"{len(voters):<{HEADER_LENGTH}}".encode("utf-8")
            client_socket.send(voters_header+voters)

            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data']}")
            return True
        else:
            message=recieve_msg(notified_socket)
            data=int(message["data"])
            if(data==1):
                    voters_list["A"]+=1
            elif(data==2):
                    voters_list["B"]+=1
            elif(data==3):
                    voters_list["C"]+=1
            #if message is False:
            soc=clients[notified_socket]
            #sockets_list.remove(notified_socket)
            #del clients[notified_socket]
            user=clients[notified_socket]
            print(f"recieved message from {user['data']}:{message['data']}")
            print(f"Closed connection from {soc['data']}")
            notified_socket.close()
            return False


    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]    

if __name__=="__main__":
    
    HEADER_LENGTH=10
    IP=socket.gethostname()
    PORT =1809

    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    server_socket.bind((IP,PORT))
    server_socket.listen()


    sockets_list=[server_socket]
    voters_list={"A":0,"B":0,"C":0}

    #socket will be the key and user data will be the value
    clients={}
    while voting_server():
        continue
    print(f"A GOT {voters_list['A']}\nB GOT {voters_list['B']}\nC GOT {voters_list['C']}")
    
