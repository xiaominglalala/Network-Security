import struct
from Crypto.Cipher import AES
from encrypted_package_pb2 import EncryptedPackage, PlaintextAndMAC, IM
from Crypto.Util.Padding import pad
import binascii
import automator

# first, we take an IM
im = IM()
im.nickname = 'Alice'
im.message = 'coding is fun'
serialized_im = im.SerializeToString()

# then we create a structure to hold the serialized IM along with a MAC
plaintext = PlaintextAndMAC()
plaintext.paddedPlaintext = pad(serialized_im,AES.block_size)
plaintext.mac = b'12345'        # I'll let you figure this out
serialized_plaintext = plaintext.SerializeToString()

# next, we create a structure to hold the encrypted plaintext+MAC along with an IV
encrypted_package = EncryptedPackage()
encrypted_package.iv = b'12345' # I'll let you figure this out
#encrypted_package.encryptedMessage = do_encryption(key,serialized_plaintext)
encrypted_package.encryptedMessage = serialized_plaintext # this needs to be encrypted; see above line
serialized_encrypted_package = encrypted_package.SerializeToString()


# now that we have our final data structure to send over the wire
# (serialized_encrypted_package), we need to send it.  First, we'll send
# the length, and then the serialized structure
length_of_encrypted_package = len(serialized_encrypted_package)
packed_length_of_encrypted_package = struct.pack('!L',length_of_encrypted_package) # note this takes up 4 bytes (not 2)!

# since we're not actually on the network, we'll comment out send() calls and
# use print statements -- for learning purposes.
# sock.send( packed_length_of_encrypted_package )
print( "length of encrypted_package = %d; packed lenth specifier = %d" %
       (length_of_encrypted_package, len(packed_length_of_encrypted_package)) )
# sock.send( serialized_encrypted_package )
print( "serialized_encrypted_package (in hex) = %s" % binascii.hexlify(serialized_encrypted_package) )

