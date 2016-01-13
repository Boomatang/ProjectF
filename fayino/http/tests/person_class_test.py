import unittest
from cgi.person import Person


class PersonClassTest(unittest.TestCase):
    def testInsufficientArgs(self):
        foo = 0
        self.failUnlessRaises(ValueError, Person, foo)

if __name__ == '__main__':
    unittest.main()