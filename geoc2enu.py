from qgis.core import *
from qgis.gui import *
from numpy import matrix, sin, cos, radians

def geod2ecef(lon, lat, h, a, f, deg=True):
    if deg:
        lon = radians(lon)
        lat = radians(lat)
    e2 = f*(2-f) # primeira excentricidade
    N = a/sqrt(1-(e2*sin(lat)**2))
    X = (N+h)*cos(lat)*cos(lon)
    Y = (N+h)*cos(lat)*sin(lon)
    Z = (N*(1-e2)+h)*sin(lat)
    return (X,Y,Z)

@qgsfunction(args='auto', group='Geodesy')
def geoc2enu(X, Y, Z, lon0, lat0, h0, GRS, Axis, feature, parent):
    """
    Calculates the sum of the two parameters value1 and value2.
    <h2>Example usage:</h2>
    <ul>
      <li>my_sum(5, 8) -> 13</li>
      <li>my_sum("field1", "field2") -> 42</li>
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
        
    Xo, Yo, Zo = geod2ecef(lon0, lat0, h0, a, f)
    
    lon = radians(lon0)
    lat = radians(lat0)

    Rot = matrix(
    [[-sin(lon),                  cos(lon),                            0],
     [-cos(lon)*sin(lat),      -sin(lon)*sin(lat),         cos(lat)],
     [ cos(lon)*cos(lat),       sin(lon)*cos(lat),        sin(lat)]]
    )

    V = matrix(
    [[X - Xo], [Y-Yo], [Z-Zo]]
    )
    
    R = Rot*V
    E = R[0,0]
    N = R[1,0]
    U = R[2,0]
    
    if Axis.lower() == 'e':
        return float(E)
    elif Axis.lower() == 'n':
        return float(N)
    elif Axis.lower() == 'u':
        return float(U)
    else:
        return '({:.4f}, {:.4f}, {:.4f})'.format(E,N,U)
