from os import chmod
import stat

from Crypto.PublicKey import RSA


def rsa_key_gen():
    private_key = RSA.generate(2048)
    public_key = private_key.public_key()

    return (private_key.export_key('PEM'), public_key.export_key('OpenSSH'))


def write_key_file(filename, key_byte_array):
    f = open(filename, 'wb')
    f.write(key_byte_array)
    f.close()
    chmod(filename, stat.S_IREAD | stat.S_IWRITE)
