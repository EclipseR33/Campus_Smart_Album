import requests
from pys import config, db
import base64
from PIL import Image, ImageDraw
import os


def get_64(pic_path):
    try:
        # 二进制方式读取文件
        img = open(pic_path, 'rb')
        data = base64.b64encode(img.read())
        print(data)
        return data
    except Exception as e:
        print("read pic file error")
        print(e)


def get_token():
    # headers = {"Content-Type": "application/json"}
    host = config.TOKEN_URL + "?grant_type=client_credentials&" \
           + "client_id=" + config.API_KEY \
           + "&client_secret=" + config.SEC_KEY + "&"
    try:
        res = requests.post(host)
        if res is not None:
            if res.status_code // 100 == 2:
                return res.json()
            else:
                return None
        else:
            return None
    except Exception as e:
        print(e)
        return None


# 使用百度云人脸识别API
def face_detect(pic_path):
    # json_res = {"error_des": "success"}

    content = get_token()
    if content is None:
        print("Get content failed")
        return False

    token = content.get("access_token")
    # json获取字符串转对象的方法
    host = config.FACE_URL + "?access_token=" + token

    # 构造request请求对接云端API
    headers = {"content-type": "application/json"}
    pic = get_64(pic_path)
    body = {"image": pic, "image_type": "BASE64", "max_face_num": 10}
    resp = requests.post(host, data=body, headers=headers)
    if resp is None:
        return False
    if resp.status_code // 100 != 2:
        return False
    face_data = resp.json().get("result")
    face_num = face_data.get("face_num")
    face_list = face_data.get("face_list")
    print("face_num:")
    print(face_num)
    print("face_list:")
    print(face_list)

    im = Image.open(pic_path)
    draw = ImageDraw.Draw(im)
    fill = 255
    width_t = 2
    for num in range(0, face_num):
        location_info = face_list[num]['location']
        left = location_info['left']
        top = location_info['top']
        width = location_info['width']
        height = location_info['height']
        draw.line((left, top, left + width, top), fill=fill, width=width_t)
        draw.line((left, top, left, top + height), fill=fill, width=width_t)
        draw.line((left + width, top, left + width, top + height), fill=fill, width=width_t)
        draw.line((left, top + height, left + width, top + height), fill=fill, width=width_t)
    length = len(pic_path)
    path = pic_path[:length - 4] + "_post" + pic_path[length-4:]
    print(path)
    im.save(path)
    return path


# 人脸注册
def face_set_add(pic_path, group_id, user_id):
    user_id = str(user_id)
    content = get_token()
    if content is None:
        print("Get content failed")
        return False

    token = content.get("access_token")
    # json获取字符串转对象的方法
    host = config.FACE_SET_ADD_URL + "?access_token=" + token

    # 构造request请求对接云端API
    headers = {"content-type": "application/json"}
    pic = get_64(pic_path)
    body = {"image": pic, "image_type": "BASE64", "group_id": group_id, "user_id": user_id}
    resp = requests.post(host, data=body, headers=headers)
    if resp is None:
        return False
    if resp.status_code // 100 != 2:
        return False
    print(resp)
    data = resp.json().get("result")
    face_token = data.get("face_token")
    face_location = data.get("location")
    print("face_token", face_token)
    print("location", face_location)


# 用户信息查询
def face_set_get(group_id, user_id):
    content = get_token()
    if content is None:
        print("Get content failed")
        return False

    token = content.get("access_token")
    # json获取字符串转对象的方法
    host = config.FACE_SET_GET_URL + "?access_token=" + token

    # 构造request请求对接云端API
    headers = {"content-type": "application/json"}
    body = {"group_id": group_id, "user_id": user_id}
    resp = requests.post(host, data=body, headers=headers)
    if resp is None:
        return False
    if resp.status_code // 100 != 2:
        return False
    data = resp.json().get("result")
    print(data)
    log_id = data.get("log_id")
    user_list = data.get("user_list")


def face_search(pic_path, group_id_list):
    content = get_token()
    if content is None:
        print("Get content failed")
        return False

    token = content.get("access_token")
    # json获取字符串转对象的方法
    host = config.FACE_SEARCH_URL + "?access_token=" + token

    # 构造request请求对接云端API
    headers = {"content-type": "application/json"}
    pic = get_64(pic_path)
    body = {"image": pic, "image_type": "BASE64", "group_id_list": group_id_list, "max_face_num": 10}
    resp = requests.post(host, data=body, headers=headers)
    if resp is None:
        return False
    data = resp.json().get("result")
    print(data)
    if data is None:
        return False
    face_list = data.get("face_list")
    user = {}
    index = 0
    for i in face_list:
        u = i["user_list"]
        try:
            u = u[0]
            score = int(u["score"])
            if score >= 80:
                user_id = u["user_id"]
                print(score)
                user[str(index)] = user_id
                index += 1
        except Exception as e:
            print(e)
    return user


def get_filename(user_id):
    path = "static/img/User/%s/img/" % user_id
    dirs = os.listdir(path)
    print(dirs)
    files1 = {}
    files2 = {}
    files3 = {}
    ma = int(len(dirs)/2)
    for i in range(0, ma):
        if i % 3 == 0:
            files1[str(i)] = {}
        elif i % 3 == 1:
            files2[str(i)] = {}
        elif i % 3 == 2:
            files3[str(i)] = {}
    index = 0
    temp = 0
    for f in dirs:
        length = len(f)
        t = f[length-4:]
        if t == ".txt":
            f = open('static/img/User/Eclipse_R/img/%s.txt' % str(temp), 'r')
            string = eval(f.read())
            txt = ""
            if string is not False:
                for i in string:
                    db_name = "database/stu_%s.db" % user_id
                    res = db.select_student_id(db_name, int(i))
                    res = res[0]
                    txt = txt + "-Name:%s; Student-Id:%s; G-C:%s-%s" % (res[4], res[1], res[2], res[3])
            print(txt)
            if index % 3 == 0:
                files1[str(index)]["txt"] = txt
            elif index % 3 == 1:
                files2[str(index)]["txt"] = txt
            elif index % 3 == 2:
                files3[str(index)]["txt"] = txt
            f.close()
            index += 1
        else:
            if index % 3 == 0:
                files1[str(index)]["img"] = f
            elif index % 3 == 1:
                files2[str(index)]["img"] = f
            elif index % 3 == 2:
                files3[str(index)]["img"] = f
            temp = int(f[:length-4])
    print(files1)
    print(files2)
    print(files3)
    return files1, files2, files3


if __name__ == "__main__":
    file_path = "static/photo/Jack_6.jpg"
    get_filename("Eclipse_R")
    # face_detect(file_path)
    # face_set_get('Eclipse_R', '0')

# group_id: test
# # user_id: Jack
