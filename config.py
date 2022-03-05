# coding : utf-8

HOST = "0.0.0.0"
PORT = "5000"

# 百度AK-SK
AK = "8909facaf545459188bcd5853b6c5d6d"
SK = "b8e8787e8e014e30b99bb5bf924404c8"

# 百度应用的API-K和SEC-KEY
API_KEY = "a93wsdUGeGYSxVDXcl9GbIpd"
SEC_KEY = "7eORx2YxnSEWGrPf9Pg9OXl7MOWZ8BNL"

TOKEN_URL = "https://aip.baidubce.com/oauth/2.0/token"
FACE_URL = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
FACE_SET_ADD_URL = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add"
FACE_SET_GET_URL = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/get"
FACE_SEARCH_URL = "https://aip.baidubce.com/rest/2.0/face/v3/multi-search"

url = "http://127.0.0.1:5000/"

investigation_base_data = [
    {
        'index': 1,
        'title': '身高',
        'data': {'1': '1.8 米以上', '2': '1.7米-1.8米', '3': '1.6米-1.7米', '4': '1.5米-1.6米', '5': '1.5米以下'}
     },
    {
        'index': 2,
        'title': '体重',
        'data': {'1': '150斤以上', '2': '130斤-150斤', '3': '90斤-130斤', '4': '90斤以下'}
     },
    {
        'index': 3,
        'title': '感兴趣的学科',
        'data': {'1': '语文', '2': '数学', '3': '英语', '4': '物理', '5': '化学',
                 '6': '生物', '7': '历史', '8': '地理', '9': '政治', '10': '技术'}
     },
    {
        'index': 4,
        'title': '最讨厌的学科',
        'data': {'1': '语文', '2': '数学', '3': '英语', '4': '物理', '5': '化学',
                 '6': '生物', '7': '历史', '8': '地理', '9': '政治', '10': '技术'}
     },
    {
        'index': 5,
        'title': '最喜欢的书籍',
        'data': {'1': '文学', '2': '科普', '3': '历史', '4': '艺术', '5': '传记'}
     },
    {
        'index': 6,
        'title': '性格',
        'data': {'1': '文静', '2': '活泼', '3': '内向', '4': '害羞', '5': '任性'}
     },
    {
        'index': 7,
        'title': '成绩',
        'data': {'1': '很好', '2': '较好', '3': '一般', '4': '较差', '5': '很差'}
     }
]
