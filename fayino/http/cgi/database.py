import gc
import pymysql
from cgi.tables import sql as tables


class Database(object):

    def __init__(self, schema):
        self.c, self.conn = self.connection(schema)
        self.execute = self.c.execute

    @staticmethod
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

    def conn_close(self):
        """
        Use to close and commit the transaction with the sql database
        Will do garbage collection too

        :return:
        """
        self.conn.commit()
        self.c.close()
        self.conn.close()
        gc.collect()

    def create_tables(self, sql):
        passed = True
        for list_e in sql:
            for script in list_e:
                passed = self.run_script(script)

        if passed is not False:
            return True

        else:
            return False

    def run_script(self, sql_script):
        try:
            self.c.execute(sql_script)
            self.conn.commit()
        except Exception:
            return False

if __name__ == '__main__':
    d = Database('testing_main')
    d.create_tables(tables)
    d.conn_close()
