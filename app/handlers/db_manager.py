from pymongo import InsertOne, MongoClient
from app.db import mongo  # Assuming this is your database configuration

class DBManager:
    def __init__(self, collection_name):
        self.collection = mongo.db[collection_name]

    def insert_one(self, document):
        self.collection.insert_one(document)

    def insert_batch(self, batch):
        operations = [InsertOne(row) for row in batch]
        self.collection.bulk_write(operations)

    def update_status(self, cron_id, status, remark=None):
        updates = {'status': status}
        if remark:
            updates['remark'] = remark
        self.collection.update_one({'cron_id': cron_id}, {'$set': updates})

    def find(self, query):
        return self.collection.find(query)
