import datetime
import gc
import string
from random import randint, choice

import pymysql

master = 'login_master_files'


def connection(schema="fayino"):
    """
    Use to make a connection to the SQL database

    :param schema: The schema in which the user connects
    :return:
    """
    conn = pymysql.connect(host="localhost",
                           user="root",
                           db=schema)
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


def add_user_to_company_member_tbl(login_details, username='username'):

    get_user_sql = u'SELECT person_ID, join_date, accept_terms ' \
                   u'FROM person_TBL ' \
                   u'WHERE person_ID = %s'

    insert_user_sql = u'INSERT INTO member_TBL (' \
                      u'login_master_ID, join_date, accept_terms, username) ' \
                      u'VALUES (%s, %s, %s, %s)'

    if verify_user_company_schema(login_details):
        get_user_data = (login_details['user_ID'],)

        mc, mconn = connection(master)
        try:
            mc.execute(get_user_sql, get_user_data)

            data = mc.fetchone()
        finally:
            conn_close(mc, mconn)

        if data is not None:
            insert_user_data = (data[0], data[1], data[2], username)
            c, conn = connection(login_details['company_schema'])
            try:
                c.execute(insert_user_sql, insert_user_data)
            finally:
                conn_close(c, conn)


def create_company_schema_tables(schema_name=None):
    """
    This function will make the basic schema set up.
    It should make all the tables that is required at the time of a user signing up
    :param schema_name: schema that has been assigned to the company a user has set up
    """
    top = [u'SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;',
           u'SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;',
           u"SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';"]

    bottom = [u'SET SQL_MODE=@OLD_SQL_MODE;',
              u'SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;',
              u'SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;']

    member_tbl = u'CREATE TABLE IF NOT EXISTS `member_TBL` ( ' \
                 u'`person_ID` INT(11) NOT NULL, ' \
                 u'`first_name` VARCHAR(45) NULL DEFAULT NULL, ' \
                 u'`last_name` VARCHAR(45) NULL DEFAULT NULL, ' \
                 u'`username` VARCHAR(100) NULL DEFAULT NULL, ' \
                 u'`DOB` DATE NULL DEFAULT NULL, ' \
                 u'`joinDate` DATE NULL DEFAULT NULL, ' \
                 u'`accept_terms` DATE NOT NULL, ' \
                 u'`login_master_ID` INT(11) NOT NULL, ' \
                 u'PRIMARY KEY (`person_ID`), ' \
                 u'UNIQUE INDEX `person_ID_UNIQUE` (`person_ID` ASC), ' \
                 u'UNIQUE INDEX `user_name_UNIQUE` (`username` ASC)) ' \
                 u'ENGINE = InnoDB ' \
                 u'DEFAULT CHARACTER SET = utf8;'

    c, conn = connection(schema_name)

    try:

        for line in top:
            c.execute(line)
            conn.commit()

        c.execute(member_tbl)
        conn.commit()

        for line in bottom:
            c.execute(line)
            conn.commit()

    finally:
        conn_close(c, conn)


def verify_user_company_schema(login_details):
    """
    This function will check that the user Id and company ID all match up to the schema in question.
    :return: output should be True or False, Default is False
    :param login_details: a dict of values used to verify details
    """
    output = False

    user_sql = u'SELECT company_ID ' \
               u'FROM person_TBL ' \
               u'WHERE person_ID = %s;'

    company_sql = u'SELECT company_schema ' \
                  u'FROM company_TBL ' \
                  u'WHERE company_ID = %s'

    user_data = (login_details['user_ID'],)

    c, conn = connection(master)
    try:
        c.execute(user_sql, user_data)

        user = c.fetchone()

        if user is not None:
            company_ID = user[0]

            if company_ID == login_details['company_ID']:
                company_data = (company_ID,)
                c.execute(company_sql, company_data)
                company = c.fetchone()

                if company is not None:
                    company_schema = company[0]

                    if company_schema == login_details['company_schema']:
                        output = True
    finally:
        conn_close(c, conn)

    return output


