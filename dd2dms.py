from qgis.core import *
from qgis.gui import *
from numpy import floor

@qgsfunction(args='auto', group='Geodesy')
def dd2dms(dd, n_digits, feature, parent):
    """
    Transform decimal degrees to degrees, minutes and seconds.
    <h2>Example usage:</h2>
    <ul>
      <li>dd2dms(dd, 3) -> -12�12'34.741''</li>
    </ul>
    """
    if dd != 0:
        graus = int(floor(abs(dd)))
        resto = round(abs(dd) - graus, 10)
        if dd < 0:
            texto = '-' + str(graus) + '�'
        else:
            texto = str(graus) + '�'
        minutos = int(floor(60*resto))
        resto = round(resto*60 - minutos, 10)
        texto = texto + '{:02d}'.format(minutos) + "'"
        segundos = resto*60
        if n_digits < 1:
            texto = texto + '{:02d}'.format(int(segundos)) + '"'
        else:
            texto = texto + ('{:0' + str(3+n_digits) + '.' + str(n_digits) + 'f}').format(segundos) + '"'
        return texto
    else:
        return "0�00'" + ('{:0' + str(3+n_digits) + '.' + str(n_digits) + 'f}').format(0)
