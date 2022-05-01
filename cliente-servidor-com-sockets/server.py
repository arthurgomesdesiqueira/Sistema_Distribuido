from socket  import *
from constCS import * #-

def simpleCalculator(firstNumber, secondNumber, op):
  try:
    firstNumber = float(firstNumber)
    secondNumber = float(secondNumber)
  except:
    return "Numbers are invalid\n"
  op = op.lower()
  if op == "add":
    return firstNumber + secondNumber
  elif op == "subtract":
    return firstNumber - secondNumber
  elif op == "divide":
    return firstNumber / secondNumber
  elif op == "multiply":
    return firstNumber * secondNumber
  else:
    return "Operation doesn't exist\n"

s = socket(AF_INET, SOCK_STREAM) 
s.bind((HOST, PORT))  #-
s.listen(1)           #-
(conn, addr) = s.accept()  # returns new socket and addr. client 
while True:                # forever
  data = conn.recv(1024)   # receive data from client
  if not data: break       # stop if client stopped
  userData = data.decode()
  arguments = userData.split(' ')

  conn.send(str.encode(str(simpleCalculator(arguments[0], arguments[1], arguments[2])))) 
conn.close()               # close the connection
