def int_to_bit(value: int, fix_length=-1):
    if fix_length == -1:
        return [True if value & (1 << (value.bit_length() - 1 -n)) else False for n in range(value.bit_length())]
    else:
        return [True if value & (1 << (fix_length - 1 -n)) else False for n in range(fix_length)]

def bool_func(bit_array):
    a = bit_array[0]
    b = bit_array[1]
    c = bit_array[2]
    d = bit_array[3]
    return ((a and b) or (a and (not b) and c)) and ((d ^ a) or (a^c^d))

nb_bits = 4
for i in range(0, pow(2, nb_bits)):
    print(int_to_bit(i, nb_bits), bool_func(int_to_bit(i, nb_bits)))
