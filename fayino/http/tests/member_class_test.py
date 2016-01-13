import unittest
from cgi.member import Member


class PersonClassTest(unittest.TestCase):
    def testInsufficientArgs(self):
        foo = 0
        self.failUnlessRaises(ValueError, Member, foo)

    # TODO make test for add_to_member_table
    # TODO make test for create_member

if __name__ == '__main__':
    unittest.main()