#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 13:41:35 2018

@author: kaustubhpardeshi
"""

import math

class cached_data:
    """object to store the results of calculations"""
    def __init__( self ):
        self.data_cache = {}
        
    def n_connected( self, v ):
        """retrieves cached calculation otherwise recomputes and stores"""
        if v < 1 or type( v ) != int:
            raise ValueError( 'vertex number has to be a natural number' )
        elif v == 1:
            return( 1 )
        elif v == 2:
            return( 1 )
        else:
            try:
                bp_class = self.data_cache[ v ]
            except KeyError:
                bp_class             = bridge_problem( v )
                bp_class.cached_data = self
                bp_class.get_n_connected()
                self.data_cache[ v ] = bp_class
            return( bp_class.n_connected )
                    


class bridge_problem:
    """examines the scenario if v treehouses were all connected with each other
    by bridges, but after a storm each individual bridge survives with probability
    0.5, then what is the probability all houses still remain connected in some
    way"""
    def __init__( self, v ):
        self.v                 = v
        self.e_max             = v * ( v - 1 )/2
        self.n_total           = 2**( self.e_max )
        self.n_connected       = float( 'inf' ) 
        self.p_connected       = float( 'inf' )
        self.n_mult_components = float( 'inf' )
        self.n_components      = [ float( 'inf' ), float( 'inf' ) ]
        self.cached_data       = cached_data()
        self.grouping_data     = {}
        
    def get_p_connected( self ):
        """calculates the probability of remaining connected"""
        self.get_n_connected()
        self.p_connected = self.n_connected/self.n_total
        
    def get_n_connected( self ):
        """calculates the number of connected graphs"""
               
        self.get_n_mult_components()
        self.n_connected = self.n_total - self.n_mult_components
        
    def get_n_mult_components( self ):
        """calculates the number of graphs with multiple components 
        ( not connected )"""
        self.n_mult_components = 0
        self.get_n_components()
         
        for i in range( 2, self.v + 1 ):
            self.n_mult_components += self.n_components[ i ]
            
    def get_n_components( self ):
        """calculates the number of graphs with each possible number of 
        components"""
        for nc in range( 2, self.v + 1 ):
            self.n_components.append( 0 )
            self.n_comp( nc )
        #if self.v == 10:
         #   import pdb; pdb.set_trace()             
            
    def n_comp( self, nc ):
        """given an input number of components nc, calculates the number of possible
        graphs"""
        grouping = [ 0 for i in range( nc ) ] 
        self.n_graphs_recursively( 0, nc, grouping )
        
    def n_graphs_recursively( self, j, nc, grouping ):
        """recursively build configurations of v vertices divided into nc components
        and calculate the number of graphs ( cardinality ) they allow"""
        #import pdb; pdb.set_trace()  
        if( j == ( nc - 1 ) ):
            #in this case grouping is almost built and we are ready to calculate
            #its cardinality
            grouping[ j ] = self.v - sum( grouping[ 0 : j ] )
            self.n_components[ nc ] += self.grouping_cardinality( grouping )
        else:
            #build range of loop such that we go through each possible number of 
            #vertices in components such that we allow at least 1 vertex in each
            #component
            v_left = self.v - sum( grouping[ 0 : j ] )
            lower_limit = math.ceil( v_left/( nc - j ) )
            if j > 0:
                prev_v = grouping[ j - 1 ]
            else:
                prev_v = float( 'inf' )
            upper_limit = min( prev_v, v_left - ( nc - ( j + 1 ) ) )
            #go one level deeper into the next component and recurse
            for k in range( lower_limit, upper_limit + 1 ):
                grouping[ j ] = k
                self.n_graphs_recursively( j + 1, nc, grouping )
                
    def grouping_cardinality( self, grouping ):
        """calculates the number of graphs supported by the inputted grouping"""
        grouping_cardinality = 1
        #import pdb; pdb.set_trace()
        i = 0
        v_left = self.v
        len_grouping = len( grouping )
        while( i < len_grouping ):
            size = grouping[ i ]
            #Figure out how many components we have of the same length
            same_size_comps = 0
            grouping_combs  = 1
            for comp_size in grouping[ i : ]:
                if( comp_size != size ):
                    break
                i += 1
                same_size_comps += 1
                grouping_combs  *= self.nCr( v_left, size )
                v_left          -= size
                
            grouping_combs       /= math.factorial( same_size_comps )
            grouping_cardinality *= grouping_combs * \
                                    ( self.cached_data.n_connected( size ) )**( same_size_comps )

        try:
            self.grouping_data[ len_grouping ][ str( grouping ) ] = grouping_cardinality
        except KeyError:
            self.grouping_data[ len_grouping ] = {}
            self.grouping_data[ len_grouping ][ str( grouping ) ] = grouping_cardinality
        return( grouping_cardinality )
    
    def nCr( self, n, r):
        f = math.factorial
        return( f(n) / f(r) / f(n-r) )    
                
                                            
            
                
        
        
        