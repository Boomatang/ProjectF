import unittest
from cgi.member import Member


class PersonClassTest(unittest.TestCase):
    def member_exist(self):
        m = Member()
        self.assertIsNotNone(m)

    # TODO make test for add_to_member_table
    # TODO make test for create_member

if __name__ == '__main__':
    unittest.main()