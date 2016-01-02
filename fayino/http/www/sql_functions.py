import datetime
import gc
import string
from random import randint, choice
import time

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


def get_company_person_ID(master_ID, schema=None):
    """
    Get the ID of the company member that is logging in
    :type schema: object
    :type master_ID: object
    """

    output = None

    sql = u'SELECT person_ID ' \
          u'FROM member_TBL ' \
          u'WHERE login_master_ID = %s'

    data = (master_ID,)

    c, conn = connection(schema)

    try:
        c.execute(sql, data)

        value = c.fetchone()

        if value is not None:
            output = value[0]
    finally:
        conn_close(c, conn)

    return output


def get_company_schema(company_ID=None):
    """
    Get the value of the company schema
    """
    output = None

    sql = u'SELECT company_schema ' \
          u'FROM company_TBL ' \
          u'WHERE company_ID = %s'

    data = (company_ID,)

    c, conn = connection(master)

    try:
        c.execute(sql, data)
        value = c.fetchone()

        if value is not None:
            output = value[0]
    finally:
        conn_close(c, conn)

    return output


def add_user_to_company_member_tbl(login_details, username='username'):
    """
    Used to copy the user details from the master into the company schema.
    Not all details are copied over.
    :param login_details:
    :param username:
    """
    output = None

    get_user_sql = u'SELECT person_ID, join_date, accept_terms, login_email ' \
                   u'FROM person_TBL ' \
                   u'WHERE person_ID = %s'

    insert_user_sql = u'INSERT INTO member_TBL (' \
                      u'login_master_ID, join_date, accept_terms, username) ' \
                      u'VALUES (%s, %s, %s, %s)'

    add_email = u'INSERT INTO email_TBL ' \
                u'(`email_address`, `main`, `person_ID`) ' \
                u'VALUES (%s, 1, %s)'

    get_user_ID_sql = u'SELECT person_ID ' \
                      u'FROM member_TBL ' \
                      u'WHERE login_master_ID = %s'

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
            get_user_ID_data = (data[0],)

            c, conn = connection(login_details['company_schema'])
            try:
                c.execute(insert_user_sql, insert_user_data)
                conn.commit()

                c.execute(get_user_ID_sql, get_user_ID_data)
                value = c.fetchone()

                if value is not None:
                    output = value[0]

                email_data = (data[3], output)
                c.execute(add_email, email_data)

            finally:
                conn_close(c, conn)
    return output


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
                 u'`person_ID` INT(11) AUTO_INCREMENT NOT NULL, ' \
                 u'`first_name` VARCHAR(45) NULL DEFAULT NULL, ' \
                 u'`last_name` VARCHAR(45) NULL DEFAULT NULL, ' \
                 u'`username` VARCHAR(100) NULL DEFAULT NULL, ' \
                 u'`DOB` DATE NULL DEFAULT NULL, ' \
                 u'`join_date` DATE NULL DEFAULT NULL, ' \
                 u'`accept_terms` DATE NOT NULL, ' \
                 u'`login_master_ID` INT(11) NOT NULL, ' \
                 u'PRIMARY KEY (`person_ID`), ' \
                 u'UNIQUE INDEX `person_ID_UNIQUE` (`person_ID` ASC), ' \
                 u'UNIQUE INDEX `login_master_ID_UNIQUE` (`login_master_ID` ASC),' \
                 u'UNIQUE INDEX `user_name_UNIQUE` (`username` ASC)) ' \
                 u'ENGINE = InnoDB ' \
                 u'DEFAULT CHARACTER SET = utf8;'

    job_tbl = u'CREATE TABLE IF NOT EXISTS `job_TBL` (' \
              u'`job_ID_year` INT(4) NOT NULL, ' \
              u'`job_ID_number` INT(6) NOT NULL, ' \
              u'`title` VARCHAR(150) NOT NULL, ' \
              u'`description` VARCHAR(1000) NULL DEFAULT NULL, ' \
              u'`entry_date` DATE NOT NULL, ' \
              u'`quoted_time` INT(11) NULL DEFAULT NULL, ' \
              u'`quoted_cost` FLOAT(10,2) NULL DEFAULT NULL, ' \
              u'PRIMARY KEY (`job_ID_year`, `job_ID_number`)) ' \
              u'ENGINE = InnoDB ' \
              u'DEFAULT CHARACTER SET = utf8; '

    job_time_log_tbl = u'CREATE TABLE IF NOT EXISTS `job_time_log_TBL` (' \
                       u'`job_time_log_ID` INT(11) NOT NULL AUTO_INCREMENT, ' \
                       u'`job_ID_year` INT(4) NOT NULL, ' \
                       u'`job_ID_number` INT(6) NOT NULL, ' \
                       u'`person_ID` INT(11) NOT NULL, ' \
                       u'`start_time` DATETIME NOT NULL, ' \
                       u'`finish_time` DATETIME NULL DEFAULT NULL, ' \
                       u'`total_time` INT(11) NULL DEFAULT NULL, ' \
                       u'PRIMARY KEY (`job_time_log_ID`), ' \
                       u'INDEX `per_job_FK` (`person_ID` ASC), ' \
                       u'INDEX `job_time_FK` (`job_ID_year` ASC, `job_ID_number` ASC), ' \
                       u'CONSTRAINT `job_time_FK` ' \
                       u'FOREIGN KEY (`job_ID_year` , `job_ID_number`) ' \
                       u'REFERENCES `job_TBL` (`job_ID_year` , `job_ID_number`), ' \
                       u'CONSTRAINT `per_job_FK` ' \
                       u'FOREIGN KEY (`person_ID`) ' \
                       u'REFERENCES `member_TBL` (`person_ID`)) ' \
                       u'ENGINE = InnoDB ' \
                       u'DEFAULT CHARACTER SET = utf8; '

    email_tbl = u'CREATE TABLE IF NOT EXISTS `email_TBL` (' \
                u'`email_ID` INT(11) AUTO_INCREMENT NOT NULL, ' \
                u'`email_address` VARCHAR(150) NOT NULL, ' \
                u'`email_type` VARCHAR(45) NULL DEFAULT NULL, ' \
                u'`main` TINYINT(1) NULL DEFAULT NULL, ' \
                u'`person_ID` INT(11) NULL DEFAULT NULL, ' \
                u'`client_company_ID` INT(11) NULL DEFAULT NULL, ' \
                u'PRIMARY KEY (`email_ID`), ' \
                u'UNIQUE INDEX `email_ID_UNIQUE` (`email_ID` ASC), ' \
                u'CONSTRAINT `per_email_FK` ' \
                u'FOREIGN KEY (`person_ID`) ' \
                u'REFERENCES `member_TBL` (`person_ID`)) ' \
                u'ENGINE = InnoDB ' \
                u'DEFAULT CHARACTER SET = utf8;'

    member_linked_jobs_tbl = u'CREATE TABLE IF NOT EXISTS `member_linked_jobs_TBL` (' \
                             u'`job_ID_year` INT(4) NOT NULL, ' \
                             u'`job_ID_number` INT(6) NOT NULL, ' \
                             u'`person_ID` INT(11) NOT NULL, ' \
                             u'`assigned_date` DATE NOT NULL, ' \
                             u'PRIMARY KEY (`job_ID_year`, `job_ID_number`, `person_ID`), ' \
                             u'UNIQUE INDEX `member_linked_jobs_ID_UNIQUE` ' \
                             u'(`job_ID_year`, `job_ID_number`, `person_ID` ASC), ' \
                             u'CONSTRAINT `per_link_jobs_FK` ' \
                             u'FOREIGN KEY (`person_ID`) ' \
                             u'REFERENCES `member_TBL` ' \
                             u'(`person_ID`), ' \
                             u'CONSTRAINT `job_link_jobs_FK` ' \
                             u'FOREIGN KEY (`job_ID_year` , `job_ID_number`) ' \
                             u'REFERENCES `job_TBL` ' \
                             u'(`job_ID_year` , `job_ID_number`)) ' \
                             u'ENGINE = InnoDB ' \
                             u'DEFAULT CHARACTER SET = utf8; '
    tables = [member_tbl, email_tbl, job_tbl, job_time_log_tbl, member_linked_jobs_tbl]

    c, conn = connection(schema_name)

    def add_table(table_name):
        c.execute(table_name)
        conn.commit()

    try:

        for line in top:
            add_table(line)

        for line in tables:
            add_table(line)

        for line in bottom:
            add_table(line)

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


