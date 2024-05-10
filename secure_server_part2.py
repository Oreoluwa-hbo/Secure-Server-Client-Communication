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
with open('server_public.pem', 'wb') as f:
    f.write(pem)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 10001))
server_socket.listen(1)
client_socket, address = server_socket.accept()

# Load client's public key from file
with open('client_public.pem', 'rb') as f:
    pem = f.read()
client_public_key = serialization.load_pem_public_key(pem)

# Receive encrypted symmetric key, message, and signature from client
data = client_socket.recv(2048)
encrypted_symmetric_key, encrypted_message, signature = data[:256], data[256:-256], data[-256:]

# Decrypt symmetric key
symmetric_key = private_key.decrypt(encrypted_symmetric_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

# Verify signature
client_public_key.verify(signature, encrypted_message, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())

# Decrypt message
f = Fernet(symmetric_key)
message = f.decrypt(encrypted_message)

print("Received message: ", message.decode())

# Encrypt and send message to client
if len(sys.argv) < 2:
    print("Please provide a message as a command-line argument.")
    sys.exit(1)
message_to_send = ' '.join(sys.argv[1:]).encode()   # Get message from command line
encrypted_message_to_send = f.encrypt(message_to_send)
client_socket.sendall(encrypted_message_to_send)


