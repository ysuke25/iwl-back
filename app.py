import urllib
import json
import os
from flask import (Flask,request, make_response)
from bson.objectid import ObjectId

# mongodb
from pymongo import MongoClient
from pymongo import DESCENDING
from pymongo import ASCENDING

# get env
def env_set():
    env_set_dic = {}

    _host = os.environ.get("MONGODB_OCP_ADDER")
    _port = 27017
    _db = os.environ.get("MONGODB_OCP_NAME")
    _coll = os.environ.get("MONGODB_OCP_COLL")
    user = os.environ.get("MONGODB_OCP_USER")
    pwd = os.environ.get("MONGODB_OCP_PWD")

    env_set_dic = {
        "host": _host,
        "port": _port,
        "db" : _db,
        "coll" : _coll,
        "user" : user,
        "pwd" : pwd 
    }

    return env_set_dic

def support_ObjectId(obj):
    '''json.dumps()でObjectIdを処理するための関数
    ObjectIdはjsonエンコードできない型なので、文字列型に変換する

    戻り値：
    ObjectIdから変換した文字列
    '''
    if isinstance(obj, ObjectId):
        return str(obj)     # 文字列として扱う
    raise TypeError(repr(obj) + " is not JSON serializable")


# Flask app should start in global layout
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route("/")
def env_check():
    check_env = env_set()
    print(check_env.get("host"))

    if check_env.get("host") != None:
        return check_env.get("host")
    else :
        return "No env\n"

@app.route('/create-word-list', methods=['POST'])
def create_word_list():
    # use evn
    ce = env_set()

    #create clinet connection to monogodb
    client = MongoClient(ce["host"], ce["port"], username=ce["user"], password=ce["pwd"], authSource=ce["db"], authMechanism='SCRAM-SHA-256')
    db = ce["db"]
    db = client[db]
    coll = ce["coll"]
    collection = db[coll]

    # post = {
    #    "word":"test2",
    #    "description":"test_disc2"
    #}

    if request.method == "POST":
        req = request.get_json(silent=True, force=True)
        print(req)

    # check request
    if "word" and "description" in req:
        result = collection.insert_one(req)
        print(result)
        return "200 OK"
    else:
        print(req)
        return "somethin worng. check your json \"word\" and \"description\" "


@app.route('/get-word-list', methods=['GET'])
def get_word_list():
    # use evn
    ce = env_set()

    #create clinet connection to monogodb
    client = MongoClient(ce["host"], ce["port"], username=ce["user"], password=ce["pwd"], authSource=ce["db"], authMechanism='SCRAM-SHA-256')
    db = ce["db"]
    db = client[db]
    coll = ce["coll"]
    collection = db[coll]

    show_dict = {}
    i = 0

    #result = collection.find(filter={"word":"test2"})
    result = collection.find()
    # print(type(result))
    for data in result :
        i += 1
        show_dict[i] = data
        
    json_data = json.dumps(show_dict, ensure_ascii=False, indent=4, default=support_ObjectId)
    r = make_response(json_data)
    r.headers['Content-Type'] = 'application/json'
    return r
    
    


if __name__ == '__main__':
    port = 8080
    print ("Starting app on port %d" %(port))
    app.run(debug=True, port=port, host='0.0.0.0')