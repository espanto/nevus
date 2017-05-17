#uso nohup python test-ann-tt.py --model net-NRASmut-02  --data data >log/OUT-NRASmut.txt >>log/ERR-NRASmut.txt     &
#uso nohup python test-ann-tt.py --model net-BRAFmut-02  --data data >log/OUT-BRAFmut.txt >>log/ERR-BRAFmut.txt     &
import os
import sys
import numpy

import ann 
from sklearn.model_selection import train_test_split


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
    print(X.shape)
    print(Y.shape)

    
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
    


    X_train,X_test,Z_train,Z_test = train_test_split( X, Z, test_size=0.25 )

    iterations=1000
    nn.fit( X_train, Z_train, X_train, Z_train, iterations, iterations )

    # Test prediction

    y_pred = nn.predict( X_test )

    test_accuracy = ( 100.0 * (Z_test == y_pred).sum() ) / len(Z_test)

    print( "Artificial Neural Networks classifier " )
    print( "%d missclassified samples from %d" % ( (Z_test != y_pred).sum(), len(Z_test) ) )
    print( "Accuracy = %.1f%%" % test_accuracy )

