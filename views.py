from flask import render_template, request
from pys import app, db, process, process_img, process_emergency, config
import os


# get
@app.route('/')
@app.route('/home')
def hello():
    title = "Home Admin"
    temp = db.select_login()
    user_id = None
    if temp is not None:
        user_id = temp[3]
    return render_template('hello.html', title=title, user_id=user_id)


@app.route('/login')
def login():
    title = "Login"
    temp = db.select_login()
    temp2 = db.select_login_stu()
    user_id = None
    if temp is not None:
        user_id = temp[3]
    if temp2 is not None:
        user_id = temp2[3]
    return render_template('login.html', title=title, user_id=user_id)


@app.route('/logout')
def logout():
    title = "Logout"
    temp = db.select_login()
    temp2 = db.select_login_stu()
    if temp is not None:
        login_id = temp[0]
        db.delete_login(login_id)
    elif temp2 is not None:
        login_id = temp2[0]
        db.delete_login_stu(login_id)
    return render_template('logout.html', title=title)


@app.route('/manage')
def manage():
    title = "Managing students"
    temp = db.select_login()
    if temp is not None:
        user_id = temp[3]
    else:
        title = "Login"
        return render_template("login.html", title=title)
    return render_template('manage.html', title=title, user_id=user_id)


@app.route('/image')
def image():
    title = "Image"
    temp = db.select_login()
    if temp is not None:
        user_id = temp[3]
    else:
        title = "Login"
        return render_template("login.html", title=title)
    dirs1, dirs2, dirs3 = process_img.get_filename(user_id)
    return render_template('image.html', title=title, user_id=user_id, dirs1=dirs1, dirs2=dirs2, dirs3=dirs3)


@app.route('/search')
def search():
    title = "search"
    temp = db.select_login()
    if temp is not None:
        user_id = temp[3]
    else:
        title = "Login"
        return render_template('login.html', title=title)
    return render_template('search.html', title=title, user_id=user_id)


@app.route('/emergency')
def emergency():
    title = "Emergency"
    temp = db.select_login()
    if temp is not None:
        user_id = temp[3]
    else:
        title = "Login"
        return render_template('login.html', title=title)
    process_emergency.get_new_pneumonia()
    f = open('data.txt', 'r')
    json = eval(f.read())
    data = json["data"]
    history = data["history"]
    change = [history[0]["confirmedNum"] - history[1]["confirmedNum"],
              history[0]["suspectedNum"] - history[1]["suspectedNum"], history[0]["curesNum"] - history[1]["curesNum"],
              history[0]["deathsNum"] - history[1]["deathsNum"]]
    return render_template('emergency.html', title=title, user_id=user_id, data=data, history=history, change=change)


# student
@app.route('/student')
def student():
    title = "Home Student"
    temp = db.select_login_stu()
    user_id = None
    if temp is not None:
        user_id = temp[3]
    return render_template('student_hello.html', title=title, user_id=user_id)


@app.route('/student/emergency')
def student_emergency():
    title = "Emergency"
    temp = db.select_login_stu()
    if temp is not None:
        user_id = temp[3]
    else:
        title = "Login"
        return render_template('login.html', title=title)
    process_emergency.get_new_pneumonia()
    f = open('data.txt', 'r')
    json = eval(f.read())
    data = json["data"]
    history = data["history"]
    change = [history[0]["confirmedNum"] - history[1]["confirmedNum"],
              history[0]["suspectedNum"] - history[1]["suspectedNum"], history[0]["curesNum"] - history[1]["curesNum"],
              history[0]["deathsNum"] - history[1]["deathsNum"]]
    return render_template('student_emergency.html', title=title, user_id=user_id, data=data, history=history, change=change)


@app.route('/student/investigation')
def student_investigation():
    title = "Investigation"
    temp = db.select_login_stu()
    if temp is not None:
        user_id = temp[3]
    else:
        title = "Login"
        return render_template('login.html', title=title)
    return render_template('student_investigation.html', title=title,
                           user_id=user_id, data=config.investigation_base_data)


# post
@app.route('/login', methods=['POST'])
def login_solve():
    paras = request.json
    user_id = paras["user_id"]
    password = paras["password"]
    click_type = paras["clickType"]
    if click_type == "administrators_Login":
        return process.login(user_id, password)
    elif click_type == "administrators_Register":
        return process.register(user_id, password)
    else:
        administrators_id = paras["administrators_id"]
        if click_type == "students_Login":
            return process.stu_login(user_id, password, administrators_id)
        elif click_type == "students_Register":
            return process.stu_register(user_id, password, administrators_id)


