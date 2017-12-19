import hashlib

#Зашифровать строку в SHA1
def getSHA1Pass(string):
    preparestr = string.encode('utf-8')
    return hashlib.sha1(preparestr).hexdigest()

#Hello
