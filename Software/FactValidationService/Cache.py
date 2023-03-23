import sqlite3, time
from datastructures.exceptions.CacheException import CacheException

def exceptionHandling(func):
    """
    Decorator function.
    Database operations might fail because the database is locked by another thread.
    If that is the case, the operation will be repeated up to 9 times, if this decorator is used.
    """
    def inner(*args, **kwargs):
        for i in range(10):
            try:
                return func(*args, **kwargs)
            except sqlite3.OperationalError as ex:
                time.sleep(0.1)
    return inner

class Cache:
    """
    Wrapper that encapsulates the SQL database
    that is used to cache validation results.
    """
    
    def __init__(self, dbpath:str, approach:str):
        try:
            self.db = sqlite3.connect(dbpath)
        except sqlite3.OperationalError:
            raise CacheException("Cannot access FactValidationService cache")
            
        self.approach = approach
        try:
            self.createTable()
        except sqlite3.OperationalError:
            pass
        
    def createTable(self):
        self.db.execute('''CREATE TABLE {}_cache
        (subject TEXT NOT NULL,
        predicate TEXT NOT NULL,
        object TEXT NOT NULL,
        score REAL NOT NULL,
        PRIMARY KEY (subject, predicate, object)
        );'''.format(self.approach))
        
    def close(self):
        self.db.close()
        
    @exceptionHandling
    def insert(self, sub:str, pred:str, obj:str, score:float):
        input = [(sub), (pred), (obj), (score)]
        self.db.execute("INSERT INTO {}_cache (subject, predicate, object, score) VALUES (?, ?, ?, ?)".format(self.approach), input)
        self.db.commit()
    
    @exceptionHandling
    def getScore(self, sub:str, pred:str, obj:str):
        input = [(sub), (pred), (obj)]
        cursor = self.db.execute('SELECT score FROM {}_cache WHERE subject=? AND predicate=? AND object=?'.format(self.approach), input)
        for row in cursor:
            return row[0]
