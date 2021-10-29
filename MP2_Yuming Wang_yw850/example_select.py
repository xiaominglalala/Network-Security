import socket
import select
import sys


# create a socket FOR INCOMING CONNECTIONS
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# tell the computer on what port to listen to
s.bind(('', 9999))

s.listen(1)

# wait until we ACCEPT a connection from another host
# and return a socket ("conn") we can use to talk to it
conn, addr = s.accept()

# here are the things we want to read from
read_handles = [ sys.stdin, conn ]

while True:
    # this statement is super important... it's the crux of the whole
    # thing.  In a nutshell, it waits/blocks until there's data to
    # read from ANY (and potentially more than one) of the elements
    # defined in read_handles
    ready_to_read_list, _, _ = select.select(read_handles, [], [])

    # if we get here, then there's something to read.  we just need
    # to figure out what
    
    if sys.stdin in ready_to_read_list:
        # we have new data from STDIN...
        # ...so let's actually read it!
        user_input = input()
        # and let's send to the connected party
        conn.send( (user_input + "\n").encode('utf-8') )

    if conn in ready_to_read_list:
        # we have new data from the network!
        # ... so let's print it out
        data = conn.recv(1024)
        if len(data) == 0:
            print( "Bye!" )
            exit(0)
        print( data )


        
