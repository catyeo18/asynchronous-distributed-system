import unittest

from three_machines import VirtualMachine


class UnitTests(unittest.TestCase):
  """
  Test for two main components of three_machines.py:
  1) messages are sending properly 
  2) the clock is updating properly

  We are unit testing the function logic, not whether the client-socket
  connections are working, so we are isolating out the functions from the
  main file here for unit testing.
  """

  # This checks that send_message returns the right
  # message value, machine sender id, machine receiver id
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