import random
import socket
import threading
import time
from _thread import *
from threading import Thread
from multiprocessing import Process, Queue

# Global variables: host, ports, sockets
host = "127.0.0.1"
port1 = 5500
port = [port1 + i for i in range(3)]
sockets = []

class VirtualMachine:
  def __init__(self, id):
    self.id = id
    self.listening_socket = None
    self.connections = []
    self.clock_rate = random.randint(1, 7)
    self.clock = 0
    self.incoming_messages = Queue()
    self.outgoing_messages = []
    self.connections = []
    self.log_file = None
    self.queue_size = 0

  def run(self):
    # Create log file
    self.log_file = open(f"logs/{self.id:n}.txt", "w")
    self.connect(host)

    while True:
      # Clock rate cycle - sleep until the next clock tick
      time.sleep(1 / self.clock_rate)

      # Test logging works
      # self.log(f"I am at time {self.clock}")

      # Process incoming messages
      if self.incoming_messages.empty():
        generator = random.randint(1, 11)
        message = self.clock
        if generator == 1:
          # Send message to first other machine
          self.clock += 1
          self.send_message(0, message)
        elif generator == 2:
          # Send message to first other machine
          self.clock += 1
          self.send_message(1, message)
        elif generator == 3:
          # Send message to both other machines
          self.clock += 1
          self.send_message(0, message)
          self.send_message(1, message)
        else: 
          self.clock += 1
          # Log internal event
          self.log(f"Internal event value {generator} at global time {time.ctime(time.time())} and logical clock time {self.clock}.")
      else:
        message = self.incoming_messages.get()
        self.queue_size -= 1
        # print(message)

        # Log info
        self.log(f"Received message \"{message}\" at global time {time.ctime(time.time())} and logical clock time {self.clock}. Message queue length: {self.queue_size}")
        # Update clock (message receive event means need to consider max rule, not just clock + 1)
        self.update_clock(self.clock)

  def send_message(self, id, message):
    if len(self.connections) > 1:
      self.connections[id].send(str(message).encode('ascii'))
      print(f"Sending message {self.clock:n} from machine {self.id:n} to other machine #{id+1:n}.")
      self.log(f"Sending message \"{self.clock:n}\" at global time {time.ctime(time.time())} and logical clock time {self.clock} from machine {self.id:n} to other machine #{id+1:n}.")
    unit_test_check = (self.clock, self.id, id+1)
    return unit_test_check

  def receive_message(self, connection):
    # Constantly listen for messages
    while True:
      data = connection.recv(1024).decode('ascii')
      self.incoming_messages.put(data)
      self.queue_size += 1

  def connect(self, host):
    for machine_id in range(3):
      if machine_id != self.id:
        # Connection from current machine to other socket.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port[machine_id]))
        self.connections.append(s)

  def update_clock(self, timestamp):
    self.clock = max(self.clock, timestamp) + 1

  def log(self, message):
    self.log_file.write(f"{message}\n")
    self.log_file.flush()

  def init_machine(self, config):
    HOST = str(config[0])
    PORT = int(config[1])

    # Create socket for receiving messages
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    while True:
      listening_socket, addr = s.accept()
      start_new_thread(VirtualMachine.receive_message, (self, listening_socket, ))

  def machine(self, host, port):
    listening_thread = Thread(target = self.init_machine, args = ([host, port], ))
    listening_thread.start() 
    # Add delay to initialize the server - side logic on all processes
    time.sleep(0.5)
    # Start thread for machine functionality, i.e. sending and receiving messages
    sending_thread = Thread(target = self.run, args = ())
    sending_thread.start()


if __name__ == '__main__':
  vm = []
  p = []

  # Initialize 3 machines
  for i in range(3):
    vm.append(VirtualMachine(i))
  
  time.sleep(0.5)

  # Start a process for each machine
  for i in range(3):
    p.append(Process(target = VirtualMachine.machine, args = (vm[i], host, port[i])))
    p[i].start()

  # Join the machines
  for i in range(3):
    p[i].join()
