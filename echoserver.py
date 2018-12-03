import socket
import sys
import threading

session=[]

def usage():
	print("Syntax: python echoserver.py <port> [-b]")
	print("Sample: python echoserver.py 1234 -b")

def RcvMsgS(ClientSocket,(host,port),OPTION_B):
	while True:
		data=ClientSocket.recv(1024).decode()
		if not data:
			break
		elif OPTION_B==True:
			print(data)
			for cliorder in session:
				cliorder.send(data.encode())
				session.pop(0)
		else:
			print(data)
			ClientSocket.send(data.encode())
	
	ClientSocket.close()

def RunServer(ServerSocket,OPTION_B):
	while OPTION_B:
		(ClientSocket,(host,port))=ServerSocket.accept()
		session.append(ClientSocket)
		t=threading.Thread(target=RcvMsgS,args=(ClientSocket,(host,port),OPTION_B))
		t.start()

	while not OPTION_B:
		(ClientSocket,(host,port))=ServerSocket.accept()
		t=threading.Thread(target=RcvMsgS,args=(ClientSocket,(host,port),OPTION_B))
		t.start()

if __name__=='__main__':
	OPTION_B=False
	host='localhost'
	port=int(sys.argv[1])
	if len(sys.argv[1])==3 and sys.argv[2]=='-b':
		OPTION_B=True

	elif len(sys.argv)!=2 and len(sys.argv)!=3:
		usage()
		sys.exit()

	ServerSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	ServerSocket.bind((host,port))
	ServerSocket.listen(1)
	RunServer(ServerSocket,OPTION_B)
