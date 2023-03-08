import unittest

from three_machines import VirtualMachine


class UnitTests(unittest.TestCase):
  """
  Test for the main components of three_machines.py:
  1. Initialization
  2. Sending messages
  3. Updating clock
  """

  def test_constructor(self):
    vm = VirtualMachine(0)
    self.assertEqual(vm.id, 0)
    self.assertEqual(vm.listening_socket, None)
    assert vm.clock_rate >= 1 and vm.clock_rate <= 7
    self.assertEqual(vm.clock, 0)
    self.assertEqual(vm.incoming_messages.empty(), True)
    self.assertEqual(vm.outgoing_messages, [])
    self.assertEqual(vm.connections, [])
    self.assertEqual(vm.log_file, None)
    self.assertEqual(vm.queue_size, 0)

  def test_messages(self):
    vm1 = VirtualMachine(0)
    output = vm1.send_message(0, "")
    self.assertEqual(output[0], 0) # message value
    self.assertEqual(output[1], 0) # machine sender id
    self.assertEqual(output[2], 1) # machine receiver id

  def test_update_clock(self):
    vm1 = VirtualMachine(0)
    self.assertEqual(vm1.clock, 0)
    vm1.update_clock(2)
    self.assertEqual(vm1.clock, 3)
    vm1.update_clock(5)
    self.assertEqual(vm1.clock, 6)


if __name__ == '__main__':
  print("Unit tests running!")
  unittest.main()