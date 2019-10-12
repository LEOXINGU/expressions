from qgis.core import *
from qgis.gui import *

@qgsfunction(args='auto', group='Custom')
def ProjectCRS(output_type, feature, parent):
    """
    Return the descriptive name  or the EPSG code of the Project's CRS.
    <h2>Example usage:</h2>
    <ul>
      <li>ProjectCRS('EPSG') -> EPSG:4674</li>
      <li>ProjectCRS('') -> SIRGAS 2000 / UTM 25 S</li>
    </ul>
    """
    a = QgsProject.instance()
    b = a.crs()
    if output_type == 'EPSG':
        return b.authid()
    else:
        return b.description()
