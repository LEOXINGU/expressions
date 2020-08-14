from qgis.core import *
from qgis.gui import *
from math import atan, pi, sqrt
import math
from numpy import floor


# Azimutes
def azimute(A,B):
    # Cálculo dos Azimutes entre dois pontos (Vetor AB origem A extremidade B)
    if ((B.x()-A.x())>=0 and (B.y()-A.y())>0): #1o quadrante
        AzAB=atan((B.x()-A.x())/(B.y()-A.y()))
        AzBA=AzAB+pi
    elif ((B.x()-A.x())>0 and(B.y()-A.y())<0): #2o quadrante
        AzAB=pi+atan((B.x()-A.x())/(B.y()-A.y()))
        AzBA=AzAB+pi
    elif ((B.x()-A.x())<=0 and(B.y()-A.y())<0): #3o quadrante
        AzAB=atan((B.x()-A.x())/(B.y()-A.y()))+pi
        AzBA=AzAB-pi
    elif ((B.x()-A.x())<0 and(B.y()-A.y())>0): #4o quadrante
        AzAB=2*pi+atan((B.x()-A.x())/(B.y()-A.y()))
        AzBA=AzAB+pi
    elif ((B.x()-A.x())>0 and(B.y()-A.y())==0): # no eixo positivo de x (90)
        AzAB=pi/2
        AzBA=1.5*pi
    else: # ((B.x()-A.x())<0 and(B.y()-A.y())==0) # no eixo negativo de x (270)
        AzAB=1.5*pi
        AzBA=pi/2
    # Correção dos ângulos para o intervalo de 0 a 2pi
    if AzAB<0 or AzAB>2*pi:
        if (AzAB<0):
           AzAB=AzAB+2*pi
        else:
           AzAB=AzAB-2*pi
    if AzBA<0 or AzBA>2*pi:
        if (AzBA<0):
            AzBA=AzBA+2*pi
        else:
            AzBA=AzBA-2*pi
    return (AzAB, AzBA)

# Graus Decimais para Graus, Minutos, Segundos (DMS)
def dd2dms(dd, n_digits):
    if dd != 0:
        graus = int(floor(abs(dd)))
        resto = round(abs(dd) - graus, 8)
        if dd < 0:
            texto = '-' + str(graus) + '&deg;'
        else:
            texto = str(graus) + '&deg;'
        minutos = int(floor(60*resto))
        resto = round(resto*60 - minutos, 10)
        texto = texto + '{:02d}'.format(minutos) + '&apos;'
        segundos = resto*60
        if round(segundos,n_digits) == 60:
            minutos += 1
            segundos = 0
        if minutos == 60:
            graus += 1
            minutos = 0
        if n_digits < 1:
            texto = texto + '{:02d}'.format(int(segundos)) + "&quot;"
        else:
            texto = texto + ('{:0' + str(3+n_digits) + '.' + str(n_digits) + 'f}').format(segundos) + "&quot;"
        return texto
    else:
        return '0&deg;00&apos;' + ('{:0' + str(3+n_digits) + '.' + str(n_digits) + 'f}').format(0) +'&quot;'

# Convergência Meridiana
def ConvMer(pnt, SRC):
    lon = pnt.x()
    lat = pnt.y()
    # Calculo do Fuso
    fuso = round((183+lon)/6.0)
    # Calculo do Meridiano Central
    MC = 6*fuso-183
    # Pegar Semi-eixo Maior e Menor do Datum da Moldura
    distanceArea = QgsDistanceArea()
    distanceArea.setEllipsoid(SRC.ellipsoidAcronym())
    a = distanceArea.ellipsoidSemiMajor()
    b = distanceArea.ellipsoidSemiMinor()
    # Calculo da Convergencia Meridiana
    delta_lon = abs( MC - lon )
    p = 0.0001*( delta_lon*3600 )
    xii = math.sin(math.radians(lat))*math.pow(10, 4)
    e2 = math.sqrt(a*a - b*b)/b
    c5 = math.pow(math.sin(math.radians(1/3600)), 4)*math.sin(math.radians(lat))*math.pow(math.cos(math.radians(lat)), 4)*(2 - math.pow(math.tan(math.radians(lat)), 2))*math.pow(10, 20)/15
    xiii = math.pow(math.sin(math.radians(1/3600)), 2)*math.sin(math.radians(lat))*math.pow(math.cos(math.radians(lat)), 2)*(1 + 3*e2*e2*math.pow(math.cos(math.radians(lat)), 2) + 2*math.pow(e2, 4)*math.pow(math.cos(math.radians(lat)), 4))*math.pow(10, 12)/3
    cSeconds = xii*p + xiii*math.pow(p, 3) + c5*math.pow(p, 5)
    c = abs(cSeconds/3600)
    if (lon-MC)*lat < 0:
        c *= -1
    return c

