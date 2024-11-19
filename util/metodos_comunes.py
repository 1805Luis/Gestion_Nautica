def ascii_a_hexadecimal(texto):
        hexadecimal = texto.encode("utf-8").hex()
        array_hex = [int(hexadecimal[i:i+2], 16) for i in range(0, len(hexadecimal), 2)]
        return array_hex