import tornado
import functools
import base64
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP


authHeaderKey = 'Authtoken'


def authenticate(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):

        try:
            if authHeaderKey not in self.request.headers:
                raise Exception('Authentication failed, no auth headers found')

            token = self.request.headers[authHeaderKey]

            decrypted_token = verify_and_decrypt_token(token, self.rsa_key_string)

            self.currentUser = tornado.escape.json_decode(decrypted_token)

            return method(self, *args, **kwargs)
        except:
            self.set_status(401)
            return self.write('Unauthorized')
    return wrapper


def generate_token(data, rsa_key_string):
    rsaKey = RSA.import_key(rsa_key_string)

    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(rsaKey)
    encrypted_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data.encode())

    result = encrypted_session_key + cipher_aes.nonce + tag + ciphertext

    return base64.b64encode(result).decode()


def verify_and_decrypt_token(data, rsa_key_string):
    private_key = RSA.import_key(rsa_key_string)

    decoded_bytes = base64.b64decode(data)

    enc_session_key = decoded_bytes[0:private_key.size_in_bytes()]
    nonce = decoded_bytes[private_key.size_in_bytes():private_key.size_in_bytes()+16]
    tag = decoded_bytes[private_key.size_in_bytes() + 16:private_key.size_in_bytes() + 32]
    ciphertext = decoded_bytes[private_key.size_in_bytes() + 32:]

    # Decrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)

    return data.decode()
