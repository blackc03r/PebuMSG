from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt
from base64 import b64decode, b64encode
print("Welcome to PebuMSG identity generator.")
privateKeyObject = generate_eth_key()
privateKey = privateKeyObject.to_hex()
publicKey = privateKeyObject.public_key.to_hex()
try:
    msg = encrypt(publicKey, b'This key is valid.')
except binascii.Error:
    privateKeyObject = generate_eth_key()
    privateKey = privateKeyObject.to_hex()
    publicKey = privateKeyObject.public_key.to_hex()
    msg = encrypt(publicKey, b'This key is valid.')
assert str(decrypt(privateKey, msg)) == "b'This key is valid.'"
f = open('public.pem', 'w')
f.write(publicKey)
f.close()
f = open('private.pem', "w")
f.write(privateKey)
f.close()
print('Your public key has been saved in public.pem! \nYour private key has been saved in private.pem!')
