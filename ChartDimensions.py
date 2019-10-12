from qgis.core import *
from qgis.gui import *

@qgsfunction(args='auto', group='Topology')
def ChartDimensions(Dscale, DimType, UTMProjection, feature, parent):
    ''' Returns the length or heigth of a feature in meters related to a scale.
        <h2>Example usage:</h2>
        <ul>
          <li>ChartDimensions(25000, 'x', 'EPSG:21985') -> 238475.121</li>
          <li>ChartDimensions(10000, 'y', 'EPSG:31984') -> 734,876</li>
        </ul>'''
    geom = feature.geometry()
    coord = geom.asPolygon()
    # Valores max e min das coordenadas
    for feat in layer.getFeatures():
            if geom.within(feat.geometry()):
                    Situation = True
                    break
    return  coord
