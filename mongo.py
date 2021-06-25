import pymongo
import pymongo.errors
import os
import time
import functools
from setting import *


# uri = settings.mongodb_uri
db_name = URI.split('/')[-1]
_remote_db = ""
if ISMONGO:
    _remote_db = pymongo.MongoClient(URI, serverSelectionTimeoutMS=10 * 1000,
                                 socketTimeoutMS=15 * 1000,
                                 waitQueueTimeoutMS=15 * 1000)[db_name]


# _lan_db = pymongo.MongoClient(os.environ.get("LOCAL_DB", "mongodb://crawler:Duoshoubang@10.1.10.4:27018/dsb"), connect = False, serverSelectionTimeoutMS = 5 * 1000)[db_name]

# local = pymongo.MongoClient(host=MONGO_IP)
# local_db = local[db_name]

def network_retry(method):
    @functools.wraps(method)
    def inner(*args, **kwargs):
        error_counter = 0
        while True:
            try:
                return method(*args, **kwargs)

            except pymongo.errors.NetworkTimeout:
                print("mongo timeout. retry...")
                error_counter += 1
                if error_counter > 3:
                    raise
                else:
                    time.sleep(0.5)
                    continue

    return inner


class ReadWriteCollection(object):
    def __init__(self, db, collection_name):
        self.rw_db = db
        self.collection_name = collection_name

    def __getattr__(self, name):
        db = self.rw_db.w_db
        if name in ("find", "find_one", "aggregate"):
            db = self.rw_db.r_db

        if self.rw_db.debug:
            print("{} {}.{} by db: {}".format(
                name, db.name, self.collection_name, db.client.address))

        attr_value = getattr(db[self.collection_name], name)
        if name in ("find_one", "update_one"):
            return network_retry(attr_value)

        return attr_value


class ReadWriteDB(object):
    def __init__(self, r_db, w_db):
        try:
            r_db.test.find_one()  # debug

        except Exception as ex:
            print("access read db error. %s" % (ex,))
            r_db = w_db

        self.r_db, self.w_db = r_db, w_db
        self.debug = bool(os.environ.get("DB_DEBUG"))

    def __getitem__(self, name):
        return ReadWriteCollection(self, name)

    def __getattr__(self, name):
        if self.is_collection(name):
            return ReadWriteCollection(self, name)

        else:
            return getattr(self.rw_db, name)

    def is_collection(self, name):
        return name not in dir(self.w_db)

if ISMONGO:
    remote_db = ReadWriteDB(_remote_db, _remote_db)
