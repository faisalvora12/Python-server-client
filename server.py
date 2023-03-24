import socket
import sys
import thread 

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_add = socket.gethostname()

def newcon(connection,client_add):
  a = 0
  while 1:
    data = connection.recv(50)
    data1 =  data.lower() 
    print 'received "%s" from %s' % (data,client_add)
    if data1 == "hello":
      connection.sendall("Welcome")
    elif data1 == "quit":
      connection.sendall("Connection terminated")
      a = 1
      break
      connection.close()
    elif data:
      print  'sending data back to the client\n'
      connection.sendall(data)
  if a == 1:
    connection.close()

def server(port):
  serversocket.bind((socket.gethostname(), port))
  serversocket.listen(5)
  while 1:
    print '\nWaiting for a connection on port %d\n' % port
    connection,client_add = serversocket.accept()
    print 'Connection established to the client ',client_add
    thread.start_new_thread(newcon,(connection,client_add))
     

if __name__ == "__main__":
  port = sys.argv[1]
  server(int(port))
  serversocket.close()
