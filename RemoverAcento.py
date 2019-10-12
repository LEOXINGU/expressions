from qgis.core import *
from qgis.gui import *
import unicodedata
import re

@qgsfunction(args='auto', group='Custom')
def removerAcentos(palavra, feature, parent):
    """
    Substitui caracteres especiais.
    <h2>Examplo:</h2>
    <ul>
      <li>removerAcentosECaracteresEspeciais('cora��o') -> coracao </li>
      <li>removerAcentosECaracteresEspeciais('g�nesis') -> genesis</li>
    </ul>
    """
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa express�o regular para retornar a palavra apenas com n�meros, letras e espa�o
    return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)
