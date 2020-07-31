#Socket client example in python
 
import socket   #for sockets
import sys      #for exit
from thread import *
import struct

ip = ""
cHOST = '';            #client server Host-Port
cPORT = 5001;

try:
	s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # socket gia na ginei o client server gia na steilei arxeia 
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit()

try:  
	s2.bind((cHOST, cPORT))
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
    
s2.listen(10)
print 'Socket now listening...'


def clientthread(a):                            # Thread gia na steilei to arxeio pou ziteitai (serverclient)
	conn, addr = s2.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
	conn.send('Hello.Which file would you want me to send?')
	cldata = conn.recv(1024)
	
	with open(cldata, 'rb') as f:
		chunk=f.read()
		
	chunk = chunk + '**********'              # Diaxwristiko sto telos pou simatodotei to telos tou arxeiou
	conn.sendall(chunk)
	print 'File sent.'
	conn.close()
	start_new_thread(clientthread ,(1,))      # Kainourio thread gia tin epomeni apostoli arxeiou
	
start_new_thread(clientthread ,(1,))          

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

except socket.error:
    print 'Failed to create socket.'
    sys.exit()
     
print 'Socket Created.'
 
host = '127.0.0.1';
port = 5000;

#Connect to remote server
s.connect((host , port))
s.send(str(cPORT))                  # Stelnoume to port sto opoio o ka8e client exei to socket pou leitourgei san server

print 'Socket Connected to server on ip ' + host 

data = s.recv(1024)   # Welcome to the server
print data

while True:
	
	print '\nWhat would you like to do?\nPress the number of the option:\n1.List of all files\n2.Upload file\n3.Download file from client\n4.Exit\n'

	msgreq = raw_input()
	
	s.send(msgreq)
	
	if int(msgreq)==4:
		sys.exit()
	
	if int(msgreq)==1:
		data = s.recv(1)
		
		if data=='Y':
			print 'Empty list!\n'
		elif data=='N':
			fsize = s.recv(4)                             # Mege8os tis listas me ta arxeia se packed morfi
			flength = struct.unpack('!I', fsize)[0]       # Unpack to mege8os
			for i in range(0,flength):                    # Epanalipsi mexri na parei ola ta arxeia tis listas
				size = s.recv(4)                          # Mege8os ka8e kataxwrisis pou stelnete tis listas
				length = struct.unpack('!I', size)[0]     # Unpack to mege8os
				data2 = s.recv(length)                    # Diavazoume akrivos tosa byte osa einai h kataxwrhsh
				print data2
	
	if int(msgreq)==3:
		ip = ""
		print 'Type the name of the Client:\n'
		msg = raw_input()
		s.sendall(msg)
		print 'Type the name of the file:\n'
		msg = raw_input()
		s.sendall(msg)
		data = s.recv(1024)
		for i in range(1,len(data)):                     # Diaxwrismos tou IP tou client pou exei to arxeio apo to paketo pou molis lavame
			if data[i] != "'":
				ip = ip + data[i]
			else:
				break
		data = s.recv(1024)                              # Receive tis portas tou client-server poy exei to arxeio
		
		try:
			s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # socket gia na zitisei arxeia kai na kanei sundesi me to server-client
		except socket.error, msg:
			print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
			sys.exit()
			
		s3.connect((ip, int(data)))                  # Sundesi ston client pou exei to arxeio
		cdata = s3.recv(1024)  
		print cdata                                  # 'Type the name of the file:'
		cmsg = raw_input()                           # to cmsg perilamvanei to onoma tou arxeiou pou zitaei o client
		s3.sendall(cmsg)
		newfile = open(cmsg, 'wb')                   # Dimiourgia tou arxeiou
		while True:
			rdata = s3.recv(1024)                    # Diavasma dedomenwn mexri na vre8ei to diaxwristiko '**********' pou simatodotei to telos tou arxeiou
			if '**********' in rdata:
				size = len(rdata) - 10
				newfile.write(rdata[:size])
				newfile.close()
				print 'File created.'
				break
			else:
				newfile.write(rdata)
		
	if int(msgreq)==2:
		data = s.recv(1024)                        # 'Type the name of the file'
		print data
		msg = raw_input()
		s.sendall(msg)
		data = s.recv(1)
		if data == 'D':                             # Simainei oti uparxei diplotypo
			data = s.recv(1024)                     # katallhlo minima apo to server gia tin apofugh diplotypwn
			print data
			
s.close()
s2.close()
s3.close()