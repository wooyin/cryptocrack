#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64

alphabet1 = "+-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
alphabet2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def decode(data,encoding='utf-8'):
	out = b''
	try:
		out += base64.b64decode(data.translate(str.maketrans(alphabet1, alphabet2)),"=/")
		return str(out,encoding)
	except:
		out += base64.b64decode(data[1:].translate(str.maketrans(alphabet1, alphabet2)),"=/")
		return str(out,encoding)