
import os
import sys
import numpy

import ann 



def load_data( filename=None ):
    f = open( filename, 'rt' )
    line = f.readline()
    dim_x, dim_y = [int(v) for v in line.split()]
    X = list()
    Y = list()
    for line in f:
        parts = line.split()
        X.append( [ float(x) for x in parts[:dim_x] ] )
        Y.append( [ float(y) for y in parts[dim_x:] ] )
    X = numpy.array(X)
    Y = numpy.array(Y)
    f.close()

    return X,Y


if __name__ == '__main__':

    modelname=None
    data_filename=None

    for i in range(len(sys.argv)):
        if   sys.argv[i] == '--model' : modelname     = sys.argv[i+1]
        elif sys.argv[i] == '--data'  : data_filename = sys.argv[i+1]
        

    if modelname is None: raise Exception( "No modelname was provided!" )
    if data_filename is None: raise Exception( "No data filename was provided!" )


    X,Y=load_data( data_filename )

    
    nn = ann.load( modelname=modelname )
    if nn is None:
        nn = ann.ANN( modelname=modelname )

    Z=numpy.zeros( len(Y), dtype=int )
    if modelname[:12] == 'net-NRASmut-':
        yy=Y[:,3]
        print( 3 )
    else:
        yy=Y[:,1]
        print( 1 )
    Z[ yy == 1.0 ] = 1
    
    iterations=1000
    nn.fit( X, Z, X, Z, iterations, iterations )
