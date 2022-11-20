
"""
driver code for converting into morse code and vice versa
"""

morsedict={ 'A':'.-', 'B':'-...','C':'-.-.', 'D':'-..', 'E':'.','F':'..-.', 'G':'--.', 'H':'....','I':'..', 'J':'.---', 'K':'-.-','L':'.-..', 'M':'--', 'N':'-.','O':'---', 'P':'.--.', 'Q':'--.-','R':'.-.', 'S':'...', 'T':'-','U':'..-', 'V':'...-', 'W':'.--','X':'-..-', 'Y':'-.--', 'Z':'--..','1':'.----', '2':'..---', '3':'...--','4':'....-', '5':'.....', '6':'-....','7':'--...', '8':'---..', '9':'----.','0':'-----', ',':'--..--', '.':'.-.-.-','?':'..--..', '/':'-..-.', '-':'-....-','(':'-.--.', ')':'-.--.-'}

def encode(x):
    morse_cipher=''
    y=x.upper()
    for i in y:
        if i != ' ':
            morse_cipher+=morsedict[i]+' '
        else:
            morse_cipher += ' '
    return morse_cipher #returning morse code

def decode(x):
	x+=' '
	morse_decipher=''
	temp_var=''
	for i in x:
		if (i!=' '):
			c = 0
			temp_var+=i
		else:
			c+=1
			if c == 2 :
				morse_decipher+=' '
			else:
				morse_decipher+=list(morsedict.keys())[list(morsedict.values()).index(temp_var)]
				temp_var=''
	return morse_decipher.lower() #returing plain text as lower literals
