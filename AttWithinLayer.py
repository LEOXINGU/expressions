from qgis.core import *
from qgis.gui import *

@qgsfunction(args='auto', group='Topology')
def AttWithinLayer(layer_name, att, feature, parent):
    ''' Returns the attribute of other layer if the feature is within the layer, else returns NULL.
        <h2>Example usage:</h2>
        <ul>
          <li>AttWithinLayer('layer_name', 'att_name') -> 'test''</li>
          <li>AttWithinLayer('layer_name', 'att_name') -> 10</li>
        </ul>'''
    geom = feature.geometry()
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    for feat in layer.getFeatures():
            if geom.within(feat.geometry()):
                return feat[att]
                break
            else:
                return None
