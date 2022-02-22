#from sympy import symbols
import sympy
from sympy.physics.units import gram, second, cm, nm

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

def getMassGainTimeLambda(conditions, modules=None):
    """
    Create a custom function lambda to be quickly executable for all time values
    within the specified module (e.g. for plotting many points).

    Parameters:
    conditions (dict): a dictionary with all conditions except t.
    modules (str): the module for which to generate the lambda. In all my uses, I set modules="numpy"

    Returns:
    f (function): function with signature f(t) -> float, where f(t) returns the mass gain after a time t
    u (sympy.Expr): the units in which f returns its answer, with equations.t inside.
        calling e.g. `u.subs([(equations.t,second), (equations.e, 1), (equations.F_p, 1)])).as_coeff_Mul()[1]/(-1 + sympy.sqrt(5))`
        (assuming that the value of t should be in seconds; otherwise use whatever unit is applicable)
        gives the units in which f(t) would return the mass gain.
    """
    conditions_values = {}
    conditions_units = {}
    # TODO iterate through all keys, copy the key and just the numerical component of the value, copy the units elsewhere
    for key in conditions:
        if type(conditions[key]) == sympy.core.mul.Mul:
            #print(conditions[key].as_coeff_Mul())
            content_tuple = conditions[key].as_coeff_Mul()
            conditions_values[key] = content_tuple[0]
            conditions_units[key] = content_tuple[1]
        else:
            #print(conditions[key])
            conditions_values[key] = conditions[key]

    return sympy.lambdify(t, x_substituted.subs(conditions_values), modules), x_substituted.subs(conditions_units)

def getOxideThicknessTimeLambda(conditions, modules=None):
    """
    Same as getMassGainTimeLambda, except this one calculates the thickness of the oxide layer.
    Assume all mass gained is in Cu2O (this is the phase at low temperature and pressure).
    Assume density of Cu2O to be 6.0 g/cm^3.
    Atomic mass of oxygen is 15.999 g/mol
    Molar mass of Cu2O is 143.09 g/mol.
    Therefore, thickness = mass gain/area / 15.999 * 143.09 / 6

    Parameters:
    conditions (dict): a dictionary with all conditions except t.
    modules (str): the module for which to generate the lambda. In all my uses, I set modules="numpy"

    Returns:
    f (function): function with signature f(t) -> float, where f(t) returns the oxide thickness after a time t
    u (sympy.Expr): the units in which f returns its answer, with equations.t inside.
        calling e.g. `u.subs([(equations.t,second), (equations.e, 1), (equations.F_p, 1)])).as_coeff_Mul()[1]/(-1 + sympy.sqrt(5))`
        (assuming that the value of t should be in seconds; otherwise use whatever unit is applicable)
        gives the units in which f(t) would return the oxide thickness.
    """
    conditions_values = {}
    conditions_units = {}
    # TODO handle the conversion to nm more gracefully
    # TODO handle the application of Cu20 constants more gracefully
    for key in conditions:
        if type(conditions[key]) == sympy.core.mul.Mul:
            #print(conditions[key].as_coeff_Mul())
            content_tuple = conditions[key].as_coeff_Mul()
            conditions_values[key] = content_tuple[0]
            conditions_units[key] = content_tuple[1]
        else:
            #print(conditions[key])
            conditions_values[key] = conditions[key]

    thickness_function = x_substituted.subs(conditions_values)  / 15.999 * 143.09 / 6 * 1e7
    thickness_units = x_substituted.subs(conditions_units) * cm**2/gram * nm
    return sympy.lambdify(t, thickness_function, modules), thickness_units
