import socket
import sys
import threading

def usage():
	print("Syntax: python echoclient.py <host> <port>")
	print("Sample: python echoclient.py 127.0.0.1 1234")
	sys.exit(1)

def RcvMsg(ClientSocket):
	while True:
		data = ClientSocket.recv(1024)
		if not data:
			break
		print(data)

def RunClient(ClientSocket):
	t=threading.Thread(target=RcvMsg,args=(ClientSocket,))
	t.daemon=True
	t.start()

	while True:
		data=raw_input()
		ClientSocket.send(data)

if __name__ == '__main__':

	if len(sys.argv)!=3:
		usage()

	host = sys.argv[1]
	port = int(sys.argv[2])
	ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ClientSocket.connect((host,port))
	RunClient(ClientSocket)
