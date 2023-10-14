import sqlite3 as sql

''' Constant Strings '''
CREATE_TABLE = "CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, username TEXT, password TEXT, name TEXT, email TEXT);"
INSERT_ACCOUNT = "INSERT INTO accounts ( username, password, name, email ) VALUES ( ?, ?, ?, ? );"
GETACCOUNTS = "SELECT * FROM accounts;"

''' Variable(s) '''
db_file = "database.db"

class Create:
    
    def database(db_file):
        open("x")
    
    def table(db_file):
        with sql.connect(db_file) as cur:
            cur.execute(CREATE_TABLE)

class Insert:

    def account(username: str, password: str, name: str, email: str):
        with sql.connect(db_file) as cur:
            cur.execute(INSERT_ACCOUNT, (username, password, name, email))    

class Check:
    def checkCall(type: str, value: str):
        match type:
            case "username":
                i = 1
            case "email":
                i = 3
            case "name":
                i = 4
        accounts = Get.allAccount()
        same = False
        for account in accounts:
            if value == account[i]:
                same = True
        match same:
            case True: return True
            case False: return False
    
    def Username(Username: str):
        Check.checkCall(value=Username, type="username")

    def Email(Email: str):
        Check.checkCall(value=Email, type="email")

    def Name(Name: str):
        Check.checkCall(value=Name, type="name")
        
class Get:
       
    def allAccount(Print : bool = False):
        with sql.connect(db_file) as cur:
            result = cur.execute(GETACCOUNTS).fetchall()
            if Print:
                print(result)
            return result
    
    def Accby(by: str, value: str):
        match by:
            case "username":
                a = "username"
            case "email":
                a = "email"
            case "name":
                a = "name"

        with sql.connect(db_file) as cur:
            result = cur.execute(f"SELECT * FROM accounts WHERE {a}=:{a};", {f"{a}" : value}).fetchall()
            print(len(result))
            if result != [] and len(result) == 1:
                return result[0]
            else:
                return None
    
    class AccountBy:
        
        def Username(Username: str):
            return Get.Accby(value=Username, by="username")

        def Email(Email: str):
            return Get.Accby(value=Email, by="email")

            
    
    
    
