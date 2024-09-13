from pymongo import MongoClient

def get_db_connection(db_name='admin', host="127.0.0.1", port=27017, username="admin", password="admin"):

    client = MongoClient(host,
                      port=int(port),
                      username=username ,
                      password=password
                     )
    db = client[db_name]
    return db, client


class db_Handler:
    
    def __init__(self ,db_name ="admin", host ="127.0.0.1", port=27017, username="admin", password="admin"):
        self.db, self.client = get_db_connection(db_name=db_name,host=host,port=port,username=username,password=password)
        
    def write(self,local,valueToInsert):
        self.db[local].insert_one(valueToInsert)
        return 0

    def read(self,local,valueToRead):
        return self.db[local].find(valueToRead)

    def update(self,local,querry,valueToUpdate):
        self.db[local].update_one(querry,valueToUpdate)
        return 0

    def delete(self,local,querry):
        self.db[local].delete_one(querry)
        return 0