import sys
import socket
import select

HOST = ''
SERVER_LIST = []
PORT = 6000
RECV_BUFFER = 4096

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    SERVER_LIST.append(server_socket)

    print 'Starting server connection. Listening to port: ', PORT

    try:
        while True:
            ready_to_read, ready_to_write, in_error = select.select(SERVER_LIST, [], [], 0)

            for sock in ready_to_read:
                # new connection request received
                if sock == server_socket:
                    sockfd, addr = server_socket.accept()
                    SERVER_LIST.append(sockfd)

                    print 'Client: (%s, %s)' % addr

                    broadcast(sockfd, "[%s:%s] entered our chatting room.\n" % addr)

                # already known connection
                else:
                    try:
                        data = sock.recv(RECV_BUFFER)
                        # is there anything in the socket
                        if data:
                            broadcast(sock, "\r" + "[" + str(sock.getpeername()) + "] " + data)
                        else:
                            # the socket is broken remove it
                            if sock in SERVER_LIST:
                                SERVER_LIST.remove(sock)
                            broadcast(sock, "Client (%s, %s) is offline.\n" % addr)
                    except:
                        broadcast(sock, "Client (%s, %s) is offline.\n" % addr)
                        continue

        # always close connection after done using
        server.close()
    except KeyboardInterrupt:
        print "\nBye."


def broadcast(sock, message):
    for socket in SERVER_LIST:
        if sock != socket:
            try:
                sock.send(message)
            except:
                # broken connection
                sock.close()
                # remove it
                if sock in SERVER_LIST:
                    SERVER_LIST.remove(sock)

if __name__ == "__main__":
    sys.exit(server())
