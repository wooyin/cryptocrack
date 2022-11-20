
def encode(data, encoding="utf-8"):
    """
    str to hex
    """
    return bytes(data,encoding).hex()


def decode(data, encoding="utf-8"):
    """
    hex to str
    """
    return str(bytes.fromhex(data),encoding)
