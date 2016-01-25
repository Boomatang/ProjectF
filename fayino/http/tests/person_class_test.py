import unittest
from cgi.person import Person


class PersonClassTest(unittest.TestCase):
    def testInsufficientArgs(self):
        foo = 0
        bar = None
        self.failUnlessRaises(ValueError, Person, foo, bar)

if __name__ == '__main__':
    unittest.main()