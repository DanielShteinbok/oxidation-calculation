# Oxidation of Copper Modelling

This is a library for simulation of the oxidation of copper at low partial pressures of oxygen, 
based on [the paper by Bjorck et al, 2013](https://skb.se/wp-content/uploads/2015/05/Bilaga-t-1371851_1410172-Oxidation-kinetics-of-copper-at-reduced-oxygen-partial-pressures.pdf).

## Modules
This project has three main modules: `values`, `equations` and `oxplotter`.

### equations
The `equations` module stores the equations from the paper in question, written via Sympy. 
`equations.x_substituted` is the expression for the mass gain, given experimental conditions.
There is also a convenience function, 

### values
`values` assists with manipulation of 
