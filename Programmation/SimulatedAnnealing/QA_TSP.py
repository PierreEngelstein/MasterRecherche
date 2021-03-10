# import dwave_networkx
# import networkx
# import dimod
# g = networkx.Graph()
# g.add_weighted_edges_from({(0, 1, .1), (0, 2, .5), (0, 3, .1), (1, 2, .1),(1, 3, .5), (2, 3, .1)})

# dwave_networkx.algorithms.traveling_salesperson(g, dimod.ExactSolver(), start=0)

def int_to_bit(value: int, fix_length=-1):
    if fix_length == -1:
        return [True if value & (1 << (value.bit_length() - 1 -n)) else False for n in range(value.bit_length())]
    else:
        return [True if value & (1 << (fix_length - 1 -n)) else False for n in range(fix_length)]

def bool_func(bit_array):
    return (bit_array[0] and bit_array[1]) or (bit_array[2] and (not bit_array[1])) or (bit_array[0] and bit_array[2])

for i in range(0, 8):
    print(int_to_bit(i, 3), bool_func(int_to_bit(i, 3)))