"""

MP4 of COSC435

Yuming Wang <yw850@georgetown.edu>
Georgetown University


"""
from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import encrypted_package_pb2
import argparse
import socket
import sys
import select
import struct



def solve_IM(args, user_input):
    IM = encrypted_package_pb2.IM()
    IM.nickname = args.nickname
    IM.message = user_input
    IM_string = IM.SerializeToString()
    return IM_string

def solve_PT(auth_key, IM_string):
    plaintext = encrypted_package_pb2.PlaintextAndMAC()
    plaintext.paddedPlaintext = pad(IM_string, AES.block_size)
    # HMAC
    h = HMAC.new(auth_key, digestmod=SHA256)
    h.update(IM_string)
    plaintext.mac = h.digest()
    PT_string = plaintext.SerializeToString()
    return PT_string

def solve_EP(iv, conf_key, PT_string):
    encrypted_package = encrypted_package_pb2.EncryptedPackage()
    encrypted_package.iv = iv
    cipher = AES.new(conf_key, AES.MODE_CBC, iv=iv)
    encrypted_package.encryptedMessage = cipher.encrypt(pad(PT_string, AES.block_size))
    EP_string = encrypted_package.SerializeToString()
    return EP_string



def main():
    parser = argparse.ArgumentParser()
    # add required arguments
    parser.add_argument('-p', dest='port', help='port number', required=True, type = int)
    parser.add_argument('-s', dest='servername', help='name of the server', required=True)
    parser.add_argument('-n', dest='nickname', help='your nickname', required=True)
    parser.add_argument('-c', dest='conf_key', help='confidentiality key', required=True)
    parser.add_argument('-a', dest='auth_key', help='authenticity key', required=True)
    args = parser.parse_args()

    # create a socket FOR INCOMING CONNECTIONS
    # s is client socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((args.servername, args.port))
    read_handles = [sys.stdin, s]

    conf_key = SHA256.new(args.auth_key.encode('utf-8')).digest()
    auth_key = SHA256.new(args.auth_key.encode('utf-8')).digest()
    iv = get_random_bytes(16)

    while True:
        ready_to_read_list, _, _ = select.select(read_handles, [], [])
        for i in ready_to_read_list:
            # new data from server
            if i == s:
                data_len_packed = i.recv(4, socket.MSG_WAITALL)
                data_len = struct.unpack('!L', data_len_packed)[0]
                protobuf = i.recv(data_len, socket.MSG_WAITALL)

                encrypted_package = encrypted_package_pb2.EncryptedPackage()
                encrypted_package.ParseFromString(protobuf)
                cipher = AES.new(conf_key, AES.MODE_CBC, iv=encrypted_package.iv)
                serialPlain = unpad(cipher.decrypt(encrypted_package.encryptedMessage), AES.block_size)

                plaintextAndMacPackage = encrypted_package_pb2.PlaintextAndMAC()
                plaintextAndMacPackage.ParseFromString(serialPlain)
                serialIM = unpad(plaintextAndMacPackage.paddedPlaintext, AES.block_size)
                im = encrypted_package_pb2.IM()
                im.ParseFromString(serialIM)

                test_mac = HMAC.new(auth_key, digestmod=SHA256)
                test_mac.update(serialIM)
                try:
                    test_mac.verify(plaintextAndMacPackage.mac)
                    print("(%s,%s)" % (im.nickname, im.message))
                except:
                    print("ERROR! Received message that could not be authenticated!")

            # new data from STDIN
            else:
                user_input = input()
                if user_input.lower() == 'exit':
                    s.close()
                    break
                else:
                    # solve IM
                    IM = solve_IM(args, user_input)
                    # solve plaintext
                    serialized_plaintext = solve_PT(auth_key, IM)
                    # solve encrypted_package
                    e_message = solve_EP(iv, conf_key, serialized_plaintext)
                    length_of_e_message = struct.pack('!L', len(e_message))
                    s.send(length_of_e_message)
                    s.send(e_message)


if __name__ == '__main__':
    main()
