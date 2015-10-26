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

                    broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room.\n" % addr)

                # already known connection
                else:
                    try:
                        data = sock.recv(RECV_BUFFER)
                        # is there anything in the socket
                        if data:
                            broadcast(server_socket, sock, "\r" + "[" + str(sock.getpeername()) + "] " + data)
                    except:
                        broadcast(server_socket, sock, "Client (%s, %s) is offline.\n" % addr)
                        print "Client (%s, %s) is offline." % addr
                        sock.close()
                        SERVER_LIST.remove(sock)
                        continue

        # always close connection after done using
        server_socket.close()
    except KeyboardInterrupt:
        print "\nBye."


def broadcast(server_socket, sock, message):
    for socket in SERVER_LIST:
        if socket != server_socket and socket != sock:
            try:
                socket.send(message)
            except:
                socket.close()
                SERVER_LIST.remove(socket)


if __name__ == "__main__":
    sys.exit(server())
