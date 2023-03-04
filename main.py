from datetime import datetime
from multiprocessing import Process
import os
import random
import socket
from _thread import *
import time
import threading
from threading import Thread

localhost = "127.0.0.1"
port1 = 2056
port2 = 3056
port3 = 4056

def consumer(conn):
  print("consumer accepted connection" + str(conn) + "\n")
  msg_queue = []
  sleepVal = 0.900

  while True:
    time.sleep(sleepVal)
    data = conn.recv(1024)
    # print("msg received\n")
    dataVal = data.decode('ascii')
    print("msg received:", dataVal)

    # test writing to log file
    filename = 'logs/' + str(conn.getsockname()[1]) + '.txt'
    with open(filename, 'a') as f:
      f.write("msg received: " + dataVal + "\n")

    msg_queue.append(dataVal)


def producer(portVal):
  host = "127.0.0.1"
  port = int(portVal)
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sleepVal = 0.500 

  try:
    s.connect((host, port))
    print("client-side connection success to port val:" + str(portVal) + "\n")

    while True:
      codeVal = str(code)
      time.sleep(sleepVal) 
      s.send(codeVal.encode('ascii'))
      print("msg sent", codeVal)
  except socket.error as e:
    print("error connecting producer: %s" % e)


"""
These 2 functions initialize a machine
"""
def init_machine(config):
  HOST = str(config[0])
  PORT = int(config[1])
  print("starting server| port val:", PORT)

  # create log file
  filename = 'logs/' + str(PORT) + '.txt'
  with open(filename, 'w') as f:
    pass

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((HOST, PORT))
  s.listen()
  while True:
    conn, addr = s.accept()
    start_new_thread(consumer, (conn, ))

def machine(config):
  global code

  config.append(os.getpid())
  # print(config)

  init_thread = Thread(target = init_machine, args = (config, ))
  init_thread.start() 
  # add delay to initialize the server - side logic on all processes
  time.sleep(5)
  # extensible to multiple producers
  prod_thread = Thread(target = producer, args = (config[2], ))
  prod_thread.start()

  while True:
    code = random.randint(1, 10)


if __name__ == '__main__':
  config1 = [localhost, port1, port2, ]
  p1 = Process(target = machine, args = (config1, ))
  config2 = [localhost, port2, port3]
  p2 = Process(target = machine, args = (config2, ))
  config3 = [localhost, port3, port1]
  p3 = Process(target = machine, args = (config3, ))

  p1.start()
  p2.start()
  p3.start()

  p1.join()
  p2.join()
  p3.join()
