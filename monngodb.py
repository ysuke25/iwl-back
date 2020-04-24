from pymongo import MongoClient
from pymongo import DESCENDING
from pymongo import ASCENDING

import os

# _host = "testdb-myproject-yy.apps.us-east-2.starter.openshift-online.com"
_host = os.environ.get("MONGODB_OCP_ADDER")
_port = 27017
_db = "mydb"
_coll = "wordlist"
user = "pyuser"
pwd = "pyuser_password"


def post_data():
    
    client = MongoClient(_host, _port, username=user, password=pwd, authSource="mydb", authMechanism='SCRAM-SHA-256')
    db = client[_db]
    collection = db[_coll]

    post = {
        "word":"test2",
        "description":"test_disc2"
    }

    result = collection.insert_one(post)

    print(result)

def get_data(test):
    client = MongoClient(_host, username=user, password=pwd, authSource="mydb", authMechanism='SCRAM-SHA-256')
    db = client[_db]
    collection = db[_coll]

    result = collection.find(filter={"word":"test"})
    # print(result)
    for data in result :
        print(data)



if __name__ == "__main__":
    post_data()
    # get_data("test")