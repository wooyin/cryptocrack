
__download__ = 'https://files.pythonhosted.org/packages/84/00/f341816387c59f9096dac3ed691b2efa9a612c3e8df08fe810f684356def/Rot13-1.0.zip'

def rot13_func(string):
    newstring=''
    for char in string:
        n=ord(char)
        
        if (n>=97 and n<=122): 
            rtn=n +13
            if not (rtn>=97 and rtn<=122): 
                rtn=rtn-26
            newstring+=chr(rtn)

        if (n>=65 and n<=90):
                    
                    rtn=n+13
                    if not (rtn>=65 and rtn<=90):
                      rtn-=26
                    newstring+=chr(rtn) 
            
        if not ((n>=97 and n<=122) or (n>=65 and n<=90)):
            
            newstring+=char
    return (newstring)

encode = rot13_func
decode = rot13_func