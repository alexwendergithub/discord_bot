import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["bot"]

def insert_into_db(collection,insertion):
    mycol = mydb[collection]
    x = mycol.insert_one(insertion)