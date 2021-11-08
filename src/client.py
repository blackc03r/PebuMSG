import socket
import hashlib
import sys
from base64 import b64decode
from base64 import b64encode
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 60000     # The port used by the server
from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt
privateKeyObject = generate_eth_key()
privateKey = privateKeyObject.to_hex()
publicKey = privateKeyObject.public_key.to_hex()
PADDING = '{'
BLOCK_SIZE = 16
def parseResponse(responsemessage):
    parsed = responsemessage.split("PEBUMSG.CASE.NEWMSG")
    messages = "New messages:"
    for i in range(1, len(parsed)):
        msgg = parsed[i][130:]
        msgg = str(decrypt(privateKey, b64decode(msgg)))
        msgg = msgg.replace("b'", "")
        msgg = msgg.replace("'","")
        messages = messages + ("\nFrom: " + parsed[i][:130] + "\nContains: " + msgg)
    return messages
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
def rawRecieve(s):
     while True:
        try :
            data = s.recv(15000)
        except Exception as e:
            return None
        if data:
            return data   
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
    recieve(s)
    send(s, public_readable)
    message = recieve(s)
    if (message != public_readable):
        print('UUID Recieved from server does not match')
        print(message)
        print(public_readable)
        exit()
    phrase = rawRecieve(s)
    decryptedPhrase = decrypt(privateKey, phrase)
    rawSend(s, decryptedPhrase)
    server_pk = recieve(s)
    send(s, 'ok')
    message = recieve(s)
    print(message)
    while 1:
        whatToDo = input("What would you like to do?: ")
        if (whatToDo == 'send' or whatToDo == 'Send' or whatToDo == 'snd' or whatToDo == 'sen' or whatToDo == 'msg'):
            sendingAddress = input("Please input the desired address to send to: ")
            if (len(sendingAddress) != 130):
                print("Invalid address.")
            else:
                data = 'PEBUMSG.CASE.SNDMSG' + sendingAddress
                message = input("What is the message: ")
                if (len(message) <= 2000):
                    data += str(b64encode(encrypt(sendingAddress, bytes(message, 'utf-8'))))
                    rawSend(s,encrypt(server_pk, bytes(data,'utf-8')))
                    print(recieve(s))
                else:
                    print("Message too long. Must be less than 877 characters.")
        elif (whatToDo == 'check' or whatToDo =='chk' or whatToDo == 'Check'):
            send(s, "PEBUMSG.CASE.CHKMSG")
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
            print('wai: Checks connection status and print UUID as returned by the server.')
            print('snd: Sends a message to a given user')
            print('chk: Checks your messages')
        else:
            print("Invalid Command. Type help to see available commands.")
s.close()

    
