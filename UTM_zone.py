from qgis.core import *
from qgis.gui import *
import math

@qgsfunction(args=0, group='Custom', usesgeometry=True)
def GetUtmZone(feature, parent):
        geom = feature.geometry()
        coord = geom.asPoint()
        lon = coord.x()
        lat = coord.y()
        # Calculo do Fuso
        fuso = round((183+lon)/6.0)
        # Hemisferio
        hemisf = 'N' if lat>= 0 else 'S'
    return str(fuso) + hemisf
