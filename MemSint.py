from qgis.core import *
from qgis.gui import *
from math import atan, pi, sqrt
import math


# Azimutes
def azimute(A,B):
    # Cálculo dos Azimutes entre dois pontos (Vetor AB origem A extremidade B)
    if ((B.x()-A.x())>=0 and (B.y()-A.y())>0): #1º quadrante
        AzAB=atan((B.x()-A.x())/(B.y()-A.y()))
        AzBA=AzAB+pi
    elif ((B.x()-A.x())>0 and(B.y()-A.y())<0): #2º quadrante
        AzAB=pi+atan((B.x()-A.x())/(B.y()-A.y()))
        AzBA=AzAB+pi
    elif ((B.x()-A.x())<=0 and(B.y()-A.y())<0): #3º quadrante
        AzAB=atan((B.x()-A.x())/(B.y()-A.y()))+pi
        AzBA=AzAB-pi
    elif ((B.x()-A.x())<0 and(B.y()-A.y())>0): #4º quadrante
        AzAB=2*pi+atan((B.x()-A.x())/(B.y()-A.y()))
        AzBA=AzAB+pi
    elif ((B.x()-A.x())>0 and(B.y()-A.y())==0): # no eixo positivo de x (90º)
        AzAB=pi/2
        AzBA=1.5*pi
    else: # ((B.x()-A.x())<0 and(B.y()-A.y())==0) # no eixo negativo de x (270º)
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

# Graus Decimais para DMS
def DD2DMS(dd):
    is_positive = dd >= 0
    dd = abs(dd)
    minutes,seconds = divmod(dd*3600,60)
    degrees,minutes = divmod(minutes,60)
    degrees = str(int(degrees)) if is_positive else '-' + str(int(degrees))
    minutes = int(minutes)
    return degrees + "&deg;" + str(minutes).zfill(2) + "\'" + ("{:.1f}".format(seconds)).zfill(4) + '\"'

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

linha = '''
<tr style="">
      <td
 style="border-style: none solid solid; border-color: -moz-use-text-color windowtext windowtext; border-width: medium 1pt 1pt; padding: 0cm 5.4pt; width: 54.15pt;"
 width="72">
      <p class="MsoNormal"
 style="margin-bottom: 0.0001pt; text-align: center; line-height: normal;"
 align="center"><span
 style="font-size: 10pt; font-family: &quot;Arial&quot;,sans-serif;">Vn<o:p></o:p></span></p>
      </td>
      <td
 style="border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; border-width: medium 1pt 1pt medium; padding: 0cm 5.4pt; width: 78.35pt;"
 width="104">
      <p class="MsoNormal"
 style="margin-bottom: 0.0001pt; text-align: center; line-height: normal;"
 align="center"><span
 style="font-size: 10pt; font-family: &quot;Arial&quot;,sans-serif;">En<o:p></o:p></span></p>
      </td>
      <td
 style="border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; border-width: medium 1pt 1pt medium; padding: 0cm 5.4pt; width: 72.1pt;"
 width="96">
      <p class="MsoNormal"
 style="margin-bottom: 0.0001pt; text-align: center; line-height: normal;"
 align="center"><span
 style="font-size: 10pt; font-family: &quot;Arial&quot;,sans-serif;">Nn<o:p></o:p></span></p>
      </td>
      <td
 style="border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; border-width: medium 1pt 1pt medium; padding: 0cm 5.4pt; width: 130pt;"
 width="74">
      <p class="MsoNormal"
 style="margin-bottom: 0.0001pt; text-align: center; line-height: normal;"
 align="center"><span
 style="font-size: 10pt; font-family: &quot;Arial&quot;,sans-serif;">Ln<o:p></o:p></span></p>
      </td>
      <td
 style="border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; border-width: medium 1pt 1pt medium; padding: 0cm 5.4pt; width: 75.4pt;"
 width="101">
      <p class="MsoNormal"
 style="margin-bottom: 0.0001pt; text-align: center; line-height: normal;"
 align="center"><span
 style="font-size: 10pt; font-family: &quot;Arial&quot;,sans-serif;">Az_n<o:p></o:p></span></p>
      </td>
      <td
 style="border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; border-width: medium 1pt 1pt medium; padding: 0cm 5.4pt; width: 77.6pt;"
 width="103">
      <p class="MsoNormal"
 style="margin-bottom: 0.0001pt; text-align: center; line-height: normal;"
 align="center"><span
 style="font-size: 10pt; font-family: &quot;Arial&quot;,sans-serif;">AzG_n<o:p></o:p></span></p>
      </td>
      <td
 style="border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; border-width: medium 1pt 1pt medium; padding: 0cm 5.4pt; width: 68.9pt;"
 width="92">
      <p class="MsoNormal"
 style="margin-bottom: 0.0001pt; text-align: center; line-height: normal;"
 align="center"><span
 style="font-size: 10pt; font-family: &quot;Arial&quot;,sans-serif;">Dn<o:p></o:p></span></p>
      </td>
    </tr>
'''

