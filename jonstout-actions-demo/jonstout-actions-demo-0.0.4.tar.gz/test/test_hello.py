import unittest

from jonstout.actions_demo import hello_message


class TestHello(unittest.TestCase):
  def test_hello_message(self):
    testdata = [
      { 'name': "Jonathan", 'result': "Hello Jonathan." },
      { 'name': "Dave", 'result': "Hello Dave." },
      { 'name': "Snoopy", 'result': "Hello Snoopy." },
    ]
    
    for data in testdata:
      self.assertEqual(hello_message(data['name']), data['result'])

if __name__ == '__main__':
  unittest.main()