def check_new_username(username, login_details):
    """
    This function checks to see if a user name has been used before
    :param login_details:
    :param username:
    :return:
    """
    output = False

    sql = u'SELECT username ' \
          u'FROM member_TBL ' \
          u'WHERE userName = %s;'

    data = (username,)
    if verify_user_company_schema(login_details):
        c, conn = connection(login_details['company_schema'])
        try:
            c.execute(sql, data)
            info = c.fetchone()
            if info is None:
                output = True
        finally:
            conn_close(c, conn)
    return output


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
          u'(login_email, password, accept_terms, join_date, password_set)' \
          u'VALUES (%s, %s, %s, %s, %s)'

    accept_date = datetime.date.today()
    accept_date = str(accept_date.year) + "-" + str(accept_date.month) + "-" + str(accept_date.day)

    join_date = datetime.date.today()
    join_date = str(join_date.year) + "-" + str(join_date.month) + "-" + str(join_date.day)
    password_set = int(time.time())

    data = (user[1], user[2], accept_date, join_date, password_set)


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


def get_user_details(login_details):
    """
    Get a set amount of details from the member table in the company schema.
    Use in the User class mostly
    :param login_details:
    :return:
    """
    output = None
    sql = 'SELECT person_ID, first_name, last_name, username ' \
          'FROM member_TBL ' \
          'WHERE person_ID = %s'

    data = (login_details['person_ID'],)

    if verify_user_company_schema(login_details):

        c, conn = connection(login_details['company_schema'])
        try:
            c.execute(sql, data)

            values = c.fetchone()

            if values is not None:
                output = values

            else:
                output = ('error',)
        finally:
            conn_close(c, conn)
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


