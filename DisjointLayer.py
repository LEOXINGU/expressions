from qgis.core import *
from qgis.gui import *

@qgsfunction(args='auto', group='Topology')
def DisjointLayer(layer_name, feature, parent):
    ''' Returns True if a feature is within another layer's feature, else returns False.
        <h2>Example usage:</h2>
        <ul>
          <li>DisjointLayer("layer_name") -> True</li>
          <li>DisjointLayer("layer_name") -> False</li>
        </ul>'''
    Situation = False
    geom = feature.geometry()
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    for feat in layer.getFeatures():
            if geom.intersects(feat.geometry()):
                    Situation = True
                    break
    return  not Situation
