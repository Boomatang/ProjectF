import datetime
import gc

import pymysql


def connection():
    """
    Use to make a connection to the SQL database

    :return:
    """
    conn = pymysql.connect(host="localhost",
                           user="root",
                           db="fayino")
    c = conn.cursor()
    return c, conn


def conn_close(c, conn):
    """
    Use to close and commit the trans action with the sql database
    Will do garbage collection too
    :param c:
    :param conn:
    :return:
    """
    conn.commit()
    c.close()
    conn.close()
    gc.collect()


def check_new_username_and_email(username, email):
    c, conn = connection()

    sql = """SELECT userName, loginEmail
    FROM person_TBL
    WHERE userName = %s
            AND loginEmail = %s"""

    data = (username, email)

    info = c.execute(sql, data)

    if info == 0:
        output = True
    else:
        output = False

    conn_close(c, conn)
    return output


def sign_up_user(user):
    c, conn = connection()

    sql = u'INSERT INTO person_TBL' \
          u'(personID, userName, loginEmail, password, acceptTErms, joinDate)' \
          u'VALUES (%s, %s, %s, %s, %s, %s)'

    acceptDate = datetime.date.today()
    acceptDate = str(acceptDate.year) + "-" + str(acceptDate.month) + "-" + str(acceptDate.day)

    joinDate = datetime.date.today()
    joinDate = str(joinDate.year) + "-" + str(joinDate.month) + "-" + str(joinDate.day)

    sql2 = u'SELECT MAX(personID)' \
           u'FROM person_TBL'

    a = c.execute(sql2)

    personID = c.fetchone()
    personID = personID[0] + 1

    data = (personID, user[0], user[1], user[2], acceptDate, joinDate)

    c.execute(sql, data)
    conn_close(c, conn)

    return personID


def company_code_check(code):
    """
    Check to see if a company code doesnt exists already in the data base.

    :param code: The short code is which is to be checked
    :return output: a Boolean value
    """
    # fixme This should all so check to make the code tied to the usr not the full data base
    c, conn = connection()

    sql = u'SELECT companyCode ' \
          u'FROM company_TBL ' \
          u'WHERE companyCode = %s'

    data = (code,)

    a = c.execute(sql, data)

    if a >= 1:
        output = False

    else:
        output = True

    conn_close(c, conn)

    return output


def next_companyID():
    c, conn = connection()

    sql = u'SELECT MAX(companyID)' \
          u'FROM company_TBL'

    a = c.execute(sql)

    value = c.fetchone()
    if value[0] is None:
        companyID = 1
    else:
        companyID = value[0] + 1

    conn_close(c, conn)
    return companyID


def enter_company_detail(company):
    """
    Enter a company name into the system
    The codes should be checked first.
    :param company: List of values from a form that has been filled in
    :return:
    """
    c, conn = connection()
    sql = u'INSERT INTO company_TBL ' \
          u'(companyID, companyName, companyCode, companyType, companyOwer, companyAdmin)' \
          u'VALUES (%s, %s, %s, %s, %s, %s)'

    data = (company[4], company[0], company[1], company[2], company[3], company[3])

    c.execute(sql, data)
    conn_close(c, conn)


def link_user_company(userID, companyID):
    """
    Enters employees to be linked with their company
    :param userID: Integer length 11 or less
    :param companyID: Integer length 11 or less
    :return:
    """

    c, conn = connection()
    sql = u'INSERT INTO employee_TBL (personID, companyID)' \
          u'VALUES (%s, %s)'

    data = (userID, companyID)

    c.execute(sql, data)
    conn_close(c, conn)


# TODO these functions can be writen better
def get_uesr_details(userID):
    sql = 'SELECT * ' \
          'FROM person_TBL ' \
          'WHERE personID = %s'

    data = (userID,)

    c, conn = connection()
    c.execute(sql, data)

    values = c.fetchone()

    if values[0] is not None:
        output = values

    else:
        output = ('error',)

    return output


# TODO these functions can be writen better
def get_company_details(companyID):
    sql = 'SELECT * ' \
          'FROM company_TBL ' \
          'WHERE companyID = %s'

    data = (companyID,)

    c, conn = connection()
    c.execute(sql, data)

    values = c.fetchone()

    if values[0] is not None:
        output = values

    else:
        output = ('error',)

    return output


