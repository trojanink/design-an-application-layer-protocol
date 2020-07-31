import socket
import sys
from thread import *
import struct

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 5000 # Arbitrary non-privileged port

m=0
x=0
flag=0
counter =0
conns = []
files = []
clients = []
ipport = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'
 
#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    conn.send('Welcome to the server\n')
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
        global counter
        global flag
        for i in range (0,len(clients)):                                # Vriskei to trexwn client gia tin apo8ikeusi twn arxeiwn pou ekei kanei upload
			if conn==clients[i][1]:
				temp = clients[i][0]
				break
				
        data = conn.recv(1024)
        
        if int(data)==4:                                                # Kleinei to sugkekrimeno thread katopin epilogis tou client
			return
			
        if int(data)==3:                                                # 3 einai h  epilogh tou download file
			name = conn.recv(1024)
			filename = conn.recv(1024)
			for i in range(0,len(files)):
				if name==files[i][0] and filename==files[i][1]:         # Vriskei ton client ston pinaka files pou exei to arxeio pou ziti8ike
					pos = i
					break
			for i in range(0,len(clients)):                             # Vriskei to conn tou client pou vrikame proigoumenos
				if clients[i][0] == files[pos][0]:
					temp2 = clients[i][1]
					break
			for i in range(0,len(conns)):                               # Vriskei to ip address tou conn tou client pou vrikame proigoumenos
				if conns[i][0] == temp2:
					temp3 = conns[i][1]
					conn.send(str(conns[i][1]))                         # Stelnei to ip adress tou client pou exei to arxeio se auton pou to zitaei
					break
			for i in range(0,len(ipport)):
				if ipport[i][0] == temp3:
					print 'Sending socket port...'
					conn.send(str(ipport[i][1]))                        # Stelnei tin Port tou serversocket tou client se auton pou zitaei to arxeio
					break
			
        if int(data)==1:                                                # 1 einai h epilogh  List of files
			if counter==0:                                              # Simainei oti einai adeia h lista twn arxeiwn
				conn.send('Y')
			else:                                                       # Simainei oti dn einai adeia h lista twn arxeiwn
				conn.send('N')
				filessize = len(files)                                  # Mege8os tis listas files
				sfilessize = struct.pack('!I', filessize)               # Pack to mege8os tis listas se Network(Big Endian
				conn.send(sfilessize)
				
				for row in files:
					size = len(row[0]) + 3 + len(row[1])                # Mege8os ka8e kataxwrisis stin lista files
					ssize = struct.pack('!I', size)                     # Pack to mege8os tis kataxwrisis se  Network(Big Endian) Unsigned Int
					conn.send(ssize)
					conn.sendall(row[0]+ ' ' + ':' + ' ' +row[1])       # Stelnei tin lista twn arxeiwn mazi kai tous clients apo opoy proerxonte
				
        if int(data)==2:                                                # 2 einai h epilogh  Upload file
			flag = 0
			conn.send('Type the name of the file:\n')
			data = conn.recv(1024)
			for i in range(0,len(files)):                               # Vriskei an to onoma tou arxeiou pou edwse o client uparxei mesa stin lista ( apofugh diplotypon kataxwrisewn )
				if temp == files[i][0]:
					if data == files[i][1]:
						flag = 1
			if flag == 0:                                               # Den uparxei diplotypo
				conn.send('O')
				files.append([temp, data])
				files.sort()
			elif flag == 1:
				conn.send('D')                                          # Uparxei diplotypo
				conn.send('The name of the file you typed already exists.\n')
			counter = 1
			
        if not data: 
            break
            
    #came out of loop
    conns.close()
 
#now keep talking with the client
while 1:
    global x
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    conns.append([conn, addr])
    port = conn.recv(1024)
    ipport.append([addr, port])
    
    d = 'Client' + str(x)                                               # Pinakas me tous Clients kai ta antistoixa conn
    clients.append([d, conn])
    
    x = x + 1
    
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()