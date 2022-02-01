#from sympy import symbols
import sympy

k_p, k_l, t, t_0 = sympy.symbols("k_p, k_l, t, t_0")

x = sympy.Rational(1/2)*(-k_p/k_l + sympy.sqrt((k_p/k_l)**2 + 4*k_p*(t + t_0)))

n_p, A_1, A_2, A_l, F_p, P_O2, P_O2ref_p, P_O2ref_l, R, T, T_ref, n_l, e, E_1, E_2, E_l  = sympy.symbols("n_p, A_1, A_2, A_l, F_p, P_{O_2}, P_{O_2}^{ref\,p}, P_{O_2}^{ref\,l}, R, T, T_ref, n_l, e, E_1, E_2, E_l ")

# the expression for k_p, eqn (4-3)
k_p_expr = F_p*(P_O2/P_O2ref_p)**n_p*(A_1*e**-(E_1/R/T) + A_2*e**-(E_2/R/T))

# the expression for k_l, eqn (4-4)
k_l_expr = A_l*(P_O2/P_O2ref_l)**n_l*e**(-E_l/R*(1/T - 1/T_ref))

x_substituted = x.subs([(k_p, k_p_expr), (k_l, k_l_expr)])

# approximate as linear rate law:
x_linear = k_l*(t + t_0)
x_linear_substituted = x_linear.subs(k_l, k_l_expr)

# helper functions that make it easy to calculate things:
def complexMassGain(conditions):
    """
    calculates the mass gain given certain conditions

    Parameter:
    conditions (dictionary): the conditions in which to calculate,
        addressed with the relevant symbol as a key and the relevant value with units as the value

    Returns:
    mass gain, in units of g/cm**2
    """
    return x_substituted.evalf(subs=conditions)

def linearMassGain(conditions):
    return x_linear_substituted.evalf(subs=conditions)
