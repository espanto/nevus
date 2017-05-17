#uso python explorar.py
import os
import sys
import numpy

import pandas


from data_tools import RangeToBitmap, CategoriesToBitmap


def load_data_info_old():
    """
    Fototipo
    [ -1.   1.   2.   3.   4.   5.  99.]
    99
    categorico
    """
    data_path = 'data/'
    f=open( data_path+'tipoDatos.txt', 'rt' )
    d = dict()
    l = list()
    for line in f:
        # Attribute name
        attribute_name = line.strip()
        if len(attribute_name) > 0  and  attribute_name[0] == '#' : continue
        l.append(attribute_name)
        # Line to be ignored
        #line = f.readline()
        # Values to be excluded, if any
        line = f.readline().strip()
        if len(line) == 0:
            to_be_excluded = list()
        else:
            to_be_excluded = line.split()
        # Attribute type
        line = f.readline()
        attribute_type = line.strip()
        d[attribute_name] = { 'excluded' : to_be_excluded, 'type' : attribute_type }
    f.close()
    return l,d
# -----------------------------------------------------------------------------------------

def load_data_info( filename=None ):
    """
        N_ID;categorico;;;;;
        Sexo;categorico;;;;;
        Edad;rango;;0;99;;20;
        Fototipo;categorico;99;;;;
        Ojos_R;categorico;99;;;;
        Pelo R;categorico;99;;;;
    """
    l=list()
    d=dict()
    f=open( filename, 'rt' )
    for line in f:
        parts=line.split(';')
        attribute_name=parts[0].strip()
        attribute_type=parts[1].strip()
        if len(parts[2]) > 0:
            excluded_values=[ x for x in parts[2].split() ]
        else:
            excluded_values=list()
        min_value=float(parts[3].strip()) if len( parts[3] ) > 0 else None
        max_value=float(parts[4].strip()) if len( parts[4] ) > 0 else None
        num_intervals=float(parts[5].strip()) if len( parts[5] ) > 0 else None
        if len(parts[6]) > 0:
            range_of_values=[ float(x) for x in parts[6].split() ]
        else:
            range_of_values=None
        l.append(attribute_name)
        d[attribute_name]={ 'type' : attribute_type,
                            'excluded' : excluded_values,
                            'min' : min_value,
                            'max' : max_value,
                            'num_intervals' : num_intervals,
                            'range' : range_of_values };
    f.close()
    return l,d
# -----------------------------------------------------------------------------------------

def save_data_info( filename=None, l=None, d=None ):
    f=open( filename, 'wt' )
    for key in keys:
        d = data_info[key]
        f.write( "%s;%s;%s;%s;%s;%s;%s;\n" % (
                    key,
                    d['type'],
                    " ".join( "{:s}".format(x) for x in d['excluded'] ),
                    d['min'] if d['min'] is not None else "",
                    d['max'] if d['max'] is not None else "",
                    d['num_intervals'] if d['num_intervals'] is not None else "",
                    ( " ".join( "{:s}".format(str(x)) for x in d['range'] ) if  d['range'] is not None else "" ),
               ) )
    f.close()
# -----------------------------------------------------------------------------------------

def preprocess_data( df, data_info, verbose=0 ):
    """
    """
    for column in df.columns:
        X = df[column]
        X.fillna( value=-1, inplace=True )
        X = numpy.array( X )
        if verbose > 1: print( column )
        try:
            U = numpy.unique( X )
        except:
            print( "ERROR in data" )
            print( X )
            for x in X: print( x, type(x) )
            raise Exception()
        U.sort()
        if verbose > 0: print( U )
        if column in data_info:
            t = data_info[column]['type']
            if t in [ 'categorico', 'numerico' ] :
                l=list()
                excl = data_info[column]['excluded']
                for c in U:
                    try:
                        vc = float(c)
                    except:
                        vc = c
                    append=True
                    if vc == -1.0: # Change this according to X.fillna( value=-1, inplace=True )
                        append=False
                    else:
                        for e in excl:
                            try:
                                ve=float(e)
                                if vc == ve:
                                    append=False
                                    break
                            except:
                                if c == e: # Can fail when comparing values of different types
                                    append=False
                                    break
                    if append: l.append(c)
                data_info[column]['range'] = l

                if t == 'numerico' :
                    data_info[column]['min'] = l[0]
                    data_info[column]['max'] = l[-1]

            elif t == 'rango' :
                data_info[column]['min'] = U[0]
                data_info[column]['max'] = U[-1]
            else:
                raise Exception( 'Unknown data type <' + t + '>' )
        else:
            raise Exception( "Column %s found in the data but not found in the data definition" % column )
# -----------------------------------------------------------------------------------------


if __name__ == '__main__' :
    data_path = 'data/'

    keys,data_info=load_data_info( data_path+'tipoDatos.csv' )

    save_data_info( data_path+'test-1.csv', keys, data_info )

    df = pandas.read_csv( data_path+'dataBRASblancos.csv', sep=';', delimiter=';', na_filter=True )
    preprocess_data( df, data_info, verbose=0 )

    save_data_info( data_path+'test-2.csv', keys, data_info )

    """
    if type(U[0]) == numpy.float64  and  len(U) > 10 :
        rtb = RangeToBitmap( bounds=[ U[0],U[-1] ], num_bits=10 )
        print( rtb.x_range )
    else:
        ctb = CategoriesToBitmap( subset=X, to_be_excluded=[-1], mass=0.97 )
        print( ctb.values )
    """
