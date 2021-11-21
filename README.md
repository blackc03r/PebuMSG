# PebuMSG
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/pebu1337/PebuMSG/blob/main/LICENSE) [![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/) [![Shields.io](https://img.shields.io/badge/shields.io-ok-green.svg?style=flat)](http://shields.io/) [![Version](https://badge.fury.io/gh/tterb%2FHyde.svg)](https://badge.fury.io/gh/pebu1337%2FPebuMSG) <br>
A simple end to end encrypted self hosted messaging solution. Designed to solve trust issues with centralized service providers. <br>
Not meant as a real time communication solution, more as a secure "dropbox" for messages. <br>
<b/>Still in pre-alpha, no audit or rigourous security testing done yet.</b>
## Features
* End to end encrypted. Transport encryption between server and client. Messages are encrypted with the clients public key that is only stored on the client machine. Server cannot view the contents of the message ever.
* Simple and easy to deploy or learn off of. Entire codebase is less than 1000 lines and will remain that way in perpetuity. 
* Public key encryption for messages between clients and public key encryption for server<->client communication. 
* Only communication that is sent unencrypted is the servers public key to the client, this way a network snooper cannot even get what user is logging in.
## Message Dumping
Example dump of the messages on the server side: <br>
```
'0xc31aa1d1d1016a81648cc0f5f002e53502795f9c784daf454540821149d739143bc16467dc3d99a18bea457fced89003693ff55361ca41327c32de22de947a84': 
'PEBUMSG.CASE.NEWMSGBOvna8sCCgv3MI4dymqD6oBLQvUQNaedgFahz9thQX/Qo3IczQOjBC2mdt/4oEJPtcqkGQh1FKWnHDvqAqwgYNXtTnXc+J21c+SZ0XSCCnOF3FG9OwlXKsU4FqRk4mrhaIT9z9zGdY/TXEyQHD4ZeFEBkcgC2/hjQFKlFHMPg5XPBiowAdPSPC+87vwQrWZXOcJJmKD+dO2KCGqdtzFsM3iR/vLXcJzaIex8o56N1/dMbYWJhAJZ4oI14A3Q9FfhCd+X0wlKfXz4D1OL3BngGb8JAGyY/HXaeOfPp0o6ymWbHr6y3mm6WlLwRPg='}
```
What the client(0xc31a...47a84) recieving this sees: <br>
```
From: 0x6180bff027c8ae6b765c4cc482be5cd074667ca4626af18fcfc46d9c5f9d4bf9b935df90f606b58eb5fc33f799d8b792503a5cbe407a8ed845608805543f1350
hi test 1 
```
## Risks
* IP is not anonymized, while it is not stored by the server on purpose, an adversary can modify the servers source code to log that.
* Server can see how many messages a specific address has, while the server cannot see who sent the message or the message.
* Public and Private key are saved in plaintext on the client machine.
## To do list
* Implement source code checking, sends an alert on sign on if the server is running modified source code.
* ~~Clean up code and inital handshake technique.~~ # Done 19-11-2021
* Allow for more customization options.
* Better memory optimization.
## Future Ideas
* Create a group chat feature.
* Create an onion routing protocol to hide IP addresses. 
* Create a GUI.
### Server Installation
```pip install eciespy``` <- Prerequesite for encryption library. <br>
Port forward port 60000/tcp to the server if necessasary. <br>
Run the server.py script as you would normally, if a private key is not in private.txt and a public key is not in public.txt, the server will generate one. <br>
### Client Installation
```pip install eciespy``` <- Prerequesite for encryption library. <br>
Run the IdentityGenerator.py file to generate an identity to use on the platform. <br>
By default, client.py is configured to connect to the default open node that I run, you can change this if you have a different node. <br>
Run ```help``` at the prompt to see a list of commands. 
### Testing 
The default node in client.py is currently a node controlled by me run on AWS. Do not consider this node secure by any means. <br>
I run a free node for this service located @ 18.215.143.240:60000 <br>
Please shoot me a message on there @  <b/>0xc31aa1d1d1016a81648cc0f5f002e53502795f9c784daf454540821149d739143bc16467dc3d99a18bea457fced89003693ff55361ca41327c32de22de947a84</b>
