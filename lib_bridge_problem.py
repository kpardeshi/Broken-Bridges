#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 13:28:28 2018

@author: kaustubhpardeshi
"""

import class_bridge_problem

def n_connected( v ):
    """Calculates the number of connected graphs supported by v vertices"""
    calc_obj = class_bridge_problem.cached_data()
    return( calc_obj.n_connected( v ) )
    
    
def p_connected( v ):
    """Calculates the probability that a graph chosen at random with v vertices
    is connected given any given edge 0.5 probability of existing"""
    e_max   = v * ( v - 1 )/2
    n_total = 2**e_max 
    return( n_connected( v )/n_total )
        

#for v = 5  ( 125 + 222 + 205 + nCr( 10, 7 ) + nCr( 10, 8 ) + 10 + 1  )/2**10 =  0.7109375   
#for v = 4  38/64 = 0.59375
#for v = 3 0.5
#for v = 2 0.5
#for v = 1 1