def get_possible_user_login_details(email):
    """
    As a user can be part of more than one company.
    This returns a list of possible matches for the email address
    :param email:
    :return:
    """
    output = None

    sql = 'SELECT person_ID, password, company_ID, password_set ' \
          'FROM person_TBL ' \
          'WHERE login_email = %s'

    data = (email,)

    c, conn = connection(master)
    try:
        c.execute(sql, data)

        values = c.fetchall()

        if values is not None:
            output = values
    finally:
        conn_close(c, conn)

    return output


def create_job(values, login_details):
    """
    Create a job in the database, only basic information is add at this time and in the future more has to be added.
    This function will break not all 4 values are passed in.
    :param login_details:
    :param values: List of up to 4 values passed in as strings. 2 is the minimum required.
    """
    # FIXME This function will break not all 4 values are passed in.
    job_number = None

    current_year = datetime.date.today()
    current_year = current_year.year

    next_number = next_job_number(current_year, login_details)

    sql = u'INSERT INTO job_TBL ' \
          u'(job_ID_year, job_ID_number, title, description, entry_date, quoted_Time, quoted_Cost)' \
          u'VALUES (%s, %s, %s, %s, NOW(), %s, %s)'

    hm = values[3]
    h, m = hm.split(':')

    quoted_time = (int(m) + (int(h) * 60)) * 60

    data = (current_year, next_number, values[0], values[1], quoted_time, float(values[2]))

    if verify_user_company_schema(login_details):
        c, conn = connection(login_details['company_schema'])
        try:
            c.execute(sql, data)
        finally:
            conn_close(c, conn)

        job_number = (current_year, next_number)

    return job_number