texto = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
</head>
<body>
<table class="MsoTableGrid"
 style="border: medium none ; width: 481.7pt; border-collapse: collapse; margin-left: 4.8pt; margin-right: 4.8pt;"
 align="left" border="1" cellpadding="0"
 cellspacing="0" width="642">
  <tbody>
    <tr style="">
      <td colspan="7"
 style="border: 1pt solid windowtext; padding: 0cm 5.4pt; width: 481.7pt;"
 width="642">
      <p class="MsoNormal"
 style="margin-bottom: 0.0001pt; text-align: center; line-height: normal;"
 align="center"><span
 style="font-size: 10pt; font-family: &quot;Arial&quot;,sans-serif;">MEMORIAL
DESCRITIVO SINT&Eacute;TICO [TITULO]<o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td rowspan="2"
 style="border-style: none solid solid; border-color: -moz-use-text-color windowtext windowtext; border-width: medium 1pt 1pt; padding: 0cm 5.4pt; width: 54.15pt;"
 width="72">
      <p class="MsoNormal"
 style="margin-bottom: 0.0001pt; text-align: center; line-height: normal;"
 align="center"><span
 style="font-size: 10pt; font-family: &quot;Arial&quot;,sans-serif;">V&Eacute;RTICE<o:p></o:p></span></p>
      </td>
      <td colspan="2"
 style="border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; border-width: medium 1pt 1pt medium; padding: 0cm 5.4pt; width: 150.45pt;"
 width="201">
      <p class="MsoNormal"
 style="margin-bottom: 0.0001pt; text-align: center; line-height: normal;"
 align="center"><span
 style="font-size: 10pt; font-family: &quot;Arial&quot;,sans-serif;">COORDENADAS<o:p></o:p></span></p>
      </td>
      <td rowspan="2"
 style="border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; border-width: medium 1pt 1pt medium; padding: 0cm 5.4pt; width: 165pt;"
 width="74">
      <p class="MsoNormal"
 style="margin-bottom: 0.0001pt; text-align: center; line-height: normal;"
 align="center"><span
 style="font-size: 10pt; font-family: &quot;Arial&quot;,sans-serif;">LADO<o:p></o:p></span></p>
      </td>
      <td colspan="2"
 style="border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; border-width: medium 1pt 1pt medium; padding: 0cm 5.4pt; width: 153pt;"
 width="204">
      <p class="MsoNormal"
 style="margin-bottom: 0.0001pt; text-align: center; line-height: normal;"
 align="center"><span
 style="font-size: 10pt; font-family: &quot;Arial&quot;,sans-serif;">AZIMUTES<o:p></o:p></span></p>
      </td>
      <td rowspan="2"
 style="border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; border-width: medium 1pt 1pt medium; padding: 0cm 5.4pt; width: 68.9pt;"
 width="92">
      <p class="MsoNormal"
 style="margin-bottom: 0.0001pt; text-align: center; line-height: normal;"
 align="center"><span
 style="font-size: 10pt; font-family: &quot;Arial&quot;,sans-serif;">DIST&Acirc;NCIA<o:p></o:p></span></p>
      <p class="MsoNormal"
 style="margin-bottom: 0.0001pt; text-align: center; line-height: normal;"
 align="center"><span
 style="font-size: 10pt; font-family: &quot;Arial&quot;,sans-serif;">(m)<o:p></o:p></span></p>
      </td>
    </tr>
    <tr style="">
      <td
 style="border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; border-width: medium 1pt 1pt medium; padding: 0cm 5.4pt; width: 78.35pt;"
 width="104">
      <p class="MsoNormal"
 style="margin-bottom: 0.0001pt; text-align: center; line-height: normal;"
 align="center"><span
 style="font-size: 10pt; font-family: &quot;Arial&quot;,sans-serif;">E<o:p></o:p></span></p>
      </td>
      <td
 style="border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; border-width: medium 1pt 1pt medium; padding: 0cm 5.4pt; width: 72.1pt;"
 width="96">
      <p class="MsoNormal"
 style="margin-bottom: 0.0001pt; text-align: center; line-height: normal;"
 align="center"><span
 style="font-size: 10pt; font-family: &quot;Arial&quot;,sans-serif;">N<o:p></o:p></span></p>
      </td>
      <td
 style="border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; border-width: medium 1pt 1pt medium; padding: 0cm 5.4pt; width: 75.4pt;"
 width="101">
      <p class="MsoNormal"
 style="margin-bottom: 0.0001pt; text-align: center; line-height: normal;"
 align="center"><span
 style="font-size: 10pt; font-family: &quot;Arial&quot;,sans-serif;">PLANO<o:p></o:p></span></p>
      </td>
      <td
 style="border-style: none solid solid none; border-color: -moz-use-text-color windowtext windowtext -moz-use-text-color; border-width: medium 1pt 1pt medium; padding: 0cm 5.4pt; width: 77.6pt;"
 width="103">
      <p class="MsoNormal"
 style="margin-bottom: 0.0001pt; text-align: center; line-height: normal;"
 align="center"><span
 style="font-size: 10pt; font-family: &quot;Arial&quot;,sans-serif;">VERDADEIRO<o:p></o:p></span></p>
      </td>
    </tr>
