lastData = "Pebu1337/PebuMSG"
import socket
import sys
from _thread import *
import hashlib
from Crypto import Random
from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt
import random
import string
HOST = '' # Binds to all network interfaces
PORT = 60000	
currentlyConnected = ['']
msgs = {'address':'message'}
try:
    f = open('public.txt')
    server_pk = f.readline()
    f.close()
    f = open('private.txt')
    privateKey = f.readline()
    f.close()
except Exception as e:
    privateKeyObject = generate_eth_key()
    privateKey = privateKeyObject.to_hex()
    server_pk = privateKeyObject.public_key.to_hex()
    f = open('public.txt', 'w')
    f.write(server_pk)
    f.close()
    f = open('private.txt', 'w')
    f.write(privateKey)
    f.close()
    privateKeyObject = ' ' 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	s.bind((HOST, PORT))
except socket.error as msg:
	print ('Bind failed. Error Code : ' + str(msg))
	sys.exit()
def recieve(s):
    while True:
        try :
            data = s.recv(15000)
        except Exception as e:
            return None
        if data:
            try:
                data = decrypt(privateKey, data)
            except ValueError:
                pass
            data = str(data)
            data = data.replace("b'", "")
            data = data.replace("'", "")
            data = data.replace('b"', "")
            data = data.replace("\\n","\n")
            data = data.replace('"', "")
            return data
def send(s, msg, pk=None):
    if (pk != None):
        s.sendall(encrypt(pk, bytes(str(msg),'utf-8')))
    else:
        s.sendall(bytes(str(msg),'utf-8'))
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
s.listen(10)
print ('PebuMSG Server Established.')   
def checkMessages(clientUUIDinfo):
        try :
            if (msgs[clientUUIDinfo] == '' or msgs[clientUUIDinfo] == None):
                msgs[clientUUIDinfo] == ''
                messagesExist = False
            else:

                messagesExist = True #here
        except KeyError:
            messagesExist = False
        return messagesExist
def sendMessage(address, fromAddress, message):
    if (checkMessages(address)):
        msgs[address] = msgs[address] + "PEBUMSG.CASE.NEWMSG" + message
    else:
        msgs[address] = "PEBUMSG.CASE.NEWMSG"  + message
    return None   
def clientthread(conn, addr):
    global currentlyConnected
    global msgs
    conn.send(b'Connection initiated.') 
    clientUUID = recieve(conn)
    try :
        if (msgs[clientUUID] == '' or msgs[clientUUID] == None):
            msgs[clientUUID] == ''
            messagesExist = False
        else:
            messagesExist = True #here
    except KeyError:
        messagesExist = False
    send(conn, clientUUID)
    verificationPhrase = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
    verificationPhrase = bytes(str(verificationPhrase), 'utf-8')
    encryptedVerificationPhrase = encrypt(clientUUID, verificationPhrase)
    rawSend(conn, encryptedVerificationPhrase)
    clientSECRET = rawRecieve(conn)
    if (clientSECRET != verificationPhrase):
        print('Imposter detected: on ' + addr[0] + ":" + str(addr[1]))
        return
    send(conn, server_pk, clientUUID)
    recieve(conn)
    if (messagesExist):
        send(conn, 'You have logged in as ' + clientUUID +'\nYou have new messages!', clientUUID)
    else:
        send(conn, 'You have logged in as ' + clientUUID, clientUUID)
    currentlyConnected.append(clientUUID)
    print('Connected with ' + clientUUID + ' on ' + addr[0] + ":" + str(addr[1]))
    while True:
            try:
                data = recieve(conn)
                if not data:
                    break
                if (data == lastData):
                    pass
                else:
                    data==lastData 
                    if (str(data).startswith("PEBUMSG.CASE.SNDMSG") == True):
                        message = data[149:]
                        address = data[:149]
                        address = address[-130:]
                        sendMessage(address, clientUUID, message)
                        send(conn,"The message has been delivered successfully.", clientUUID)
                    elif (str(data).startswith("PEBUMSG.CASE.CHKMSG")):
                        if (checkMessages(clientUUID) == True):
                            send(conn, msgs[clientUUID], clientUUID)
                            msgs[clientUUID] = ''
                            messagesExist = False
                        else:
                            send(conn, "PEBUMSG.CASE.NOMSGS")
                    elif (str(data).startswith("PEBUMSG.CASE.CONNEC")):
                        send(conn, "Your UUID = " + clientUUID + "\nServ UUID = " + server_pk, clientUUID)
                    else:
                        print(data)
            except ConnectionAbortedError:
                break
            except ConnectionResetError:
                break
    print('Connection with ' + clientUUID + ' on ' + addr[0] + ":" + str(addr[1]) + ' terminated.')
    conn.close()
    currentlyConnected.remove(clientUUID)
while 1:
	conn, addr = s.accept()
	start_new_thread(clientthread ,(conn, addr))

s.close()
