
def isEmailValid(email: str):
    DOMAINs = ["gmail", "freemail"]
    TLDs = ["com", "hu"]
    
    for tld in TLDs:
        if email.endswith(tld):
            temp = email.removesuffix(tld)
            print("endswith: " , tld, temp)
            if temp.endswith("."):
                temp = temp.removesuffix(".")
                for dom in DOMAINs:
                    if temp.endswith(dom):
                        print("endswith: " , dom)
                        temp = temp.removesuffix(dom)
                        if temp.endswith("@"):
                            print("returns: ", True)
                            return True
    return False
    
def isPasswordValid(password: str):
    if len(password) >= 8:
        for i in password:
            if i.isupper():
                for i in password:
                    if i.islower():
                        for i in password:
                            if i.isnumeric():
                                return (True, "")
                            else: resp = "Password ha no numeric character!"
                    else: resp = "Password has no Lowercase character!"
            else: resp = "Password has no Uppercase character!"
    else: resp = "Password is not 8 character long atleast!"
    return (False, resp)
                    