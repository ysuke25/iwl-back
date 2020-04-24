import urllib
import json
import os
from flask import (Flask,request, make_response)

# mongodb
from pymongo import MongoClient
from pymongo import DESCENDING
from pymongo import ASCENDING

# _host = "testdb-myproject-yy.apps.us-east-2.starter.openshift-online.com"
_host = os.environ.get("MONGODB_OCP_ADDER")
_port = 27017
_db = os.environ.get("MONGODB_OCP_NAME")
_coll = os.environ.get("MONGODB_OCP_COLL")
user = os.environ.get("MONGODB_OCP_USER")
pwd = os.environ.get("MONGODB_OCP_PWD")

# Flask app should start in global layout
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/create-word-list', methods=['POST'])
def create_word_list():
    client = MongoClient(_host, _port, username=user, password=pwd, authSource="mydb", authMechanism='SCRAM-SHA-256')
    db = client[_db]
    collection = db[_coll]

    post = {
        "word":"test2",
        "description":"test_disc2"
    }

    result = collection.insert_one(post)

    print(result)

    return "200 OK"


@app.route('/get-word-list', methods=['GET'])
def get_word_list():
    client = MongoClient(_host, _port, username=user, password=pwd, authSource="mydb", authMechanism='SCRAM-SHA-256')
    db = client[_db]
    collection = db[_coll]

    result = collection.find(filter={"word":"test"})
    # print(result)
    for data in result :
        print(data)
    
    return data


if __name__ == '__main__':
    port = 8080
    print ("Starting app on port %d" %(port))
    app.run(debug=True, port=port, host='0.0.0.0')