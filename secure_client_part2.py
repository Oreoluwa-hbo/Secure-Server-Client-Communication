from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.fernet import Fernet
import socket
import sys

# Generate RSA keys
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Save public key to a file
pem = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
with open('client_public.pem', 'wb') as f:
    f.write(pem)

# Load server's public key from file
with open('server_public.pem', 'rb') as f:
    pem = f.read()
server_public_key = serialization.load_pem_public_key(pem)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 10001))

# Generate symmetric/secret key
symmetric_key = Fernet.generate_key()

# Encrypt symmetric/secret key
encrypted_symmetric_key = server_public_key.encrypt(symmetric_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

# Encrypt and send message to the server
if len(sys.argv) < 2:
    print("Please provide a message as a command-line argument.")
    sys.exit(1)
message = ' '.join(sys.argv[1:]).encode()
f = Fernet(symmetric_key)
encrypted_message = f.encrypt(message)

# Sign the encrypted message
signature = private_key.sign(encrypted_message, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
client_socket.sendall(encrypted_symmetric_key + encrypted_message + signature)

# Receive and decrypt message from the server
data = client_socket.recv(2048)
encrypted_message_received = data
message_received = f.decrypt(encrypted_message_received)
print("Received message: ", message_received.decode())
