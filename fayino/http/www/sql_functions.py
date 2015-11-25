import gc
import pymysql
import datetime

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
    Will do grabge colllection too
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
          u'(userName, loginEmail, password, acceptTErms    , joinDate)' \
          u'VALUES (%s, %s, %s, %s, %s)'

    acceptDate = datetime.date.today()
    acceptDate = str(acceptDate.year) + "-" + str(acceptDate.month) + "-" + str(acceptDate.day)

    joinDate = datetime.date.today()
    joinDate = str(joinDate.year) + "-" + str(joinDate.month) + "-" + str(joinDate.day)

    data = (user[0], user[1], user[2], acceptDate, joinDate)

    c.execute(sql, data)
    conn_close(c, conn)


















