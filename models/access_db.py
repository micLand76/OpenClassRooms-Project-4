from tinydb import TinyDB, Query, where
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
from datetime import datetime


class DbManag:

    serialization = SerializationMiddleware(JSONStorage)
    serialization.register_serializer(DateTimeSerializer(), 'TinyDate')

    db = TinyDB('db.json', storage=serialization, indent=4)
    User = Query()

    def connect_db(self):
        pass

    def close_db(self):
        self.db.close()

    def search_data(self, field='name', value=''):
        return self.search(where(field) == value)
