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
    stop = False
    e_val_prec, u1_val_prec, u2_val_prec, r1_val_prec, r2_val_prec, i_val_prec, p_val_prec = e_val, u1_val, u2_val, r1_val, r2_val, i_val, p_val
    while not stop:
        u1_val, r1_val, i_val = c_mul(u1_val, r1_val, i_val)
        u2_val, r2_val, i_val = c_mul(u2_val, r2_val, i_val)
        e_val, u1_val, u2_val = c_add(e_val, u1_val, u2_val)
        p_val, i_val, e_val = c_mul(p_val, i_val, e_val)
        if e_val_prec == e_val and u1_val_prec == u1_val and u2_val_prec == u2_val and r1_val_prec == r1_val and r2_val_prec == r2_val and i_val_prec == i_val and p_val_prec == p_val :
            stop=True
        e_val_prec, u1_val_prec, u2_val_prec, r1_val_prec, r2_val_prec, i_val_prec, p_val_prec = e_val, u1_val, u2_val, r1_val, r2_val, i_val, p_val
    
    return e_val, u1_val, u2_val, r1_val, r2_val, i_val, p_val