def next_job_number(current_year, login_details):
    """
    Use to find the next job number for the for the year in question
    :param login_details:
    :param current_year: In the format of a INT of length 4
    :return: INT of unknown length
    """
    output = None
    sql = u'SELECT MAX(job_ID_number) ' \
          u'FROM job_TBL ' \
          u'WHERE job_ID_year = %s'

    data = (current_year,)
    if verify_user_company_schema(login_details):
        c, conn = connection(login_details['company_schema'])
        try:
            c.execute(sql, data)

            value = c.fetchone()

            if value[0] is not None:
                output = int(value[0]) + 1
            else:
                output = 1
        finally:
            conn_close(c, conn)

    return output


def get_job_details(job_number, login_details):
    """
    Used to bring all the information about the job number from the database
    :param login_details:
    :param job_number: requires a tuple of 2 integers that are existing job number keys
    :return: a set record from the database
    """
    # TODO add in a fix to check to see if the input keys are existing in the database.
    output = None
    sql = u'SELECT title, description, entry_date, quoted_time, quoted_cost ' \
          u'FROM job_TBL ' \
          u'WHERE job_ID_year = %s ' \
          u'AND job_ID_number = %s'

    data = (job_number[0], job_number[1])

    if verify_user_company_schema(login_details):
        c, conn = connection(login_details['company_schema'])
        try:
            c.execute(sql, data)

            value = c.fetchone()

            if value[0] is not None:
                output = value
        finally:
            conn_close(c, conn)

    return output


def get_all_job_numbers(login_details):
    """
    This function will return a list of all the job numbers that is currently in be database
    :param login_details:
    """

    sql = u'SELECT job_ID_year, job_ID_number ' \
          u'FROM job_TBL'

    data = ()

    c, conn = connection(login_details['company_schema'])
    try:
        c.execute(sql, data)

        values = c.fetchall()

        if len(values) > 0:
            output = values
        else:
            output = 'List size error'
    finally:
        conn_close(c, conn)

    return output


def get_sudo_username(login_details):
    """
    Gets the default username for the adding of user to the company
    :param login_details: These are the values stored in the session cookie
    """
    name = 'UserName'
    sql = u'SELECT MAX(person_ID) ' \
          u'FROM member_TBL '

    if verify_user_company_schema(login_details):
        c, conn = connection(login_details['company_schema'])
        try:
            c.execute(sql)

            value = c.fetchone()

            if value is not None:
                number = value[0]
                number += 1

                name = 'UserName' + str(number)
        finally:
            conn_close(c, conn)

    return name


def get_local_master_ID(user_ID, login_details):
    """
    This method will get the master ID number for a member.
    It would be expected that this function would be run by someone looking up a person not the person them self's
    :param user_ID:
    :param login_details:
    """
    master_id = None
    find_id = u'SELECT login_master_ID ' \
              u'FROM member_TBL ' \
              u'WHERE person_ID = %s'

    if verify_user_company_schema(login_details):
        data = (user_ID,)

        c, conn = connection(login_details['company_schema'])

        try:
            c.execute(find_id, data)
            value = c.fetchone()

            if value is not None:
                master_id = value[0]

        finally:
            conn_close(c, conn)

    return master_id


