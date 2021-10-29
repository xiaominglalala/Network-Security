"""

MP3 of COSC435

Yuming Wang <yw850@georgetown.edu>
Georgetown University


"""

# 1. listen for new connections from clients
# 2. upon receiving a message from a client, it sends a copy of that message to every other client.

import socket
import select
import sys

def main():
    ## some codes from project's example code

    # create a socket FOR INCOMING CONNECTIONS
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # listen to 9999 port
    s.bind(('', 9999))
    # as many as 100 connect requests
    s.listen(100)
    connection_list = [s]

    try:
        while True:
            #
            ready_to_read_list, _, _ = select.select(connection_list, [], [])
            for i in ready_to_read_list:
                # if we get a new connection
                if i == s:
                    # return a socket ("conn") we can use to talk to it
                    conn, addr = s.accept()
                    connection_list.append(conn)
                # if we get message from stdin
                #elif i is sys.stdin:
                #    user_input = input()

                else:
                    message = i.recv(4096)
                    if len(message) == 0:
                        # if someone leave
                        #print("Bye!")
                        i.close()
                        connection_list.remove(i)
                        continue
                    else:
                        # we should send message to people who still here
                        for j in connection_list:
                            if j != s and j != i:
                                j.send(message)
    # ctrl+c
    except KeyboardInterrupt:
        #print("Bye!")
        s.close()
        exit(0)


if __name__ == '__main__':
    main()


