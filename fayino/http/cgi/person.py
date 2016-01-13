"""
This module holds the class for the person. A person is someone that makes up other classes.
This class will be blank for some time but will be filled out as we go along
"""


class Person(object):
    """
    This class is used to hold the higher functions of the lower classes.
    """

    def __init__(self, foo):

        if foo != 1:
            raise ValueError('foo is not equal to 1')

    def add_person(self, set_dict):
        """
        This function adds users to the user table. It does not matter if the user is a member or a client
        :param set_dict: A formatted dict of data on the user
        :return:
        """