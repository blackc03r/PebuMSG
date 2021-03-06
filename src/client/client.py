import socket, hashlib, sys
from base64 import b64decode, b64encode
HOST = '18.215.143.240'  # The server's hostname or IP address
PORT = 60000     # The port used by the server
from library import generate_eth_key, generate_key, encrypt, decrypt
try:
    f = open('public.pem')
    publicKey = f.readline()
    f.close()
    f = open('private.pem')
    privateKey = f.readline()
    f.close()
except Exception as e:
    privateKeyObject = generate_eth_key()
    privateKey = privateKeyObject.to_hex()
    publicKey = privateKeyObject.public_key.to_hex()
    f = open('public.pem', 'w')
    f.write(publicKey)
    f.close()
    f = open('private.pem', 'w')
    f.write(privateKey)
    f.close()
    print("Rewrote public.pem and private.pem due to an error reading it. If these files did not exist before there is nothing to worry about.")
def parseResponse(responsemessage):
    parsed = responsemessage.split("PEBUMSG.CASE.NEWMSG")
    messages = { 'beginning' : 'Messages: '}
    addresses = []
    messagesString = ""
    for i in range(1, len(parsed)):
        try:
            msgg = stripBytes(str(decrypt(privateKey, b64decode(parsed[i][304:]))))
            address = stripBytes(str(decrypt(privateKey, b64decode(parsed[i][:304]))))
            try:
                messages[address] = messages[address] + "\n" + msgg
            except KeyError:
                messages[address] = msgg
                addresses.append(address)
        except ValueError:
            messagesString += "\nInvalid message: " + parsed[i]
    for x in range(0, len(addresses)):
        messagesString += "\nFrom: " + addresses[x] + "\n" + messages[addresses[x]] 
    return messagesString
def recieve(s):
    while True:
        data = s.recv(15000)
        if not data:
            pass
        if data:
            try :
                data = decrypt(privateKey, data)
            except ValueError:
                pass
            data = stripBytes(data)
            return data
def stripBytes(data):
    data = str(data)
    data = data.replace("b'", "")
    data = data.replace("\\n","\n")
    data = data.replace("'", "")
    data = data.replace('b"', "")
    data = data.replace(r"\\n","\n")
    data = data.replace('"', "")
    data = data.replace(r'''\\''', '''\\''') 
    return data   
def rawSend(s, bytes):
    s.sendall(bytes) 
def send(s, msg, pk=None):
    if (pk != None):
        s.sendall(encrypt(pk, bytes(str(msg), 'utf-8')))
    else:
        s.sendall(bytes(str(msg), 'utf-8'))
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Node not found.")
        exit()
    server_pk = recieve(s)
    send(s, publicKey, server_pk)
    print(recieve(s))
    while 1:
        whatToDo = input("What would you like to do?: ")
        if (whatToDo == 'send' or whatToDo == 'Send' or whatToDo == 'snd' or whatToDo == 'sen' or whatToDo == 'msg'):
            sendingAddress = input("Please input the desired address to send to: ")
            sendingAddress = sendingAddress.strip()
            if (len(sendingAddress) != 130):
                print("Invalid address.")
            else:
                data = 'PEBUMSG.CASE.SNDMSG' + sendingAddress
                message = input("What is the message: ")
                if (len(message) <= 1580):
                    data += str(b64encode(encrypt(sendingAddress, bytes(message, 'utf-8'))))
                    rawSend(s,encrypt(server_pk, bytes(data,'utf-8')))
                    print(recieve(s))
                else:
                    print("Message too long. Must be less than 877 characters.")
        elif (whatToDo == 'check' or whatToDo =='chk' or whatToDo == 'Check'):
            send(s, "PEBUMSG.CASE.CHKMSG", server_pk)
            response = recieve(s)
            if (response.startswith("PEBUMSG.CASE.NOMSGS")):
                print("No new messages on this swarm.")
            else:
                msgs = parseResponse(response)   
                print(msgs)
        elif (whatToDo == 'whoami' or whatToDo == 'wai'):
            send(s, "PEBUMSG.CASE.CONNEC", server_pk)
            response = recieve(s)
            print(response + "\nCurrent Node: " + HOST)
        elif (whatToDo == 'help' or whatToDo == 'Help'):
            print('wai: Checks connection status and print UUID as returned by the server. \nsnd: Sends a message to a given user \nchk: Checks your messages')
        else:
            print("Invalid Command. Type help to see available commands.")
s.close()