[LINHAS]
  </tbody>
</table>
</body>
</html>
'''

@qgsfunction(args='auto', group='Custom')
def MemorialSintetico(layer_name, ini, fim, titulo, feature, parent):
    """
    Gera o memorial descritivo sintético a partir de uma camada de pontos do perímetro de um imóvel e dos vértices inicial e final pretendido.
    O título da tabela pode ser inserido como string.
    <h2>Examplo:</h2>
    <ul>
      <li>MemorialSintetico('nome_camada', ini, fim, 'titulo') ->[HTML]</li>
      <li>MemorialSintetico('Vértices', 1, 20, 'Area X') ->[HTML]</li>
    </ul>
    """
    
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
                    'Ln': pnts_UTM[k+1][2] + ' / ' + pnts_UTM[1 if k+2 > tam else k+2][2],
                    'Az_n': DD2DMS(Az_lista[k]).replace('.', ','),
                    'AzG_n':  DD2DMS(Az_Geo_lista[k]).replace('.', ','),
                    'Dn': '{:,.2f}'.format(Dist[k]).replace(',', 'X').replace('.', ',').replace('X', '.')
                    }
        for item in itens:
            linha0 = linha0.replace(item, itens[item])
        LINHAS += linha0
    resultado = texto.replace('[LINHAS]', LINHAS).replace('[TITULO]', titulo)
    
    return resultado
