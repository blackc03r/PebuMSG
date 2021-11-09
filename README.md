# PebuMSG
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/pebu1337/PebuMSG/blob/main/LICENSE) [![Open Source](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://opensource.org/) [![Shields.io](https://img.shields.io/badge/shields.io-ok-green.svg?style=flat)](http://shields.io/) [![Version](https://badge.fury.io/gh/tterb%2FHyde.svg)](https://badge.fury.io/gh/pebu1337%2FPebuMSG) <br>
A simple end to end encrypted self hosted messaging solution. Designed to solve trust issues with centralized service providers. <br>
<b/>Still in pre-alpha, no audit or rigourous security testing done yet.</b>
## Features
* End to end encrypted. Transport encryption between server and client. Messages are encrypted with the clients public key that is only stored on the client machine. Server cannot view the contents of the message ever.
## Risks
* IP is not anonymized, while it is not stored by the server on purpose, an adversary can modify the servers source code to log that.
* Server can see how many messages a specific address has, while the server cannot see who sent the message or the message.
* Public and Private key are saved in plaintext on the client machine.
## To do list
* Implement source code checking, sends an alert on sign on if the server is running modified source code.
* Clean up code and inital handshake technique.
* Allow for more customization options.
* Better memory optimization.
## Future Ideas
* Create a group chat feature.
* Create an onion routing protocol to hide IP addresses. 
* Create a GUI.
### Installation
```pip install eciespy``` <- Prerequesite for encryption library. <br>
Port forward port 60000/tcp to the server if necessasary. <br>
Run the server.py script as you would normally, if a private key is not in private.txt and a public key is not in public.txt, the server will generate one. <br>
### Testing 
I run a free node for this service located @ 18.215.143.240:60000 <br>
Please shoot me a message on there @ 0xc31aa1d1d1016a81648cc0f5f002e53502795f9c784daf454540821149d739143bc16467dc3d99a18bea457fced89003693ff55361ca41327c32de22de947a84
