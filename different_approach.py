import queue
import random
import socket
import threading
import time


class VirtualMachine:
  def __init__(self, name, clock_rate):
    self.name = name
    self.clock_rate = clock_rate
    self.clock = 0
    self.incoming_messages = queue.Queue()
    self.outgoing_messages = []
    self.connections = []
    self.log_file = open(f"logs/{name}.txt", "w")

  def run(self):
    while True:
      # Perform a limited number of instructions based on clock rate
      for i in range(self.clock_rate):
        # Test logging works
        self.log(f"I am at time {self.clock}")

        # TO CHANGE: currently only incrementing
        # Update logical clock based on local events
        self.clock += 1

        # Process incoming messages
        if self.incoming_messages.empty():
          generator = random.randint(1, 11)
          if generator == 1:
            # TODO: send to a machine
            # need to figure out a way to direct which machine to send_message to 
            pass
          # TODO: generator = 2, etc cases
        else:
          while not self.incoming_messages.empty():
            message = self.incoming_messages.get()
            print(message)
            # Log info
            self.log(f"Received message {message} of length {str(len(message))} at global time {time.time()} and logical clock time {self.clock}")
            # Update clock
            self.update_clock(message["timestamp"])
            # TODO: NEED TO REMOVE MESSAGE FROM QUEUE

        # Send outgoing messages
        for message in self.outgoing_messages:
          self.log(f"Sending message {message} at time {self.clock}")
          message["timestamp"] = self.clock
          self.send_message(message)

        self.outgoing_messages = []

      # Clock rate cycle - sleep until the next clock tick
      time.sleep(1 / self.clock_rate)

  def send_message(self, message):
    for connection in self.connections:
      connection.send(str(message).encode('ascii'))

  def receive_message(self, connection):
    while True:
      data = connection.recv(1024).decode('ascii')
      self.incoming_messages.put(data)

  def connect(self, ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    self.connections.append(s)
    threading.Thread(target=self.receive_message, args=(s,)).start()

  def update_clock(self, timestamp):
    self.clock = max(self.clock, timestamp) + 1

  def log(self, message):
    self.log_file.write(f"{message}\n")
    self.log_file.flush()


if __name__ == '__main__':
  # Initialize virtual machines
  vm1 = VirtualMachine("vm1", random.randint(1, 7))
  vm2 = VirtualMachine("vm2", random.randint(1, 7))
  vm3 = VirtualMachine("vm3", random.randint(1, 7))

  # Start up servers
  s0 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s0.bind(("127.0.0.1", 5550))
  s0.listen()
  s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s1.bind(("127.0.0.1", 5551))
  s1.listen()
  s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s2.bind(("127.0.0.1", 5552))
  s2.listen()

  # Connect virtual machines
  vm1.connect("127.0.0.1", 5551)
  vm1.connect("127.0.0.1", 5552)
  vm2.connect("127.0.0.1", 5550)
  vm2.connect("127.0.0.1", 5552)
  vm3.connect("127.0.0.1", 5550)
  vm3.connect("127.0.0.1", 5551)

  # Start virtual machines
  threading.Thread(target=vm1.run).start()
  threading.Thread(target=vm2.run).start()
  threading.Thread(target=vm3.run).start()