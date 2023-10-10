import sqlite3 as sql

class cons():
    CREATE_TABLE = "CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, username TEXT, password TEXT, name TEXT, email TEXT);"
    READ_ALL_ACCOUNT = "SELECT * FROM accounts;"
    INSERT_ACCOUNT = "INSERT INTO accounts ( username, password, name, email ) VALUES ( ?, ?, ?, ? );"
    GETACCOUNT = "SELECT * FROM accounts WHERE username=:username;"

class command():
    def create_table():
        with sql.connect("database.db") as cur:
            cur.execute(cons.CREATE_TABLE)

    def insert_account(username: str, password: str, name: str, email: str):
        with sql.connect("database.db") as cur:
            cur.execute(cons.INSERT_ACCOUNT, (username, password, name, email))
            
    def getAllAccount(Print : bool = False) -> list:
        with sql.connect("database.db") as cur:
            result = cur.execute(cons.READ_ALL_ACCOUNT).fetchall()
            if Print:
                print(result)
            return result
        
    def getAccount(username):
        with sql.connect("database.db") as cur:
            result = cur.execute(cons.GETACCOUNT, {"username" : username}).fetchall()
            if result != [] and len(result) == 1:
                return (True, result[0])
            
            else:
                return (False, None)