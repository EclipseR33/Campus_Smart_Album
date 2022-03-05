import sqlite3
import datetime
import socket


# 查询ip地址
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def create(db_name):
    conn = sqlite3.connect(db_name)
    try:
        c = conn.cursor()
        sql = '''
        CREATE TABLE INVESTIGATION(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            STUDENT_ID INTEGER,
            A INTEGER,
            B INTEGER,
            C INTEGER,
            D INTEGER,
            E INTEGER,
            F INTEGER,
            G INTEGER
        )
        '''

        c.execute(sql)
        conn.commit()
        c.close()
        print("Create *")
    except Exception as e:
        print(e)
        print("Create Failed")
    finally:
        conn.close()


def create_student(db_name):
    conn = sqlite3.connect(db_name)
    try:
        c = conn.cursor()
        sql = '''
        CREATE TABLE STUDENT(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            STUDENT_ID INTEGER,
            GRADE INTEGER,
            CLASS INTEGER,
            NAME TEXT,
            SEX TEXT
        )
        '''
        c.execute(sql)

        sql = '''
        CREATE TABLE USER(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            USER_ID TEXT,
            PASSWORD TEXT,
            JURISDICTION TEXT
        )
        '''
        c.execute(sql)

        sql = '''
        CREATE TABLE INVESTIGATION(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            STUDENT_ID INTEGER,
            A INTEGER,
            B INTEGER,
            C INTEGER,
            D INTEGER,
            E INTEGER,
            F INTEGER,
            G INTEGER
        )
        '''
        c.execute(sql)

        conn.commit()
        c.close()
        print("Create *")
    except Exception as e:
        print(e)
        print("Create Failed")
    finally:
        conn.close()


def drop(db_name, table_name):
    conn = sqlite3.connect(db_name)
    try:
        c = conn.cursor()
        sql = '''
            DROP TABLE %s
        ''' % table_name
        c.execute(sql)
        conn.commit()
        c.close()
        print("Drop *")
    except Exception as e:
        print(e)
        print("Drop Failed")
    finally:
        conn.close()


def insert_user(table_name, user_id, password):
    conn = sqlite3.connect("stu.db")
    try:
        c = conn.cursor()
        sql = '''
            INSERT INTO %s VALUES(NULL, '%s', '%s')
        ''' % (table_name, user_id, password)
        c.execute(sql)
        conn.commit()
        c.close()
        print("Insert *")
    except Exception as e:
        print(e)
        print("Insert Failed")
    finally:
        conn.close()


def insert_user_stu(db_name, table_name, user_id, password, administrators_id):
    conn = sqlite3.connect(db_name)
    try:
        c = conn.cursor()
        sql = '''
            INSERT INTO %s VALUES(NULL, '%s', '%s', 'None', '%s')
        ''' % (table_name, user_id, password, administrators_id)
        c.execute(sql)
        conn.commit()
        c.close()
        print("Insert *")
    except Exception as e:
        print(e)
        print("Insert Failed")
    finally:
        conn.close()


def insert_investigation(db_name, user_id, data):
    conn = sqlite3.connect(db_name)
    try:
        c = conn.cursor()
        sql = '''
            INSERT INTO INVESTIGATION VALUES(NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
        ''' % (user_id, data[0], data[1], data[2], data[3], data[4], data[5], data[6])
        c.execute(sql)
        conn.commit()
        c.close()
        print("Insert *")
    except Exception as e:
        print(e)
        print("Insert Failed")
    finally:
        conn.close()


def select_user(db_name, table_name, user_id):
    conn = sqlite3.connect(db_name)
    res = "?Select-Failed?"
    try:
        c = conn.cursor()
        sql = '''
            SELECT * FROM %s WHERE UserID='%s'
        ''' % (table_name, user_id)
        c.execute(sql)
        res = c.fetchone()
        c.close()
        print("Select *")
    except Exception as e:
        print(e)
        print("Select Failed")
    finally:
        conn.close()
    return res


def select_stu(db_name, table_name, user_id):
    conn = sqlite3.connect(db_name)
    res = "?Select-Failed?"
    try:
        c = conn.cursor()
        sql = '''
            SELECT * FROM %s WHERE USER_ID='%s'
        ''' % (table_name, user_id)
        c.execute(sql)
        res = c.fetchone()
        c.close()
        print("Select *")
    except Exception as e:
        print(e)
        print("Select Failed")
    finally:
        conn.close()
    return res


def select_investigation(db_name, stu_id):
    conn = sqlite3.connect(db_name)
    res = "?Select-Failed?"
    try:
        c = conn.cursor()
        sql = '''
            SELECT * FROM INVESTIGATION WHERE STUDENT_ID='%s'
        ''' % stu_id
        c.execute(sql)
        res = c.fetchone()
        c.close()
        print("Select *")
    except Exception as e:
        print(e)
        print("Select Failed")
    finally:
        conn.close()
    return res


def insert_login(user_id):
    conn = sqlite3.connect("stu.db")
    try:
        c = conn.cursor()
        pc_name = socket.getfqdn(socket.gethostname())
        ip = get_host_ip()
        date = datetime.date.today()
        sql = '''
            INSERT INTO LOGIN VALUES(NULL, '%s', '%s', '%s', '%s')
        ''' % (ip, pc_name, user_id, date)
        c.execute(sql)
        conn.commit()
        c.close()
        print("Insert *")
    except Exception as e:
        print(e)
        print("Insert Failed")
    finally:
        conn.close()


