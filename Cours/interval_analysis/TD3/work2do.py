from interval.contractors import i_sqr, c_mul, c_add, c_sqr


# general contractor for the system
# note that this contractor should use the basic contractors imported line 1
def c_system(e_val, u1_val, u2_val, r1_val, r2_val, i_val, p_val):
    """ :param e_val (Interval)
        :param u1_val (Interval)
        :param u2_val (Interval)
        :param r1_val (Interval)
        :param r2_val (Interval)
        :param i_val (Interval)
        :param p_val (Interval)
    """
    e_val_c, u1_val_c, u2_val_c = c_add(e_val, u1_val, u2_val)
    u1_val_c1, r1_val_c1, i_val_c1 = c_mul(u1_val_c, r1_val, i_val)
    u2_val_c1, r2_val_c1, i_val_c1 = c_mul(u2_val_c, r2_val, i_val)


    return e_val_c, u1_val_c, u2_val_c, r1_val, r2_val, i_val, p_val
