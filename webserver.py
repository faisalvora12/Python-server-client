import socket
import sys
import thread
import os.path
from os import path

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #open server socket
client_add = socket.gethostname() # get the host name 
#client_add = '127.0.0.1'  # testing local host


def badrequest():
  res = "HTTP/1.1 400 Bad Request\r\n"
  res+= "Content-Type: text/html; charset=utf-8\r\n"
  res+="\r\n"
  res+="Bad request error"
  res+= "\r\n\r\n"
  return res

def forbidden():
  res = "HTTP/1.1 403 Forbidden\r\n"
  res+= "Content-Type: text/html; charset=utf-8\r\n"
  res+="\r\n"
  res+="Forbidden file error"
  res+= "\r\n\r\n"
  return res



def newcon(connection,client_add): # new connection function
  while 1:
    request = connection.recv(10240).decode()#get request from the browser/client
    #print(request)
    try:
      headers = request.split("\n")
      if len(request) > 0:
        requesthead,requestbody = request.split('\r\n',1)
        requesthead = requesthead.splitlines()
        requestheadline = requesthead[0]
        print(requestheadline)
        method, filename, ver = requestheadline.split(' ', 3)
        if method != "GET":  # check if the method is get or else return badrequest
          res = badrequest()
          connection.sendall(res.encode()) 
          connection.close()
          break

        if filename == '/': #change the name of default file to index.html
          filename = '/index.html'
     
        if ver !='HTTP/1.1' and ver!='HTTP/1.0': #check the version of request
          res = 'HTTP/1.0 505 HTTP Version Not Supported\r\n\r\n'# Content-Type:text/html;enxoding=utf8 \n Connection:close \n'
          connection.sendall(res)

        else: # if the version is correct
          ext = filename.split(".")[1]
          if path.exists(filename[1:]):
            if os.access(filename[1:],os.R_OK) == False:
              res = forbidden()
              connection.sendall(res.encode())
              connection.close()
              break             
          try:
            res = "HTTP/1.1 200 OK\r\n"
            if ext == "html": #if it is a text file
              html_file = open(filename[1:], 'r')
              body = html_file.read()
              html_file.close()
              res+= "Content-Type: text/html; charset=utf-8\r\n"
              res+= "\r\n"
              res+= body
              res+= "\r\n\r\n"
              connection.sendall(res.encode()) 
            elif ext=="jpg": # if it is a jpg file
              image = open(filename[1:],'rb')
              imgbytes = image.read()
              image.close()
              res+="Content-Type: image/jpeg\r\n Accept-Ranges: bytes\r\n"
              res+= "\r\n"
              res+= imgbytes
              res+= "\r\n\r\n"
              connection.sendall(res)
            elif ext=="gif": # if it is a gif file
              image = open(filename[1:],'rb')
              imgbytes = image.read()
              image.close()
              res+="Content-Type: image/gif\r\n Accept-Ranges: bytes\r\n"
              res+= "\r\n"
              res+= imgbytes
              res+= "\r\n\r\n"
              connection.sendall(res)  
          except IOError: #if the file is not found
            res = "HTTP/1.1 404 Not Found\r\n"
            res+= "Content-Type: text/html; charset=utf-8\r\n"
            res+="\r\n"
            res+="File not found"
            res+= "\r\n\r\n"
            connection.sendall(res.encode()) 
    except:
      res = badrequest()
      connection.sendall(res.encode()) 

    connection.close()
    break


def server(port):
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_socket.bind((client_add, port))
  server_socket.listen(1)
  print('\nListening on port %s ...\n' % port)    
  while 1:
    print '\nWaiting for a connection on port %d\n' % port
    connection,client_addr = server_socket.accept()
    print 'Connection establesh to the client',client_add
    thread.start_new_thread(newcon,(connection,client_add))

if __name__=="__main__":
  port = sys.argv[1] #get the port from commandline
  server(int(port)) 
  server_socket.close() #close the server socket
