from pys import db, config
import os


def login(user_id, password):
    json_res = {"error_des": "success"}

    table_name = "USER"
    error_01 = "error_id_password"
    db_name = "stu.db"

    res = db.select_user(db_name, table_name, user_id)

    if res is None:
        json_res["error_des"] = error_01
    else:
        if res[2] == password:
            db.insert_login(user_id)
        else:
            json_res["error_des"] = error_01
    return json_res


def register(user_id, password):
    json_res = {"error_des": "success"}

    table_name = "USER"
    error_02 = "unknown_error"
    error_03 = "already_have"
    db_name = "stu.db"

    res = db.select_user(db_name, table_name, user_id)
    if res is None:
        db.insert_user(table_name, user_id, password)

        check = db.select_user(db_name, table_name, user_id)
        if check is None:
            json_res["error_des"] = error_02
        else:
            db_name = "database/stu_%s.db" % user_id
            db.create_student(db_name)
            path = os.getcwd()
            os.chdir('static/img/User/')
            os.system('mkdir %s' % user_id)
            os.chdir('%s/' % user_id)
            os.system('mkdir Base')
            os.system('mkdir img')
            os.chdir(path)
    else:
        json_res["error_des"] = error_03
    return json_res


def stu_login(stu_id, password, administrators_id):
    json_res = {"error_des": "success"}

    table_name = "USER"
    error_01 = "error_id_password"
    db_name = "database/stu_%s.db" % administrators_id

    res = db.select_stu(db_name, table_name, stu_id)

    if res is None:
        json_res["error_des"] = error_01
    else:
        if res[2] == password:
            db.insert_login_stu(stu_id, administrators_id)
        else:
            json_res["error_des"] = error_01
    return json_res


def stu_register(stu_id, password, administrators_id):
    json_res = {"error_des": "success"}

    table_name = "USER"
    error_02 = "unknown_error"
    error_03 = "already_have"
    error_04 = "cant_find_stu"
    error_05 = "type_error"
    db_name = "database/stu_%s.db" % administrators_id

    res = db.select_stu(db_name, table_name, stu_id)
    if res is None:
        try:
            stu = int(stu_id)
            res = db.select_student_id(db_name, stu)
        except Exception as e:
            print(e)
            json_res["error_des"] = error_05
        try:
            temp = res[0]
            db.insert_user_stu(db_name, table_name, stu_id, password, administrators_id)

            check = db.select_stu(db_name, table_name, stu_id)
            if check is None:
                json_res["error_des"] = error_02
        except Exception as e:
            print(e)
            json_res["error_des"] = error_04
    else:
        json_res["error_des"] = error_03
    return json_res


def manage_add(db_name, student_id, grade, class_index, student_name, sex):
    json_res = {"error_des": "success"}
    if student_id == '':
        json_res["error_des"] = "empty_id"
    elif grade == '':
        json_res["error_des"] = "empty_grade"
    elif class_index == '':
        json_res["error_des"] = "empty_class"
    elif student_name == '':
        json_res["error_des"] = "empty_name"
    elif sex is None:
        json_res["error_des"] = "empty_sex"
    else:
        try:
            stu_id = int(student_id)
            stu_grade = int(grade)
            stu_class = int(class_index)
            res = db.select_student_id(db_name, stu_id)
            try:
                if res[1] is not None:
                    flag = False
                else:
                    flag = True
            except Exception as e:
                print(e)
                flag = True
            if flag:
                db.insert_student(db_name, stu_id, stu_grade, stu_class, student_name, sex)
            else:
                json_res["error_des"] = "already_have"
        except Exception as e:
            print(e)
            json_res["error_des"] = "type_error"
    return json_res


def student_check(db_name, student_id):
    json_res = {"error_des": "success"}
    try:
        stu_id = int(student_id)
        res = db.select_student_id(db_name, stu_id)
    except Exception as e:
        print(e)
        json_res["error_des"] = "type_error"
        return json_res
    try:
        json_res["student_id"] = student_id
        json_res["grade"] = res[0][2]
        json_res["class"] = res[0][3]
        json_res["name"] = res[0][4]
        json_res["sex"] = res[0][5]
    except Exception as e:
        print(e)
        json_res["error_des"] = "cant_find"
    return json_res


def manage_delete_sent(db_name, student_id):
    json_res = {"error_des": "success"}
    try:
        stu_id = int(student_id)
    except Exception as e:
        print(e)
        json_res["error_des"] = "type_error"
        return json_res
    db.delete_student(db_name, "STUDENT_ID", stu_id)
    return json_res


def manage_select(db_name, search_type, value):
    json_res = {"error_des": "success"}
    try:
        if search_type == "all":
            v = 0
        elif search_type is None:
            json_res["error_des"] = "choose"
            return json_res
        else:
            v = int(value)
        res = db.select_student_search(db_name, search_type, v)
        index = 0
        for i in res:
            json_res[str(index)] = i
            index += 1
    except Exception as e:
        print(e)
        json_res["error_des"] = "type_error"
    return json_res


def image_check(student_id):
    temp = db.select_login()
    user_id = temp[3]
    path = "static/img/User/%s/Base/%s.jpg" % (user_id, student_id)
    return os.path.exists(path)


def investigation(data):
    title = data['title']
    stu_id = data['stu_id']
    admin_id = data['admin_id']
    db_name = "database/stu_%s.db" % admin_id
    res = db.select_investigation(db_name, stu_id)
    if res is None:
        data = data['data'].split('&')
        post = []
        for i in data:
            post.append(i[2:])
        db.insert_investigation(db_name, stu_id, post)
        return "accept"
    return "already_have"


def search(stu_id, admin_id):
    db_name = "database/stu_%s.db" % admin_id
    stu_id = stu_id['0']
    try:
        res = db.select_investigation(db_name, stu_id)[2:]
        data = []
        for index, each in enumerate(res):
            string = []
            string.append(config.investigation_base_data[index]['title'])
            string.append(config.investigation_base_data[index]['data'][str(each)])
            data.append(string)
        return list(data)
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    temp = ""
    search("0", "Eclipse_R")
