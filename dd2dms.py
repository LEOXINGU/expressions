from qgis.core import *
from qgis.gui import *
from numpy import floor

@qgsfunction(args='auto', group='Geodesy')
def dd2dms(dd, n_digits, feature, parent):
    """
    Transform decimal degrees to degrees, minutes and seconds.
    <h2>Example usage:</h2>
    <ul>
      <li>dd2dms(dd, 3) -> -12dd12mm34.741ss</li>
    </ul>
    """
    if dd != 0:
        graus = int(floor(abs(dd)))
        resto = round(abs(dd) - graus, 8)
        if dd < 0:
            texto = '-' + str(graus) + 'dd'
        else:
            texto = str(graus) + 'dd'
        minutos = int(floor(60*resto))
        resto = round(resto*60 - minutos, 10)
        texto = texto + '{:02d}'.format(minutos) + "mm"
        segundos = resto*60        
        if round(segundos,n_digits) == 60:
            minutos += 1
            segundos = 0
        if minutos == 60:
            graus += 1
            minutos = 0
        if n_digits < 1:
            texto = texto + '{:02d}'.format(int(segundos)) + 'ss'
        else:
            texto = texto + ('{:0' + str(3+n_digits) + '.' + str(n_digits) + 'f}').format(segundos) + 'ss'
        return texto
    else:
        return "0dd00mm" + ('{:0' + str(3+n_digits) + '.' + str(n_digits) + 'f}').format(0) + 'ss'
