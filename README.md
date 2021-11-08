# PebuMSG
An end to end encrypted self hosted messaging solution. 
## Features
* End to end encrypted. Transport encryption between server and client. Messages are encrypted with the clients public key that is only stored on the client machine. Server cannot view the contents of the message ever.
## Risks
* IP is not anonymized, while it is not stored by the server on purpose, an adversary can modify the servers source code to log that.
* Server can see who sent the message and who is recieving it. 
## To do list
* Implement source code checking, sends an alert on sign on if the server is running modified source code.
* Clean up code and inital handshake technique.
* Allow for more customization options.
* Better memory optimization.
## Future Ideas
* Create a more text like environment.
* Create a group chat feature.
* Create an onion routing protocol to hide IP addresses. 
* Create a GUI.
### Installation
```pip install eciespy``` <- Prequesite for encryption library. <br>
Port forward port 60000 to the server if necessasary. <br>
Run the server.py script as you would normally, if a private key is not in private.txt and a public key is not in public.txt, the server will generate one. <br>
