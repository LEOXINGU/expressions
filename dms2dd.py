from qgis.core import *
from qgis.gui import *

@qgsfunction(args='auto', group='Geodesy')
def dms2dd(txt, feature, parent):
    """
    Transform degrees, minutes, seconds coordinate to decimal degrees.
    <h2>Example usage:</h2>
    <ul>
      <li>dms2dd("dms") -> dd</li>
      <li>dms2dd('-10°30'00.0"') -> -10.5</li>
    </ul>
    """
    txt = txt.replace(' ','').replace(',','.')
    newtxt =''
    for letter in txt:
        if not letter.isnumeric() and letter != '.' and letter != '-':
            newtxt += '|'
        else:
            newtxt += letter
    lista = newtxt[:-1].split('|')
    if len(lista) != 3: # GMS
        return None
    else:
        if '-' in lista[0]: 
            return -1*(abs(float(lista[0])) + float(lista[1])/60 + float(lista[2])/3600)
        else:
            return float(lista[0]) + float(lista[1])/60 + float(lista[2])/3600