def get_user_login_details(email):
    sql = 'SELECT personID, password ' \
          'FROM person_TBL ' \
          'WHERE loginEmail = %s'

    data = (email,)

    c, conn = connection()
    c.execute(sql, data)

    values = c.fetchone()

    if values[0] is not None:
        output = values

    else:
        output = ('error',)

    conn_close(c, conn)
    return output


def create_job(values=[]):
    """
    Create a job in the database, only basic information is add at this time and in the future more has to be added.
    This function will break not all 4 values are passed in.
    :param values: List of up to 4 values passed in as strings. 2 is the minimum required.
    """
    # FIXME This function will break not all 4 values are passed in.
    current_year = datetime.date.today()
    current_year = current_year.year

    next_number = next_job_number(current_year)

    sql = u'INSERT INTO job_TBL ' \
          u'(jobIDyear, jobIDnum, title, description, entryDate, pTime, pCost)' \
          u'VALUES (%s, %s, %s, %s, NOW(), %s, %s)'

    hm = values[3]
    h, m = hm.split(':')

    ptime = (int(m) + (int(h) * 60)) * 60

    data = (current_year, next_number, values[0], values[1], ptime, float(values[2]))

    c, conn = connection()

    c.execute(sql, data)

    conn_close(c, conn)

    job_number = (current_year, next_number)

    return job_number


def next_job_number(current_year):
    """
    Use to find the next job number for the for the year in question
    :param current_year: In the format of a INT of length 4
    :return: INT of unknown length
    """
    sql = u'SELECT MAX(jobIDnum) ' \
          u'FROM job_TBL ' \
          u'WHERE jobIDyear = %s'

    data = (current_year,)

    c, conn = connection()

    c.execute(sql, data)

    value = c.fetchone()

    if value[0] is not None:
        output = int(value[0]) + 1
    else:
        output = 1

    conn_close(c, conn)

    return output


def get_job_details(job_number):

    """
    Used to bring all the information about the job number from the database
    :param job_number: requires a tuple of 2 integers that are existing job number keys
    :return: a set record from the database
    """
    # TODO add in a fix to check to see if the input keys are existing in the database.

    sql = u'SELECT title, description, entryDate, pTime, pCost ' \
          u'FROM job_TBL ' \
          u'WHERE jobIDyear = %s ' \
          u'AND jobIDnum = %s'

    data = (job_number[0], job_number[1])

    c, conn = connection()

    c.execute(sql, data)

    value = c.fetchone()

    if value[0] is not None:
        output = value

    else:
        output = None

    conn_close(c, conn)

    return output


def get_all_job_numbers():

    """
    This function will return a list of all the job numbers that is currently in be database
    """
    # TODO this function should only get the results for the company that is logged in
    sql = u'SELECT jobIDyear, jobIDnum ' \
          u'FROM job_TBL'

    data = ()

    c, conn = connection()

    c.execute(sql, data)

    values = c.fetchall()

    if len(values) > 1:
        output = values
    else:
        output = 'List size error'

    conn_close(c, conn)

    return output


def get_sudo_username():
    """
    Gets the default username for the adding of user to the company
    """

    sql = u'SELECT MAX(personID) ' \
          u'FROM person_TBL '
    c, conn = connection()

    c.execute(sql)

    value = c.fetchone()

    if value is not None:
        number = value[0]
        number += 1

        name = 'UserName' + str(number)

    else:
        name = 'UserName'

    return name


def add_user(data_set):
    """
    Make a new user. This would be do by the admin for the company
    :param data_set:
    """

    c, conn = connection()

    joinDate = datetime.date.today()
    joinDate = str(joinDate.year) + "-" + str(joinDate.month) + "-" + str(joinDate.day)

    sql2 = u'SELECT MAX(personID) ' \
           u'FROM person_TBL'

    c.execute(sql2)

    personID = c.fetchone()
    personID = personID[0] + 1

    sql = u'INSERT INTO person_TBL ' \
          u'(personID, userName, loginEmail, fName, lName, password, ' \
          u'acceptTErms, joinDate) ' \
          u'VALUES (%s, %s, %s, %s, %s, %s, %s)'

    data = (str(personID), str(data_set[0]), str(data_set[1]), str(data_set[2]), str(data_set[3]), str(data_set[4]), str(joinDate), str(joinDate))
    c.execute(sql, data)
    conn_close(c, conn)
