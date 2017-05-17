#uso python FeatureExtractor.py >> data
import os
import sys
import numpy
import pandas


import data_tools


from explorar import  load_data_info


class FeatureExtractor:
    """
        { 'type' : attribute_type,
          'excluded' : excluded_values,
          'min' : min_value,
          'max' : max_value,
          'num_intervals' : num_intervals,
          'range' : range_of_values }
    """
    
    def __init__( self, filename_with_data_description=None ):

        self.columns, self.data_info = load_data_info( filename=filename_with_data_description )

        self.extractors = dict()
        self.size=0

        for column in self.columns:

            di = self.data_info[column]
            t = self.data_info[column]['type']

            if t == 'categorico':
                extractor = data_tools.CategoriesToBitmap( values=di['range'] )

            elif t == 'numerico':
                extractor = data_tools.PercentilesToBitmap( values=di['range'] )

            elif t == 'rango':
                min_value = di['min']
                max_value = di['max']
                num_intervals = di['num_intervals']
                if num_intervals is None or num_intervals <= 0:
                    num_intervals = 10
                extractor = data_tools.RangeToBitmap( bounds=[ min_value, max_value ], num_bits=num_intervals )

            self.extractors[column] = extractor
            self.size += len(extractor)
    # -------------------------------------------------------------------------------------------------

    def __len__(self): return self.size
    # -------------------------------------------------------------------------------------------------

    def convert( self, df=None, index=-1 ):
        
        x = numpy.zeros( self.size )
        i = 0
        for column in self.columns:
            extractor = self.extractors[column]
            v = df[column][index]     
            if v != v :
                #raise Exception( "v is nan! -- %f " % v );
                if extractor is data_tools.CategoriesToBitmap:
                    v = None
                else:
                    v = -1
            z = extractor.bitmap( v )
            #print( column )
            #print( type(extractor) )
            #print( type(v), v )
            #print( type(z), z )
            for k in range(len(z)):
                if z[k] is None or z[k] is numpy.nan: sys.stderr.write( "ERROR: ", z, '\n' )
            x[i:i+len(extractor)] = z[:]
            i+=len(extractor)
        #
        return x
    # -------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    data_path = 'data/' 
    fe_input  = FeatureExtractor( filename_with_data_description=data_path+'input_variables_2.2.csv' )
    fe_output = FeatureExtractor( filename_with_data_description=data_path+'output_variables.csv' )
    df = pandas.read_csv( data_path+'dataBRASblancos.csv', sep=';', delimiter=';', na_filter=True )

    print( len(fe_input), len(fe_output) )
    for i in range(len(df)): 
        x = fe_input.convert( df, i )
        y = fe_output.convert( df, i )
        #print( "%9.2f  " % x.sum(), " ".join( "{:.6f}".format(v) for v in x ) )
        if y.sum() > 0.0:
            print( " ".join( "{:.6f}".format(v) for v in x ),  "  ", " ".join( "{:.6f}".format(v) for v in y ) )
