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

    data = (email)

    c, conn = connection()
    c.execute(sql, data)

    values = c.fetchone()

    if values[0] is not None:
        output = values

    else:
        output = ('error',)

    return output