from qgis.core import *
from qgis.gui import *

@qgsfunction(args='auto', group='Topology')
def IntersectsLayer(layer_name, feature, parent):
    ''' Returns True if a feature intersects another layer's feature, else returns False.
    
        <h2>Example usage:</h2>
        <ul>
          <li>IntersectsLayer("layer_name") -> True</li>
          <li>IntersectsLayer("layer_name") -> False</li>
        </ul>'''
    Intersects = False
    geom = feature.geometry()
    if len(QgsProject.instance().mapLayersByName(layer_name)) == 1:
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    else:
        layer = QgsProject.instance().mapLayer(layer_name)
    for feat in layer.getFeatures():
            if geom.intersects(feat.geometry()):
                    Intersects = True
                    break
    return  Intersects
