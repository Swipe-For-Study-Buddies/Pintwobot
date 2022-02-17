#pintwo database sqlite3
import sqlite3

class db(object):

    #def __init__(self):
        #"""Initialize db class variables"""
        #define connection and cursor
    connection = sqlite3.connect('PinTwo.db')
    cursor = connection.cursor()

    #close connection 
    def close(self):
        """close sqlite3 connection"""
        self.connection.close()

    #create userprofile table(info on card for swiping and skimming)
    command1 = """CREATE TABLE IF NOT EXISTS userprofile(username TEXT PRIMARY KEY, shortbio TEXT, ratings INTEGER, contacts TEXT)"""

    cursor.execute(command1)

    def execute(self, new_data):
        """execute a row of data to current cursor"""
        self.cur.execute(new_data)

    #add to userprofile
    cursor.execute("INSERT INTO userprofile VALUES ('test', 'hi', 2, 'null')")

    #update
    cursor.execute("UPDATE userprofile SET ratings = 3 WHERE ratings = 2")

    #delete
    cursor.execute("DELETE FROM userprofile WHERE ratings = 2")

    #get results 
    cursor.execute("SELECT * FROM userprofile")
    results = cursor.fetchall()
    print(results)

    #commit changes
    def commit(self):
        """commit changes to database"""
        self.connection.commit()
