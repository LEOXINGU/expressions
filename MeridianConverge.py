from qgis.core import *
from qgis.gui import *
import math


@qgsfunction(args='auto', group='Custom')
def MeridianConvergence(lon, lat, feature, parent):
    """
    Calculates the Meridian Convergence based on a Polygon Centroid.
    <h2>Example usage:</h2>
    <ul>
      <li>MerdianConvergence(lon, lat) -> -0.3451</li>
    </ul>
    """

    # Calculo do Fuso
    fuso = round((183+lon)/6.0)
    # Calculo do Meridiano Central
    MC = 6*fuso-183
    # Fator de distorcao inicial
    kappaZero = 0.9996
    # Semi-eixos do Elipsoide SIRGAS 2000
    a = 6378137.0
    b = 6356752.314140356 
    
    # Calculo da Convergencia Meridiana
    delta_lon = abs( MC - lon )
    p = 0.0001*( delta_lon*3600 )
    xii = math.sin(math.radians(lat))*math.pow(10, 4)
    e2 = math.sqrt(a*a - b*b)/b
    c5 = math.pow(math.sin(math.radians(1/3600)), 4)*math.sin(math.radians(lat))*math.pow(math.cos(math.radians(lat)), 4)*(2 - math.pow(math.tan(math.radians(lat)), 2))*math.pow(10, 20)/15
    xiii = math.pow(math.sin(math.radians(1/3600)), 2)*math.sin(math.radians(lat))*math.pow(math.cos(math.radians(lat)), 2)*(1 + 3*e2*e2*math.pow(math.cos(math.radians(lat)), 2) + 2*math.pow(e2, 4)*math.pow(math.cos(math.radians(lat)), 4))*math.pow(10, 12)/3
    cSeconds = xii*p + xiii*math.pow(p, 3) + c5*math.pow(p, 5)
    c = abs(cSeconds/3600)
    if (lon-MC)*lat < 0:
        c *= -1
    return c
