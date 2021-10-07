"""

MP3 of COSC435

Yuming Wang <yw850@georgetown.edu>
Georgetown University


"""

import argparse
import socket
import select
import sys
import broadcastMsg_pb2


def main():
    ## some codes from project's example code
    parser = argparse.ArgumentParser()

    # add a required argument, which can either be specified
    parser.add_argument('-s', '--severname', dest='severname', help='type severname', required=True)
    parser.add_argument('-n', '--nickname', dest='nickname', help='type nickname', required=True)

    args = parser.parse_args()

    # create a socket FOR INCOMING CONNECTIONS
    # s is client socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((args.server, 9999))
    read_handles = [sys.stdin, s]

    while True:
        ready_to_read_list, _, _ = select.select(read_handles, [], [])

        for i in ready_to_read_list:
            if i == s:
                message = s.recv(4096)
                if len(message) == 0:
                    break
                broadcastMsg = broadcastMsg_pb2.broadcastMsg()
                broadcastMsg.ParseFromString(message)
                print("%s: %s\n" % (broadcastMsg.nickname, broadcastMsg.essage), flush=True)
            # new data from STDIN
            else:
                user_input = input()
                # user needs to exit
                if user_input.lower() == 'exit':
                    s.close()
                    break
                # send message to other people
                else:
                    broadcastMsg = broadcastMsg_pb2.broadcastMsg()
                    broadcastMsg.nickname = args.nickname
                    broadcastMsg.message = user_input
                    message = broadcastMsg.SerializeToString()
                    s.send(message)



if __name__ == '__main__':
    main()
