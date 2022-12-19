from random import choice

def randomCodeGenerator(longitud):
    caracteres = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<=>@#%&+"

    p = ""
    p = p.join([choice(valores) for i in range(longitud)])
    return p

def randomCodeVerification(realCode, codeReceived):
    
    realCodeList = list(realCode)
    codeReceivedList = list(codeReceived)
    counter = 0
    if len(realCodeList) == len(codeReceivedList):
        for i in range(len(realCode)):
            if realCodeList[i] == codeReceivedList[i]:
                counter+=1
    if counter == len(realCode): return True
    else: return False