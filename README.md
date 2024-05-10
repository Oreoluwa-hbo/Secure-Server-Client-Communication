# Secure-Server-Client-Communication

Secure Server and Client Communication

Oreoluwa Adegbesan NET4005 Assignment 3

Part 1:
In the first part (secure_server_part1 and secure_client_part1), RSA encryption is used for both encrypting the messages and signing them.

How it works
Both the server and the client generate their own RSA keys.
The client encrypts the message with the server’s public key and signs it with its own private key.
The client sends the encrypted message and the signature to the server.
The server decrypts the message with its private key and verifies the signature with the client’s public key.
The server then encrypts the response with the client’s public key and sends it back (two-directional message flow).
The client decrypts the response with its private key.
This makes sure that only the intended recipient can read the message and that the message has not been tampered with in transit.

Part 2:
In the second part (secure_server_part2 and secure_client_part2), symmetric encryption (Fernet) is used for encrypting the messages.

How it works
Both the server and the client generate their own RSA keys.
The client generates a symmetric key (Fernet key).
The client uses this symmetric key to encrypt the message.
The client signs the encrypted message using its private key.
The client then encrypts the symmetric key using the server’s public key.
The client sends the encrypted symmetric key, the encrypted message, and the signature to the server.
The server decrypts the symmetric key using its private key.
The server verifies the signature of the encrypted message using the client’s public key.
The server decrypts the message using the symmetric key.
This approach combines the efficiency of symmetric encryption with the security of RSA encryption for key exchange.
Two directional message flow is also implemented here

Testing
To test these implementations, you need to run the server script first and add a message then the client script with a message. Make sure both scripts are using the same port number. The client script will send a message to the server, and the server will respond with the message written. The messages will be printed to the console.

Run the client from the console/terminal using: <python3/python> secure_client_part<1/2>.py <add message here>
Run the server from the console/terminal using: <python3/python> secure_server_part<1/2>.py <add message here>

Example:

python3 secure_server_part2.py "Sending encrypted message to server"
python3 secure_client_part2.py "Message received thank you client"

