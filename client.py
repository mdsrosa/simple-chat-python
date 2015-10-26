import sys
import socket
import select

RECV_BUFFER = 4096

def client():
    if len(sys.argv) < 3:
        print 'Usage: python %s hostname port' % (sys.argv[0])
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try:
        s.connect((host, port))
    except Exception as e:
        print 'Unable to connect: %s' % e
        sys.exit()

    print 'Connected to remote host. You can start sending message.'
    sys.stdout.write('[Me] '); sys.stdout.flush()

    while True:
        socket_list = [sys.stdin, s]

        # get the list of readable sockets
        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [], 0)

        for sock in ready_to_read:
            if sock == s:
                # message from the server
                data = sock.recv(RECV_BUFFER)

                if not data:
                    print 'Disconnected from ther server.'
                    sys.exit()
                else:
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] '); sys.stdout.flush()
            else:
                # user has entered a message
                message = sys.stdin.readline()
                s.send(message)
                sys.stdout.write('[Me] '); sys.stdout.flush()


if __name__ == '__main__':
    sys.exit(client())
