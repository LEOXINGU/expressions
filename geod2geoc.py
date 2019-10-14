from qgis.core import *
from qgis.gui import *
from numpy import sin, cos, sqrt, radians, pi

@qgsfunction(args='auto', group='Geodesy')
def geod2geoc(lon, lat, h, GRS, Axis, feature, parent):
    """
    Calculates the Geocentric (X,Y,Z) coordinates.
    <h2>Example usage:</h2>
    <ul>
      <li>geod2geoc(lon, lat, h, GRS, axis) -> (X,Y,Z)</li>
      <li>geod2geoc(-21.456, 12.345, 345.981, 'sirgas2000', 'x') -> 113545645.1225</li>
    </ul>
    """
    lon = radians(lon)
    lat = radians(lat)
    
    # GRS
    if GRS.lower() == 'corrego':
        a = 6378388.
        f = 1/297.
    elif GRS.lower() == 'sad69':
        a = 6378160.
        f = 1/298.25
    elif GRS.lower() == 'grs80':
        a = 6378137.
        f = 1/298.257222100882711243
    elif GRS.lower() == 'wgs84':
        a = 6378137.
        f = 1/298.2572235630
    elif GRS.lower() == 'sirgas2000':
        a = 6378137.
        f = 1/298.257222101
    else:
        a = 6378137.
        f = 1/298.257222101
    
    e2 = f*(2-f)
    N = a/sqrt(1-(e2*sin(lat)**2))
    X = (N+h)*cos(lat)*cos(lon)
    Y = (N+h)*cos(lat)*sin(lon)
    Z = (N*(1-e2)+h)*sin(lat)
    
    if Axis.lower() == 'x':
        return float(X)
    elif Axis.lower() == 'y':
        return float(Y)
    elif Axis.lower() == 'z':
        return float(Z)
    else:
        return '({:.4f}, {:.4f}, {:.4f})'.format(X,Y,Z)
