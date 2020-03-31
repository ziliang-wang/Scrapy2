import pymongo


class Handle_mongo_guazi:

    def __init__(self):
        my_client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
        self.db = my_client['db_guazi']

    def save_task(self, collection_name, task):
        print(f'当前存储的是{task}')
        collection = self.db[collection_name]
        data = dict(task)
        collection.insert_one(data)

    def get_task(self, collection_name):
        collection = self.db[collection_name]
        task = collection.find_one_and_delete({})
        return task

    def save_data(self, collection_name, data):
        print(f'正在存入...{data}')
        collection = self.db[collection_name]
        data = dict(data)
        collection.update({'car_id': data['car_id']}, data, True)


mongo = Handle_mongo_guazi()