def add_user(data_set, login_details):
    """
    Make a new user. This would be do by the admin for the company
    :param login_details:
    :param data_set:
    """
    person_ID = None
    insert_master_sql = u'INSERT INTO person_TBL ' \
                        u'(login_email, password, ' \
                        u'accept_terms, join_date, company_ID) ' \
                        u'VALUES (%s, %s, %s, %s, %s)'

    master_ID_sql = u'SELECT person_ID ' \
                    u'FROM person_TBL ' \
                    u'WHERE login_email = %s ' \
                    u'AND password = %s'

    insert_local_sql = u'INSERT INTO member_TBL ' \
                       u'(first_name, last_name, username, join_date, accept_terms, login_master_ID) ' \
                       u'VALUES (%s, %s, %s, %s, %s, %s);'

    person_ID_sql = u'SELECT person_ID ' \
                    u'FROM member_TBL ' \
                    u'WHERE login_master_ID = %s'

    add_email = u'INSERT INTO email_TBL ' \
                u'(`email_address`, `main`, `person_ID`) ' \
                u'VALUES (%s, 1, %s)'

    joinDate = datetime.date.today()
    joinDate = str(joinDate.year) + "-" + str(joinDate.month) + "-" + str(joinDate.day)

    if verify_user_company_schema(login_details):
        mc, mconn = connection(master)
        c, conn = connection(login_details['company_schema'])

        try:
            data = (data_set[1], data_set[4], joinDate, joinDate, login_details['company_ID'])
            mc.execute(insert_master_sql, data)
            mconn.commit()

            data = (data_set[1], data_set[4])
            mc.execute(master_ID_sql, data)

            value = mc.fetchone()

            if value is not None:
                master_ID = value[0]
            else:
                master_ID = 'error'

            if master_ID != 'error':
                data = (data_set[2], data_set[3], data_set[0], joinDate, joinDate, master_ID)
                c.execute(insert_local_sql, data)
                conn.commit()

                data = (master_ID,)
                c.execute(person_ID_sql, data)
                value = c.fetchone()

                if value is not None:
                    person_ID = value[0]

                add_email_data = (data_set[1], person_ID)
                c.execute(add_email, add_email_data)

        finally:
            conn_close(mc, mconn)
            conn_close(c, conn)

    return person_ID


def get_all_user_ids(login_details):
    """
    Will return the person_ID numbers for all the members in the company
    :param login_details: standard input values
    :return: list of person_ID
    """
    output = None
    sql = u'SELECT person_ID ' \
          u'FROM member_TBL'

    if verify_user_company_schema(login_details):
        c, conn = connection(login_details['company_schema'])

        try:
            c.execute(sql)
            values = c.fetchall()

            if values is not None:
                output = values
        finally:
            conn_close(c, conn)

    return output


def assign_users_to_job(values, login_details):
    """
    A function that will assign user to a job on the members linked jobs table
    :param values: set of ID values for the job and user
    :param login_details: standard input values
    """

    sql = u'INSERT INTO member_linked_jobs_TBL ' \
          u'(job_ID_year, job_ID_number, person_ID, assigned_date) ' \
          u'VALUES (%s, %s, %s, NOW());'

    data = values

    if verify_user_company_schema(login_details):
        c, conn = connection(login_details['company_schema'])

        try:
            c.execute(sql, data)
        finally:
            conn_close(c, conn)


def job_assigned_users(login_details, job_id):
    """
    Used to show the assigned company members to a job
    :param login_details:
    :param job_id:
    :return: List of person ID's or None
    """
    output = None

    sql = u'SELECT person_ID ' \
          u'FROM member_linked_jobs_TBL ' \
          u'WHERE job_ID_year = %s ' \
          u'AND job_ID_number = %s;'

    data = job_id

    if verify_user_company_schema(login_details):
        c, conn = connection(login_details['company_schema'])

        try:
            c.execute(sql, data)

            values = c.fetchall()

            if values is not None:
                output = values
        finally:
            conn_close(c, conn)

    return output


def remove_users_from_job(entry_id, login_details):
    """
    Removes the assigned user from the job in question
    :param entry_id:
    :param login_details:
    """
    sql = u'DELETE FROM member_linked_jobs_TBL ' \
          u'WHERE job_ID_year = %s ' \
          u'AND job_ID_number = %s ' \
          u'AND person_ID = %s;'

    data = entry_id

    if verify_user_company_schema(login_details):
        c, conn = connection(login_details['company_schema'])

        try:
            c.execute(sql, data)
        finally:
            conn_close(c, conn)
