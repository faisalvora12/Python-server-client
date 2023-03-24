import socket
import sys

def client(host,port):
  server_address = (host, port)
  # Connect the socket to the port where the server is listening
  socketcon = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  #socketcon.setblocking(0)
  print 'connecting to %s port %s' % server_address
  socketcon.connect(server_address)

  while 1:
      #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      #print 'connecting to %s port %s' % server_address
      #socketcon.connect(server_address)
      message = raw_input("enter a message\n") 
      socketcon.sendall(message)

      # Look for the response
      data = socketcon.recv(1024)
      print 'Server responded with "%s" \n' % data
      if data == "Connection terminated":
        break  
  while 1:
    print "the connection was terminated. \n"
    try:
      inputo = raw_input("Enter 1 to exit the program\n")    
      if int(inputo) == 1:
        print "Thank you for being an amazing client!"
        break
    except ValueError:
      print "please enter a number"
  socketcon.close()
  

if __name__ == "__main__":
  host = sys.argv[1]
  port = sys.argv[2]
  client(host,int(port))
