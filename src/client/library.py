import hashlib 
import codecs
from typing import Union
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import HKDF
from Crypto.Hash import SHA256
from coincurve import PrivateKey, PublicKey
from coincurve.utils import get_valid_secret
from eth_keys import keys
AES_CIPHER_MODE = AES.MODE_GCM
AES_KEY_BYTES_LEN = 32
__all__ = [
    "sha256",
    "generate_key",
    "generate_eth_key",
    "hex2prv",
    "hex2pub",
    "aes_encrypt",
    "aes_decrypt",
]
def remove_0x(s: str) -> str:
    if s.startswith("0x") or s.startswith("0X"):
        return s[2:]
    return s
def decode_hex(s: str) -> bytes:
    return codecs.decode(remove_0x(s), "hex")  # type: ignore
def sha256(msg: bytes) -> bytes:
    return hashlib.sha256(msg).digest()
def generate_key() -> PrivateKey:
    return PrivateKey(get_valid_secret())
def generate_eth_key() -> keys.PrivateKey:
    return keys.PrivateKey(get_valid_secret())
def hex2pub(pub_hex: str) -> PublicKey:
    uncompressed = decode_hex(pub_hex)
    if len(uncompressed) == 64:  # eth public key format
        uncompressed = b"\x04" + uncompressed
    return PublicKey(uncompressed)
def hex2prv(prv_hex: str) -> PrivateKey:
    return PrivateKey(decode_hex(prv_hex))
def encapsulate(private_key: PrivateKey, peer_public_key: PublicKey) -> bytes:
    shared_point = peer_public_key.multiply(private_key.secret)
    master = private_key.public_key.format(compressed=False) + shared_point.format(
        compressed=False
    )
    derived = HKDF(master, AES_KEY_BYTES_LEN, b"", SHA256)
    return derived  # type: ignore
def decapsulate(public_key: PublicKey, peer_private_key: PrivateKey) -> bytes:
    shared_point = public_key.multiply(peer_private_key.secret)
    master = public_key.format(compressed=False) + shared_point.format(compressed=False)
    derived = HKDF(master, AES_KEY_BYTES_LEN, b"", SHA256)
    return derived  # type: ignore
def aes_encrypt(key: bytes, plain_text: bytes) -> bytes:
    aes_cipher = AES.new(key, AES_CIPHER_MODE)

    encrypted, tag = aes_cipher.encrypt_and_digest(plain_text)  # type: ignore
    cipher_text = bytearray()
    cipher_text.extend(aes_cipher.nonce)  # type: ignore
    cipher_text.extend(tag)
    cipher_text.extend(encrypted)
    return bytes(cipher_text)
def aes_decrypt(key: bytes, cipher_text: bytes) -> bytes:
    iv = cipher_text[:16]
    tag = cipher_text[16:32]
    ciphered_data = cipher_text[32:]
    aes_cipher = AES.new(key, AES_CIPHER_MODE, nonce=iv)
    return aes_cipher.decrypt_and_verify(ciphered_data, tag)  # type: ignore
def encrypt(receiver_pk: Union[str, bytes], msg: bytes) -> bytes:
    ephemeral_key = generate_key()
    if isinstance(receiver_pk, str):
        receiver_pubkey = hex2pub(receiver_pk)
    elif isinstance(receiver_pk, bytes):
        receiver_pubkey = PublicKey(receiver_pk)
    else:
        raise TypeError("Invalid public key type")

    aes_key = encapsulate(ephemeral_key, receiver_pubkey)
    cipher_text = aes_encrypt(aes_key, msg)
    return ephemeral_key.public_key.format(False) + cipher_text
def decrypt(receiver_sk: Union[str, bytes], msg: bytes) -> bytes:
    if isinstance(receiver_sk, str):
        private_key = hex2prv(receiver_sk)
    elif isinstance(receiver_sk, bytes):
        private_key = PrivateKey(receiver_sk)
    else:
        raise TypeError("Invalid secret key type")

    pubkey = msg[0:65]  # uncompressed pubkey's length is 65 bytes
    encrypted = msg[65:]
    ephemeral_public_key = PublicKey(pubkey)

    aes_key = decapsulate(ephemeral_public_key, private_key)
    return aes_decrypt(aes_key, encrypted)