def create_company_schema(company_schema=None):
    """
    Create a new schema in the database that user can now use.
    All company details will be set up in this schema.
    :param company_schema: String set in the master database
    """
    sql = 'CREATE SCHEMA IF NOT EXISTS ' + company_schema + ';'

    c, conn = connection(master)
    try:
        c.execute(sql)
    finally:
        conn_close(c, conn)


def check_new_username_and_email(username, email):
    """

    :param username:
    :param email:
    :return:
    """
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
    """
    Enters a new user in to the main data base table.
    :param user: This is a tuple of values that comes form a sign up form.
    :return: The ID used as a primary Key in the tables
    """
    # FIXME there is nothing stopping a user from entering the same password and email
    c, conn = connection(master)

    sql = u'INSERT INTO person_TBL' \
          u'(login_email, password, accept_terms, join_date)' \
          u'VALUES (%s, %s, %s, %s)'

    accept_date = datetime.date.today()
    accept_date = str(accept_date.year) + "-" + str(accept_date.month) + "-" + str(accept_date.day)

    join_date = datetime.date.today()
    join_date = str(join_date.year) + "-" + str(join_date.month) + "-" + str(join_date.day)

    data = (user[1], user[2], accept_date, join_date)

    c.execute(sql, data)
    conn.commit()

    person_ID_sql = u'SELECT person_ID ' \
                    u'FROM person_TBL ' \
                    u'WHERE login_email = %s ' \
                    u'AND password = %s'

    person_ID_data = (user[1], user[2])

    c.execute(person_ID_sql, person_ID_data)
    values = c.fetchone()

    if values is not None:
        person_ID = values[0]

    else:
        person_ID = 'Error'

    conn_close(c, conn)

    return person_ID


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

    all_char = string.ascii_letters + string.digits
    company_schema = "zb_" + "".join(choice(all_char) for x in range(randint(7, 17)))

    set_up_date = datetime.date.today()
    set_up_date = str(set_up_date.year) + "-" + str(set_up_date.month) + "-" + str(set_up_date.day)

    c, conn = connection(master)
    sql = u'INSERT INTO company_TBL ' \
          u'(company_name, set_up_date, company_schema) ' \
          u'VALUES (%s, %s, %s)'

    data = (company, set_up_date, company_schema)

    c.execute(sql, data)
    conn.commit()

    company_ID_sql = u'SELECT company_ID ' \
                     u'FROM company_TBL ' \
                     u'WHERE company_schema = %s'

    company_ID_data = (company_schema,)

    c.execute(company_ID_sql, company_ID_data)

    value = c.fetchone()
    if value is not None:
        company_ID = value[0]
    else:
        company_ID = 'Error'

    conn_close(c, conn)

    return company_ID, company_schema


def link_user_company(userID, companyID):
    """
    Enters employees to be linked with their company
    :param userID: Integer length 11 or less
    :param companyID: Integer length 11 or less
    :return:
    """

    c, conn = connection(master)
    sql = u'UPDATE person_TBL ' \
          u'SET company_ID = %s ' \
          u'WHERE person_ID = %s'

    data = (companyID, userID)

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

    insert_sql = u'INSERT INTO person_TBL ' \
                 u'(personID, userName, loginEmail, password, ' \
                 u'acceptTErms, joinDate) ' \
                 u'VALUES (%s, %s, %s, %s, %s, %s)'

    insert_data = (personID, data_set[0], data_set[1], data_set[4], joinDate, joinDate)
    c.execute(insert_sql, insert_data)
    conn.commit()

    update_sql = u'UPDATE person_TBL ' \
                 u'SET fName = %s,' \
                 u'lName = %s ' \
                 u'WHERE personId = %s;'

    update_data = (data_set[2], data_set[3], personID)

    c.execute(update_sql, update_data)

    conn_close(c, conn)

    return personID
