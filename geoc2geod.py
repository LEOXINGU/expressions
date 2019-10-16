from qgis.core import *
from qgis.gui import *
from numpy import sin, cos, sqrt, radians, pi, arctan

@qgsfunction(args='auto', group='Geodesy')
def geoc2geod(X, Y, Z, GRS, Axis, feature, parent):
    """
    Calculates the Geodesic (lon, lat, h) coordinates from Geocentric (X,Y,Z) coordinates.
    <h2>Example usage:</h2>
    <ul>
      <li>geoc2geod(X,Y,Z, 'wgs84', 'lon') -> lon</li>
      <li>geoc2geod(X,Y,Z, 'sirgas2000', '') -> '(lon,lat,h)'</li>
    </ul>
    """
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
        
    b = a*(1-f)
    e2 = f*(2-f) # primeira excentricidade
    e2_2 = e2/(1-e2) # segunda excentricidade
    tg_u = (a/b)*Z/sqrt(X**2 + Y**2)
    sen_u = tg_u/sqrt(1+tg_u**2)
    cos_u = 1/sqrt(1+tg_u**2)
    lon =arctan(Y/X)
    lat = arctan( (Z+ e2_2 * b * sen_u**3) / (sqrt(X**2 + Y**2) - e2 * a * cos_u**3))
    N = a/sqrt(1-(e2*sin(lat)**2))
    h = sqrt(X**2 + Y**2)/cos(lat) - N
    lon = lon/pi*180
    lat = lat/pi*180
    
    if Axis.lower() == 'lon':
        return float(lon)
    elif Axis.lower() == 'lat':
        return float(lat)
    elif Axis.lower() == 'h':
        return float(h)
    else:
        return '({:.4f}, {:.4f}, {:.4f})'.format(lon,lat,h)
