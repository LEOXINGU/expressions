from qgis.core import *
from qgis.gui import *

def menos(a, b):
    return a-b

@qgsfunction(args='auto', group='Custom')
def my_differece(value1, value2, feature, parent):
    """
    Calculates the sum of the two parameters value1 and value2.
    <h2>Example usage:</h2>
    <ul>
      <li>my_differece(5, 8) -> -3</li>
      <li>my_differece("field1", "field2") -> 9</li>
    </ul>
    """
    return menos(value1, value2)
