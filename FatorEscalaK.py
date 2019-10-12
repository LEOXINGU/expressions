from qgis.core import *
from qgis.gui import *
import math

@qgsfunction(args='auto', group='Custom')
def FatorEscalaK(layer_name, feature, parent):
    """
    Calculates the Kappa Factor based on a Polygon Centroid.
    <h2>Example usage:</h2>
    <ul>
      <li>FatorEscalaK('layer_name') -> 0.99138</li>
    </ul>
    """
    
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    SRC = layer.crs()

    # Pegar centroide da moldura
    for feat in layer.getFeatures():
        feat1 = feat
        break
    geom = feat1.geometry()
    centroide = geom.centroid().asPoint()

    # Verificar os SRC da moldura
    if not SRC.isGeographic():
        # Transformar Coordenadas Projetadas do sistema UTM para geograficas
        crsDest = QgsCoordinateReferenceSystem('EPSG:4674')
        coordinateTransformer = QgsCoordinateTransform()
        coordinateTransformer.setDestinationCrs(crsDest)
        coordinateTransformer.setSourceCrs(SRC)
        centroide = coordinateTransformer.transform(centroide)

    # Pegar coordenadas do Centroide
    lon = centroide.x()
    lat = centroide.y()
    
    # Calculo do Fuso
    fuso = round((183+lon)/6.0)
    # Calculo do Meridiano Central
    MC = 6*fuso-183
    
    kappaZero = 0.9996 # Fator de distorcao inicial
    b = math.cos(math.radians(lat))*math.sin(math.radians(lon - MC))
    k = kappaZero/math.sqrt(1 - b*b)
    return k
