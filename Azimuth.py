from qgis.core import *
from qgis.gui import *
from math import atan, pi

@qgsfunction(args='auto', group='Custom')
def Azimuth2(X, Y, feature, parent):
    ''' Returns the azimuth from X and Y values.
    
        <h2>Example usage:</h2>
        <ul>
          <li>Azimuth2(0, 1) -> pi/2</li>
          <li>Azimuth2(-2,0) -> pi</li>
        </ul>'''
    if (X>=0 and Y>0): #1� quadrante
        AzAB=atan(X/Y)
    elif (X>0 and Y<0): #2� quadrante
        AzAB=pi+atan(X/Y)
    elif (X<=0 and Y<0): #3� quadrante
        AzAB=atan(X/Y)+pi
    elif (X<0 and Y>0): #4� quadrante
        AzAB=2*pi+atan(X/Y)
    elif (X>0 and Y==0): # no eixo positivo de x (90�)
        AzAB=pi/2
    else: # (X<0 andY==0) # no eixo negativo de x (270�)
        AzAB=1.5*pi
    # Corre��o dos �ngulos para o intervalo de 0 a 2pi
    if AzAB<0 or AzAB>2*pi:
        if (AzAB<0):
           AzAB=AzAB+2*pi
        else:
           AzAB=AzAB-2*pi
    if X == 0 and Y==0:
        AzAB = None
    return AzAB
