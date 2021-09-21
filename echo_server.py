"""

MP2 of COSC435

Yuming Wang <yw850@georgetown.edu>
Georgetown University


"""

import argparse
import socket



def main():
    parser = argparse.ArgumentParser()
    reverse = False

    # add an optional argument
    parser.add_argument('-r', '--reverse', dest='reverse_0', help='activate reverse mode',action="store_true")

    # add a required argument
    parser.add_argument('-p', '--port', dest='port', help='port number', required=True, type=int)

    args = parser.parse_args()

    if args.reverse_0 is True:
        reverse = True

    #if args.reverse_1 is True:
    #    reverse = True

    # create an INET, STREAMing socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to a public host, and a well-known port
    serversocket.bind(('localhost', args.port))
    # become a server socket
    serversocket.listen(5)
    while True:
        # accept connections from outside
        clientsocket, address = serversocket.accept()
        while True:
            #require buffer at least 1024 bytes
            response = clientsocket.recv(4096)
            if not response:
                break
            if reverse == True:
                #reverse
                r_response = response[::-1]
                r_response = r_response.lstrip()
                r_response = r_response + b"\n"
                clientsocket.send(r_response )
            else:
                clientsocket.send(response)
        clientsocket.close()





if __name__ == '__main__':
    main()
