import datetime
import string
from random import choice, randint

from cgi import database


def gen_schema():
    all_char = string.ascii_letters + string.digits
    company_schema = "zb_" + "".join(choice(all_char) for x in range(randint(7, 17)))

    return company_schema


class Company(object):

    def __init__(self, company_id, company_schema):
        self.id = company_id
        self.schema = company_schema

    @classmethod
    def enter_company_detail(cls, company):
        """
        Enter a company name into the system
        The codes should be checked first.
        :param company: List of values from a form that has been filled in
        :return:
        """

        all_char = string.ascii_letters + string.digits
        company_schema = "zt_" + "".join(choice(all_char) for x in range(randint(7, 17)))

        set_up_date = datetime.date.today()
        set_up_date = str(set_up_date.year) + "-" + str(set_up_date.month) + "-" + str(set_up_date.day)

        sql = u'INSERT INTO company_TBL ' \
              u'(company_name, set_up_date, company_schema) ' \
              u'VALUES (%s, %s, %s)'

        data = (company, set_up_date, company_schema)

        db = database.Database('test_login_master_files')

        db.execute(sql, data)
        db.conn.commit()

        company_id_sql = u'SELECT company_id ' \
                         u'FROM company_TBL ' \
                         u'WHERE company_schema = %s'

        company_id_data = (company_schema,)

        db.execute(company_id_sql, company_id_data)

        value = db.c.fetchone()
        if value is not None:
            company_id = value[0]
        else:
            company_id = 'Error'

        db.conn_close()

        return company_id, company_schema