@app.route('/manage/add', methods=['POST'])
def manage_add():
    temp = db.select_login()
    user_id = temp[3]
    db_name = "database/stu_%s.db" % user_id
    paras = request.json
    s_id = paras["student-id"]
    s_grade = paras["student-grade"]
    s_class = paras["student-class"]
    s_name = paras["student-name"]
    try:
        sex = paras["sex"]
    except Exception as e:
        print(e)
        sex = None
    return process.manage_add(db_name, s_id, s_grade, s_class, s_name, sex)


@app.route('/manage/delete', methods=['POST'])
def manage_delete():
    temp = db.select_login()
    user_id = temp[3]
    db_name = "database/stu_%s.db" % user_id
    paras = request.json
    s_id = paras["student-id"]
    del_type = paras["type"]
    if del_type == "check":
        return process.student_check(db_name, s_id)
    elif del_type == "sent":
        return process.manage_delete_sent(db_name, s_id)


@app.route('/manage/select', methods=['POST'])
def manage_select():
    temp = db.select_login()
    user_id = temp[3]
    db_name = "database/stu_%s.db" % user_id
    paras = request.json
    search_type = paras["search_type"]
    value = paras["sel_value"]
    json_res = process.manage_select(db_name, search_type, value)
    return json_res


@app.route('/image/base/check', methods=['POST'])
def image_check():
    temp = db.select_login()
    user_id = temp[3]
    db_name = "database/stu_%s.db" % user_id
    data = request.json
    stu_id = data["id"]
    json = process.student_check(db_name, stu_id)
    flag = process.image_check(stu_id)
    json["is_have"] = flag
    if json["error_des"] == "success":
        f = open('temp.txt', 'w')
        f.write(str(stu_id))
    return json


# 负责添加基础图片
@app.route('/image/base/post', methods=['POST'])
def image_base_post():
    temp = db.select_login()
    user_id = temp[3]
    img = request.files.get("image_file")
    f = open('temp.txt', 'r')
    stu_id = int(f.read())
    file_path = "static/img/User/%s/Base/%s.jpg" % (user_id, stu_id)
    img.save(file_path)
    process_img.face_set_add(file_path, user_id, stu_id)
    return file_path


# 负责添加普通图片
@app.route('/image/img/post', methods=['POST'])
def image_img_post():
    temp = db.select_login()
    user_id = temp[3]
    img = request.files.get("image_file")
    # 获取并更改流水号
    f = open('static/img/User/Eclipse_R/id.txt', 'r')
    i = int(f.read())
    f.close()
    f2 = open('static/img/User/Eclipse_R/id.txt', 'w')
    f2.write(str(i + 1))
    f2.close()
    # 保存
    file_path = "static/img/User/%s/img/%s.jpg" % (user_id, i)
    img.save(file_path)
    # 获取图片特性
    user = process_img.face_search(file_path, {user_id})
    print(user)
    # 保存图片特性
    f3 = open('static/img/User/Eclipse_R/img/%s.txt' % str(i), 'w')
    f3.write(str(user))
    f3.close()
    return user


@app.route('/search/img/post', methods=['POST'])
def search_img_post():
    temp = db.select_login()
    user_id = temp[3]
    img = request.files.get("image_file")
    if os.path.exists("static/temp.jpg"):
        os.remove("static/temp.jpg")
    # 保存
    file_path = "static/temp.jpg"
    img.save(file_path)
    # 获取图片特性
    stu_id = process_img.face_search(file_path, {user_id})
    data = {'error_des': 'None'}
    try:
        res = process.search(stu_id, user_id)
        if stu_id['0'] is not None:
            data['id'] = stu_id['0']
            if res is not None:
                data['data'] = res
                data['error_des'] = 'success'
            else:
                data['error_des'] = 'cantfind'
    except Exception as e:
        print(e)
    return data


@app.route('/emergency/select', methods=['POST'])
def emergency_select():
    temp = db.select_login()
    user_id = temp[3]
    db_name = "database/stu_%s.db" % user_id
    paras = request.json
    search_type = paras["search_type"]
    value = paras["new_pneumonia_value"]
    json_res = process.manage_select(db_name, search_type, value)
    return json_res


@app.route('/student/investigation', methods=['POST'])
def investigation_post():
    temp = db.select_login_stu()
    if temp is not None:
        user_id = temp[3]
        admin_id = temp[5]
    else:
        title = "Login"
        return render_template('login.html', title=title)
    paras = request.json
    paras['stu_id'] = user_id
    paras['admin_id'] = admin_id
    return process.investigation(paras)
