from qgis.core import *
from qgis.gui import *
from math import modf

@qgsfunction(args='auto', group='Custom')
def dd2dms(dd, n_digits, feature, parent):
    """
    Transform decimal degrees to degrees, minutes and seconds.
    <h2>Example usage:</h2>
    <ul>
      <li>dd2dms(dd, 3) -> -12°12'34.741''</li>
    </ul>
    """
    sinal = dd/abs(dd)
    dd = abs(dd)
    dd, d_int = modf(dd)
    mins, m_int = modf(60 * dd)
    secs = 60 * mins
    n_digits = int(n_digits)
    if n_digits < 1:
        n_digits = 1
    template_sec = "{:." + str(n_digits) + "f}"
    return str(int(sinal*d_int)) + "°" + str(int(m_int)).zfill(2) + "'" + (template_sec.format(secs)).zfill(3+n_digits) + "''"
