#from sympy import symbols
from sympy.physics.units import gram, mol, second, kelvin, joule, pascal, cm

#A_1, A_2, E_1, E_2, A_l, E_l, n_l, n_p, F_p, e, R, P_O2ref_p, P_O2ref_l, T_ref, t, P_O2, T, t_0 = symbols("A_1, A_2, E_1, E_2, A_l, E_l, n_l, n_p, F_p, e, R, P_O2ref_p, P_O2ref_l, T_ref, t, P_O2, T, t_0")
from equations import *

import numpy

# fitted values for both regimes, from table 2-1 and 4-5. Should be independent of experiment.
fitted_values = {
    #parabolic:
    A_1: 634*gram**2/(cm**4*second), A_2: 8.67e-4*gram**2/(cm**4*second), 
    E_1: 248e3*joule/mol, E_2:103e3*joule/mol,
            
    #linear:
    A_l: 1.19e-7*gram/cm**2/second, E_l: 27e3*joule/mol, n_l: 1.04, n_p: 0, F_p: 0.83,
                            
    #universal constants:
    e: 2.718281828459045, R: 8.31446261815324*joule/kelvin/mol
}

# values constant for all experiments by Bjorck et al
experiment_constants = {
    P_O2ref_p: 2.1e4*pascal,
    P_O2ref_l: 100*pascal,
    T_ref: 1173.15*kelvin,
    t: 28800*second #see cell above
}

experiment_values = {
    # conditions for each of the experiments performed by Bjorck et al. 
    # Key is the two-character code they used, value is a dict of conditons
    # some have a t_0 that was fitted to them, but the ones for which no t_0 was provided
    # have no t_0; this would return True from the test t_0==None
    "1A": {
        P_O2: 2.1e4*pascal,
        T: 543.15*kelvin
    },
                    
    "1B": {
        P_O2: 2.1e4*pascal,
        T: 1173.15*kelvin,
        t_0: 396*second
    },

    "2A": {
        P_O2: 1e3*pascal,
        T: 543.15*kelvin
    },

    "2B": {
        P_O2: 1e3*pascal,
        T: 1173.15*kelvin
    },

    "3A": {
        P_O2: 100*pascal,
        T: 543.15*kelvin
    },

    "3B": {
        P_O2: 100*pascal,
        T: 1173.15*kelvin
    },

    "3D": {
        P_O2: 100*pascal,
        T: 773.15*kelvin
    },

    "3E": {
        P_O2: 100*pascal,
        T: 973.15*kelvin
    },

    "4A": {
        P_O2: 10*pascal,
        T: 543.15*kelvin
    },

    "4B": {
        P_O2: 10*pascal,
        T: 1173.15*kelvin,
        #t_0: 369*second
    },

    "IPL": {
        P_O2: 1.33322387415 * pascal,
        T: 1273.15 * kelvin
    }
} 

def getExperimentConds(code, substitutions={}):
    """
    Get the conditions for a particular experiment.

    Parameters:
    code (String): the alpha-numeric code representing the trial in question (e.g. 1A, 2B)
    
    Returns:
    conditions: the dictionary containing all values of all variables, ready for substitution into the equation
    """
    toReturn = {**fitted_values, **experiment_constants, **(experiment_values[code])}
    # want to values in experiment_values to overwrite conflicting values already present, so this is processed last
    experiment_dict = experiment_values[code]
    for key in experiment_dict:
        toReturn[key] = experiment_dict[key]
    if toReturn.get(t_0) == None:
        toReturn[t_0] = 350 * second
    for key in substitutions:
        #print(key)
        toReturn[key] = substitutions.get(key)
    return toReturn

def getMassGain(code, massCalculator=complexMassGain, substitutions={}):
    return massCalculator(getExperimentConds(code, substitutions))

def getMassGainNumpyLambda(code, substitutions={}):
    conditions = getExperimentConds(code, substitutions)
    conditions.pop(t)
    #print(conditions)
    return getMassGainTimeLambda(conditions, modules=numpy)

def getOxideThicknessNumpyLambda(code, substitutions={}):
    conditions = getExperimentConds(code, substitutions)
    conditions.pop(t)
    print(conditions)
    return getOxideThicknessTimeLambda(conditions, modules=numpy)
