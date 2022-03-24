#pintwo database sqlite3
import sqlite3
from dataclasses import dataclass

@dataclass
class db:
    #def __init__(self):
        #"""Initialize db class variables"""
        #define connection and cursor

    def __init__(self, username, shortbio, ratings, contacts):
        self.username, self.shortbio, self.ratings, self.contacts = username, shortbio, ratings, contacts

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return "%s;%s;%f,%s" % (self.username, self.shortbio, self.ratings, self.contacts)

    #commit changes
    def commit(self):
       """commit changes to database"""
       self.connection.commit()
 
    #close connection
    def close(self):
       """close sqlite3 connection"""
       self.connection.close()

conn = sqlite3.connect('PinTwo.db')
cur = conn.cursor()

cur.execute("SELECT * FROM userprofile")
results = cur.fetchall()
print(results)

conn.commit()
conn.close()
   