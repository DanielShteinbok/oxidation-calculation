#!/usr/bin/env python

import numpy
#import matplotlib
from matplotlib import pyplot as plt
import values
import equations
from sympy.physics.units import pascal, kelvin, second
import sympy

def plotMassGainNumpy(code, substitutions={}):
    times = numpy.arange(0, 8*60*60, 1000)
    lamfunc, units_expression = values.getMassGainNumpyLambda(code, substitutions)
    fig, axis = plt.subplots()
    axis.plot(times, lamfunc(times))
    conditions = values.getExperimentConds(code, substitutions)
    plt.title("Pressure: " + str(conditions[equations.P_O2]/pascal) + ", Temperature: " + str(conditions[equations.T]/kelvin))
    #plt.show()
    #TODO return the figure and the units
    return fig, sympy.simplify(units_expression.subs([(equations.t,second), (equations.e, 1), (equations.F_p, 1)])).as_coeff_Mul()[1]/(-1 + sympy.sqrt(5))

def plotThicknessNumpy(code, start=0, stop=28800, step=1000, substitutions={}):
    times = numpy.arange(start, stop, step)
    lamfunc, units_expression = values.getOxideThicknessNumpyLambda(code, substitutions)
    fig, axes = plt.subplots()
    axes.plot(times, lamfunc(times))
    conditions = values.getExperimentConds(code, substitutions)
    plt.title("Pressure: " + str(conditions[equations.P_O2]/pascal) + ", Temperature: " + str(conditions[equations.T]/kelvin))
    final_units = sympy.simplify(units_expression.subs([(equations.t,second), (equations.e, 1), (equations.F_p, 1)])).as_coeff_Mul()[1]/(-1 + sympy.sqrt(5))
    axes.set_ylabel("Thickness, " + str(final_units))
    axes.set_xlabel("Time, seconds")
    #plt.show()
    #TODO return the figure and the units
    return fig, sympy.simplify(units_expression.subs([(equations.t,second), (equations.e, 1), (equations.F_p, 1)])).as_coeff_Mul()[1]/(-1 + sympy.sqrt(5))
