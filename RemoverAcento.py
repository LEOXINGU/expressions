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
      <li>removerAcentosECaracteresEspeciais('coração') -> coracao </li>
      <li>removerAcentosECaracteresEspeciais('gênesis') -> genesis</li>
    </ul>
    """
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])

    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)
