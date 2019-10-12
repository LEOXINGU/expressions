from qgis.core import *
from qgis.gui import *
from numpy import array

@qgsfunction(args='auto', group='Custom')
def AggregateLayerData(layer_name, field_name, AggType, feature, parent):
    ''' Returns the Aggregate function of a layer's field.
        <h2>Example usage:</h2>
        <ul>
          <li>AggregateLayerData('ayer_name', 'field_name', 'sum') ->Sum of values</li>
          <li>AggregateLayerData('ayer_name', 'field_name', 'min') ->Min of values</li>
          <li>AggregateLayerData('ayer_name', 'field_name', 'max') ->Max of values</li>
          <li>AggregateLayerData('ayer_name', 'field_name', 'mean') ->Mean of values</li>
          <li>AggregateLayerData('ayer_name', 'field_name', 'std') ->Standard Deviation of values</li>
        </ul>'''
    lista = []
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    for feat in layer.getFeatures():
        att = feat[field_name]
        if att:
            lista += [att]
    if AggType == 'sum':
        return  float((array(lista)).sum())
    elif AggType == 'min':
        return  float((array(lista)).min())
    elif AggType == 'max':
        return  float((array(lista)).max())
    elif AggType == 'mean':
        return  float((array(lista)).mean())
    elif AggType == 'std':
        return  float((array(lista)).std())
    else:
        return None
