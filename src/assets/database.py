import sqlite3 as sql
import os

class cons():
    CREATE_TABLE = "CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, username TEXT, password TEXT, name TEXT, email TEXT);"
    READ_ALL_ACCOUNT = "SELECT * FROM accounts;"
    INSERT_ACCOUNT = "INSERT INTO accounts ( username, password, name, email ) VALUES ( ?, ?, ?, ? );"
    GETACCOUNT = "SELECT * FROM accounts WHERE username=:username;"

def create_database(file):
    open(file, "x")
    
def create_table(file: str):
    with sql.connect(file) as cur:
        cur.execute(cons.CREATE_TABLE)

def insert_account(file: str, username: str, password: str, name: str, email: str):
    if not os.path.isfile(file):
        create_database(file)
        create_table(file)
    with sql.connect(file) as cur:
        cur.execute(cons.INSERT_ACCOUNT, (username, password, name, email))
        
def getAllAccount(file: str, Print : bool = False) -> list:
    if not os.path.isfile(file):
        create_database(file)
        create_table(file)
    with sql.connect(file) as cur:
        result = cur.execute(cons.READ_ALL_ACCOUNT).fetchall()
        if Print:
            print(result)
        return result
    
def getAccount(file: str, username):
    if not os.path.isfile(file):
        create_database(file)
        create_table(file)
    with sql.connect(file) as cur:
        result = cur.execute(cons.GETACCOUNT, {"username" : username}).fetchall()
        if result != [] and len(result) == 1:
            return (True, result[0])
        
        else:
            return (False, None)