def insert_login_stu(user_id, administrators_id):
    conn = sqlite3.connect("stu.db")
    try:
        c = conn.cursor()
        pc_name = socket.getfqdn(socket.gethostname())
        ip = get_host_ip()
        date = datetime.date.today()
        sql = '''
            INSERT INTO LOGIN_STU VALUES(NULL, '%s', '%s', '%s', '%s', '%s')
        ''' % (ip, pc_name, user_id, date, administrators_id)
        c.execute(sql)
        conn.commit()
        c.close()
        print("Insert *")
    except Exception as e:
        print(e)
        print("Insert Failed")
    finally:
        conn.close()


def select_login():
    conn = sqlite3.connect("stu.db")
    res = "?Select-Failed?"
    date = str(datetime.date.today())
    try:
        c = conn.cursor()
        ip = get_host_ip()
        sql = '''
                SELECT * FROM LOGIN WHERE IP='%s'
            ''' % ip
        c.execute(sql)
        res = c.fetchall()
        c.close()
        print("Select *")
    except Exception as e:
        print(e)
        print("Select Failed")
    finally:
        conn.close()
    length = len(res)
    ans = None
    if length >= 1:
        ans = res[length-1]
    if ans is not None:
        if not res == "?Select-Failed?":
            if date == ans[4]:
                return ans
    return None


def select_login_stu():
    conn = sqlite3.connect("stu.db")
    res = "?Select-Failed?"
    date = str(datetime.date.today())
    try:
        c = conn.cursor()
        ip = get_host_ip()
        sql = '''
                SELECT * FROM LOGIN_STU WHERE IP='%s'
            ''' % ip
        c.execute(sql)
        res = c.fetchall()
        c.close()
        print("Select *")
    except Exception as e:
        print(e)
        print("Select Failed")
    finally:
        conn.close()
    length = len(res)
    ans = None
    if length >= 1:
        ans = res[length-1]
    if ans is not None:
        if not res == "?Select-Failed?":
            if date == ans[4]:
                return ans
    return None


def delete_login(value):
    conn = sqlite3.connect("stu.db")
    try:
        c = conn.cursor()
        sql = '''
            DELETE FROM LOGIN WHERE ID=%d
        ''' % value
        c.execute(sql)
        conn.commit()
        c.close()
        print("delete *")
    except Exception as e:
        print(e)
        print("delete Failed")
    finally:
        conn.close()


def delete_login_stu(value):
    conn = sqlite3.connect("stu.db")
    try:
        c = conn.cursor()
        sql = '''
            DELETE FROM LOGIN_STU WHERE ID=%d
        ''' % value
        c.execute(sql)
        conn.commit()
        c.close()
        print("delete *")
    except Exception as e:
        print(e)
        print("delete Failed")
    finally:
        conn.close()


def insert_student(db_name, student_id, grade, class_index, student_name, sex):
    conn = sqlite3.connect(db_name)
    try:
        c = conn.cursor()
        sql = '''
                INSERT INTO STUDENT VALUES(NULL, '%d', '%d', '%d', '%s', '%s')
            ''' % (student_id, grade, class_index, student_name, sex)
        c.execute(sql)
        conn.commit()
        c.close()
        print("Insert *")
    except Exception as e:
        print(e)
        print("Insert Failed")
    finally:
        conn.close()


def delete_student(db_name, del_type, value):
    conn = sqlite3.connect(db_name)
    try:
        c = conn.cursor()
        if type(value) == int:
            sql = '''
                DELETE FROM STUDENT WHERE %s=%d
            ''' % (del_type, value)
        else:
            sql = '''
                DELETE FROM STUDENT WHERE %s=%s
            ''' % (del_type, value)
        c.execute(sql)
        conn.commit()
        c.close()
        print("delete *")
    except Exception as e:
        print(e)
        print("delete Failed")
    finally:
        conn.close()


def select_student_id(db_name, student_id):
    conn = sqlite3.connect(db_name)
    res = "?Select-Failed?"
    try:
        c = conn.cursor()
        sql = '''
                SELECT * FROM STUDENT WHERE STUDENT_ID=%d
            ''' % student_id
        c.execute(sql)
        res = c.fetchall()
        c.close()
        print("Select *")
    except Exception as e:
        print(e)
        print("Select Failed")
    finally:
        conn.close()
    return res


def select_student_search(db_name, search_type, value):
    conn = sqlite3.connect(db_name)
    res = "?Select-Failed?"
    try:
        c = conn.cursor()
        if search_type == "all":
            sql = '''
                SELECT * FROM STUDENT
            '''
        else:
            sql = '''
                SELECT * FROM STUDENT WHERE %s=%d
            ''' % (search_type, value)
        c.execute(sql)
        res = c.fetchall()
        c.close()
        print("Select *")
    except Exception as e:
        print(e)
        print("Select Failed")
    finally:
        conn.close()
    return res


if __name__ == "__main__":
    db_name = "database/stu_Eclipse_R.db"
    res = select_investigation(db_name, '190101490066')[2:]
    print(res)
