# Oxidation of Copper Modelling

This is a library for simulation of the oxidation of copper at low partial pressures of oxygen, 
based on [the paper by Bjorck et al, 2013](https://skb.se/wp-content/uploads/2015/05/Bilaga-t-1371851_1410172-Oxidation-kinetics-of-copper-at-reduced-oxygen-partial-pressures.pdf).

## Modules
This project has three main modules: `values`, `equations` and `oxplotter`.

### equations
The `equations` module stores the equations from the paper in question, written via Sympy. 
`equations.x_substituted` is the expression for the mass gain, given experimental conditions.
There is also a convenience function, `complexMassGain(conds)` which is equivalent to `x_substituted.evalf(subs=conds)`.

Generally, you will mostly not interact directly with `equations`. Instead, use `values` for calculation and `oxplotter` for easy plotting.

Many functions, including `complexMassGain`, require a python dictionary of conditions. The keys are Sympy `Symbol` objects defined in `equations`.
For example, the time condition can be set to 1 minute by passing a condition: `{<other conditions>..., equations.t : 60*sympy.physics.units.second}`.
Many of these same objects are accessible from `values` (i.e. `values.t is equations.t` evaluates to `True`), but it is preferred to always access conditions from `equations`
because all conditions present in the equations exist in that namespace (and may not all be in `values`)

### values
`values` stores actual values with units to assign to each variable in the equations, 
provides a convenience function to generate the correct dictionary of conditions in the necessary format, 
and provides further convenience functions to combine the condition-generating step and function calls of some of the 
useful `equations` functions into one step.

The constants to be put into the conditions dictionary are separated into three groups: *fitted values*, *experiment values* and *experiment constants*.
Here are explanations for each of these groups:

#### fitted values:
This includes all the "magic values" that make the model adhere to reality, chiefly the values that were fitted to experimental points by the authors.
It also includes universal constants. Here is a list of all values included in this section:
* $A_1$, the amplitude factor for the first term of the Arrhenius expression for the parabolic regime rate constant
* $E_1$, the activation energy for the first term of the Arrhenius expression for the parabolic regime rate constant
* $A_2$, the amplitude factor for the second term of the Arrhenius expression for the parabolic regime rate constant
* $E_2$, the activation energy for the second term of the Arrhenius expression for the parabolic regime rate constant
* $n_p$, the power law exponent for the parabolic regime
* $A_l$, the amplitude factor for the Arrhenius expression for the linear regime rate constant
* $E_l$, the activation energy for the Arrhenius expression for the linear regime rate constant
* $n_l$, the power law exponent for the linear regime
* $F_p$, the scale factor for the rate constant for the parabolic regime
* $R$, the universal gas constant
* $e$, Euler's constant

#### experiment values:
These are the values that differ per experiment. The values are stored in dictionaries within a larger dictionary, where an experiment "code" is the key and the dictionary of conditions is the value. The experiment code is a string to refer to a particular experiment run by Bjorck et al (they had codes 1A, 1B, 2A, 2B, 2C ... etc.). 
There is also a code "IPL" which will refer to the most commonly-used conditions at Infinite Potential Labs when a constant process for oxidation is established.
These are, at a minimum, $T$ and $P_{O_2}$, but can also include $t_0$ (an offset time to represent oxidation that occurred before the experiment began), $t$ (the time used for oxidation)
or anything else. Upon retrieval by `getExperimentConds`, the conditions listed in this section override all conflicting conditions, except those specifically supplied by the caller.

#### experiment constants:
These are values kept for all experiments done by Bjorck et al, and the particular reference temperatures and pressures chosen by them. 
The only value in here that would actually change from experiment to experiment is $t$, but it is here because Bjorck et al used a time of 8 hours for all their experiments.
This is overriden by whatever $t$ is specified in the *experiment values* section.

To get the experiment conditions, use `getExperimentConds(code, substitutions)`, where `code` is a string with the experiment code, and `substitutions` is a dictionary containing any desired 
substitution (where the key is a `Symbol` defined in `equations`, and the value is the desired value to give, multiplied by the correct units from `sympy.physics.units`). 
If nothing is passed to `substitutions`, then the function simply returns the exact conditions used in the experiment in question.

The result of `getExperimentConds` can be directly passed into the functions in `equations`. For example, to get the mass gain at the end of experiment 1B (8 hours):

``` python-console
>>> equations.complexMassGain(values.getExperimentConds("1B"))
0.02578697522472*gram/centimeter**2
```

To get the mass gain if 1B were performed at 10 Pascal partial pressure of O2 for 1 minute:

``` python-console
>>> from sympy.physics.units import second, pascal
>>> equations.complexMassGain(values.getExperimentConds("1B", {equations.t: 60*second, equations.P_O2: 10*pascal}))
4.94892428171134e-6*gram/centimeter**2
```

Instead of calling a function to generate the conditions, then another to perform the calculation, there are convenience functions in `values` that do both steps in one.
Namely, `getMassGain` calls `equations.complexMassGain` and `values.getExperimentConds`:

``` python-console
>>> values.getMassGain("1B", substitutions={equations.t: 60*second, equations.P_O2: 10*pascal})
4.94892428171134e-6*gram/centimeter**2
```

There is also a possiblity to specify a different algorithm for calculating the mass gain with this fuction:

``` python-console
>>> values.getMassGain("1B", massCalculator=equations.linearMassGain, substitutions={equations.t: 60*second, equations.P_O2: 10*pascal})
4.94893561868091e-6*gram/centimeter**2
```
This calculates the mass gain using the linear approximation rather than the complete formula.