# SRC do Projeto
def SRC_Projeto(output_type):
    a = QgsProject.instance()
    b = a.crs()
    if output_type == 'EPSG':
        return b.authid()
    else:
        return b.description()

@qgsfunction(args='auto', group='Custom')
def MemorialSintetico(layer_name, ini, fim, titulo, fontsize, feature, parent):
    """
    Gera o memorial descritivo sintetico a partir de uma camada de pontos do perimetro de um imovel e dos vertices inicial e final pretendido.
    O titulo da tabela pode ser inserido como string.
    <h2>Exemplo:</h2>
    <ul>
      <li>MemorialSintetico('nome_camada', ini, fim, 'titulo','fontsize') = HTML</li>
      <li>MemorialSintetico('Vertices', 1, 20, 'Area X',10) = HTML</li>
    </ul>
    """
    
    # Templates HTML
    linha = '''<tr>
      <td>Vn</td>
      <td>En</td>
      <td>Nn</td>
      <td>Ln</td>
      <td>Az_n</td>
      <td>AzG_n</td>
      <td>Dn</td>
    </tr>
'''

    texto = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
</head>
<body>
<table
 style="text-align: center; width: 100%; font-size: [FONTSIZE]px; font-family: Arial;"
 border="1" cellpadding="1" cellspacing="0">
  <tbody>
    <tr>
      <td colspan="7" rowspan="1">MEMORIAL
DESCRITIVO SINT&Eacute;TICO [TITULO]</td>
    </tr>
    <tr>
      <td colspan="1" rowspan="2">V&Eacute;RTICE</td>
      <td colspan="2" rowspan="1">COORDENADAS</td>
      <td colspan="1" rowspan="2">LADO</td>
      <td colspan="2" rowspan="1">AZIMUTES</td>
      <td colspan="1" rowspan="2">DIST&Acirc;NCIA<br>
(m)</td>
    </tr>
    <tr>
      <td>E</td>
      <td>N</td>
      <td>PLANO</td>
      <td>VERDADEIRO</td>
    </tr>
    [LINHAS]
  </tbody>
</table>
<br>
</body>
</html>
'''
    
    # Camada de Pontos
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    SRC = layer.crs()
    pnts_UTM = {}

    # Transformação de Coordenadas Geográficas para Projetadas no sistema UTM
    crsDest = QgsCoordinateReferenceSystem(SRC_Projeto('EPSG'))
    coordinateTransformer = QgsCoordinateTransform()
    coordinateTransformer.setDestinationCrs(crsDest)
    coordinateTransformer.setSourceCrs(SRC)

    for feat in layer.getFeatures():
        pnt = feat.geometry().asMultiPoint()[0]
        pnts_UTM[feat['ordem']] = [coordinateTransformer.transform(pnt), feat['tipo'], feat['codigo'], ConvMer(pnt, crsDest) ]

    # Cálculo dos Azimutes e Distâncias
    tam = len(pnts_UTM)
    Az_lista, Az_Geo_lista, Dist = [], [], []
    for k in range(tam):
        pntA = pnts_UTM[k+1][0]
        pntB = pnts_UTM[1 if k+2 > tam else k+2][0]
        Az_lista += [(180/pi)*azimute(pntA, pntB)[0]]
        ConvMerediana = pnts_UTM[k+1][3]
        Az_Geo_lista += [(180/pi)*azimute(pntA, pntB)[0]+ConvMerediana]
        Dist += [sqrt((pntA.x() - pntB.x())**2 + (pntA.y() - pntB.y())**2)]

    LINHAS = ''
    if fim == -1 or fim > tam:
        fim = tam
    for k in range(ini-1,fim):
        linha0 = linha
        itens = {'Vn': pnts_UTM[k+1][2],
                    'En': '{:,.2f}'.format(pnts_UTM[k+1][0].x()).replace(',', 'X').replace('.', ',').replace('X', '.'),
                    'Nn': '{:,.2f}'.format(pnts_UTM[k+1][0].y()).replace(',', 'X').replace('.', ',').replace('X', '.'),
                    'Ln': pnts_UTM[k+1][2] + '/' + pnts_UTM[1 if k+2 > tam else k+2][2],
                    'Az_n': dd2dms(Az_lista[k],1).replace('.', ','),
                    'AzG_n':  dd2dms(Az_Geo_lista[k],1).replace('.', ','),
                    'Dn': '{:,.2f}'.format(Dist[k]).replace(',', 'X').replace('.', ',').replace('X', '.')
                    }
        for item in itens:
            linha0 = linha0.replace(item, itens[item])
        LINHAS += linha0
    resultado = texto.replace('[LINHAS]', LINHAS).replace('[TITULO]', titulo).replace('[FONTSIZE]', str(fontsize))
    
    return resultado
