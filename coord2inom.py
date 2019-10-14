from qgis.core import *
from qgis.gui import *
from numpy import sign, array
from math import floor, modf

@qgsfunction(args='auto', group='Cartography')
def coord2inom(lon, lat, ScaleD, feature, parent):
    """
    Calculates the chart index from coordinates.
    <h2>Example usage:</h2>
    <ul>
      <li>coord2inom(lon, lat, ScaleD) -> inom</li>
      <li>coord2inom(-42.2, -13.4, 1000000) -> SA-23</li>
    </ul>
    """
    lon, lat = lon+1e-10, lat+1e-10
    if ScaleD not in [1e6, 5e5, 2.5e5, 1e5, 5e4, 2.5e4, 1e4, 5e3, 2e3, 1e3]:
        ScaleD = 1e6
        
    # Escala 1:1.000.000
    nome = ''
    sinal = sign(lat)
    if sinal == -1:
        nome+='S'
    else:
        nome+='N'
    # Determinacao da letra
    letra = chr(int(65+floor(abs(lat)/4.0)))
    nome+=letra
    # Calculo do Fuso
    fuso = round((183+lon)/6.0)
    nome+='-'+str(int(fuso))
    # Calculo do Meridiano Central
    MC = 6*fuso-183
    valores = array([[3.0, 1.5, 0.5, 0.25, 0.125, 0.125/2, 0.125/2/2, 0.125/2/2/3, 0.125/2/2/3/2],
                           [2.0, 1.0, 0.5, 0.25, 0.125, 0.125/3, 0.125/3/2, 0.125/3/2/2, 0.125/3/2/2/2]])
    if ScaleD > 500000:
        return nome
    
    # Escala 1:500.000
    if ScaleD <= 500000:
        centro = array([MC, 4.0*floor(lat/4.0)+valores[1][0]])
        sinal = sign(array([lon, lat]) - centro)
        if sinal[0]==-1 and sinal[1]==1:
            nome+='-V'
        elif sinal[0]==1 and sinal[1]==1:
            nome+='-X'
        elif sinal[0]==-1 and sinal[1]==-1:
            nome+='-Y'
        elif sinal[0]==1 and sinal[1]==-1:
            nome+='-Z'
    if ScaleD > 250000:
        return nome
    
    # Escala 1:250.000
    if ScaleD <= 250000:
        centro = centro + sinal*valores[:,1]
        sinal = sign(array([lon, lat]) - centro)
        if sinal[0]==-1 and sinal[1]==1:
            nome+='-A'
        elif sinal[0]==1 and sinal[1]==1:
            nome+='-B'
        elif sinal[0]==-1 and sinal[1]==-1:
            nome+='-C'
        elif sinal[0]==1 and sinal[1]==-1:
            nome+='-D'
    if ScaleD > 100000:
            return nome
    
    # Escala 1:100.000
    if ScaleD <= 100000:
        ok = False
        if sinal[0]==1:
            c1 = centro + sinal*valores[:,2]
            sinal_ = sign(array([lon, lat]) - c1)
            if sinal_[0]==-1 and sinal_[1]==1:
                nome+='-I'
                ok = True
                centro = c1
                sinalx = sinal_
            elif sinal_[0]==-1 and sinal_[1]==-1:
                nome+='-IV'
                ok = True
                centro = c1
                sinalx = sinal_
            c2 = centro + array([2*sinal[0], sinal[1]])*valores[:,2]
            sinal_ = sign(array([lon, lat]) - c2)
            if sinal_[0]==1 and sinal_[1]==1 and ok == False:
                nome+='-III'
                centro = c2
                sinalx = sinal_
            elif sinal_[0]==1 and sinal_[1]==-1 and ok == False:
                nome+='-VI'
                centro = c2
                sinalx = sinal_
            elif sinal_[0]==-1 and sinal_[1]==1 and ok == False:
                nome+='-II'
                centro = c2
                sinalx = sinal_
            elif sinal_[0]==-1 and sinal_[1]==-1 and ok == False:
                nome+='-V'
                centro = c2
                sinalx = sinal_
        elif sinal[0]==-1:
            c1 = centro + sinal*valores[:,2]
            sinal_ = sign(array([lon, lat]) - c1)
            if sinal_[0]==1 and sinal_[1]==1:
                nome+='-III'
                ok = True
                centro = c1
                sinalx = sinal_
            elif sinal_[0]==1 and sinal_[1]==-1:
                nome+='-VI'
                ok = True
                centro = c1
                sinalx = sinal_
            c2 = centro + array([2*sinal[0], sinal[1]])*valores[:,2]
            sinal_ = sign(array([lon, lat]) - c2)
            if sinal_[0]==1 and sinal_[1]==1 and ok == False:
                nome+='-II'
                centro = c2
                sinalx = sinal_
            elif sinal_[0]==1 and sinal_[1]==-1 and ok == False:
                nome+='-V'
                centro = c2
                sinalx = sinal_
            elif sinal_[0]==-1 and sinal_[1]==1 and ok == False:
                nome+='-I'
                centro = c2
                sinalx = sinal_
            elif sinal_[0]==-1 and sinal_[1]==-1 and ok == False:
                nome+='-IV'
                centro = c2
                sinalx = sinal_
        sinal = sinalx
    if ScaleD > 50000:
            return nome
    
    # Escala 1:50.000
    if ScaleD <= 50000:
        centro = centro + sinal*valores[:,3]
        sinal = sign(array([lon, lat]) - centro)
        if sinal[0]==-1 and sinal[1]==1:
            nome+='-1'
        elif sinal[0]==1 and sinal[1]==1:
            nome+='-2'
        elif sinal[0]==-1 and sinal[1]==-1:
            nome+='-3'
        elif sinal[0]==1 and sinal[1]==-1:
            nome+='-4'
    if ScaleD > 25000:
            return nome
    
    # Escala 1:25.000
    if ScaleD <= 25000:
        centro = centro + sinal*valores[:,4]
        sinal = sign(array([lon, lat]) - centro)
        if sinal[0]==-1 and sinal[1]==1:
            nome+='-NO'
        elif sinal[0]==1 and sinal[1]==1:
            nome+='-NE'
        elif sinal[0]==-1 and sinal[1]==-1:
            nome+='-SO'
        elif sinal[0]==1 and sinal[1]==-1:
            nome+='-SE'
    if ScaleD > 10000:
            return nome
    
    # Escala 1:10.000
    if ScaleD <= 10000:
        ok = False
        if sinal[1]==1:
            c1 = centro + sinal*valores[:,5]
            sinal_ = sign(array([lon, lat]) - c1)
            if sinal_[0]==-1 and sinal_[1]==-1:
                nome+='-E'
                ok = True
                centro = c1
                sinalx = sinal_
            elif sinal_[0]==1 and sinal_[1]==-1:
                nome+='-F'
                ok = True
                centro = c1
                sinalx = sinal_
            c2 = centro + array([sinal[0], 2*sinal[1]])*valores[:,5]
            sinal_ = sign(array([lon, lat]) - c2)
            if sinal_[0]==1 and sinal_[1]==1 and ok == False:
                nome+='-B'
                centro = c2
                sinalx = sinal_
            elif sinal_[0]==1 and sinal_[1]==-1 and ok == False:
                nome+='-D'
                centro = c2
                sinalx = sinal_
            elif sinal_[0]==-1 and sinal_[1]==1 and ok == False:
                nome+='-A'
                centro = c2
                sinalx = sinal_
            elif sinal_[0]==-1 and sinal_[1]==-1 and ok == False:
                nome+='-C'
                centro = c2
                sinalx = sinal_
        elif sinal[1]==-1:
            c1 = centro + sinal*valores[:,5]
            sinal_ = sign(array([lon, lat]) - c1)
            if sinal_[0]==1 and sinal_[1]==1:
                nome+='-B'
                ok = True
                centro = c1
                sinalx = sinal_
            elif sinal_[0]==-1 and sinal_[1]==1:
                nome+='-A'
                ok = True
                centro = c1
                sinalx = sinal_
            c2 = centro + array([sinal[0], 2*sinal[1]])*valores[:,5]
            sinal_ = sign(array([lon, lat]) - c2)
            if sinal_[0]==1 and sinal_[1]==1 and ok == False:
                nome+='-D'
                centro = c2
                sinalx = sinal_
            elif sinal_[0]==1 and sinal_[1]==-1 and ok == False:
                nome+='-F'
                centro = c2
                sinalx = sinal_
            elif sinal_[0]==-1 and sinal_[1]==1 and ok == False:
                nome+='-C'
                centro = c2
                sinalx = sinal_
            elif sinal_[0]==-1 and sinal_[1]==-1 and ok == False:
                nome+='-E'
                centro = c2
                sinalx = sinal_
        sinal = sinalx
    if ScaleD > 5000:
        return nome
    
    # Escala 1:5.000
    if ScaleD <= 5000:
        centro = centro + sinal*valores[:,6]
        sinal = sign(array([lon, lat]) - centro)
        if sinal[0]==-1 and sinal[1]==1:
            nome+='-I'
        elif sinal[0]==1 and sinal[1]==1:
            nome+='-II'
        elif sinal[0]==-1 and sinal[1]==-1:
            nome+='-III'
        elif sinal[0]==1 and sinal[1]==-1:
            nome+='-IV'
    if ScaleD > 2000:
            return nome
    
    # Escala 1:2.000
    if ScaleD <= 2000:
        ok = False
        if sinal[0]==1:
            c1 = centro + sinal*valores[:,7]
            sinal_ = sign(array([lon, lat]) - c1)
            if sinal_[0]==-1 and sinal_[1]==1:
                nome+='-1'
                ok = True
                centro = c1
                sinalx = sinal_
            elif sinal_[0]==-1 and sinal_[1]==-1:
                nome+='-4'
                ok = True
                centro = c1
                sinalx = sinal_
            c2 = centro + array([2*sinal[0], sinal[1]])*valores[:,7]
            sinal_ = sign(array([lon, lat]) - c2)
            if sinal_[0]==1 and sinal_[1]==1 and ok == False:
                nome+='-3'
                centro = c2
                sinalx = sinal_
            elif sinal_[0]==1 and sinal_[1]==-1 and ok == False:
                nome+='-6'
                centro = c2
                sinalx = sinal_
            elif sinal_[0]==-1 and sinal_[1]==1 and ok == False:
                nome+='-2'
                centro = c2
                sinalx = sinal_
            elif sinal_[0]==-1 and sinal_[1]==-1 and ok == False:
                nome+='-5'
                centro = c2
                sinalx = sinal_
        elif sinal[0]==-1:
            c1 = centro + sinal*valores[:,7]
            sinal_ = sign(array([lon, lat]) - c1)
            if sinal_[0]==1 and sinal_[1]==1:
                nome+='-3'
                ok = True
                centro = c1
                sinalx = sinal_
            elif sinal_[0]==1 and sinal_[1]==-1:
                nome+='-6'
                ok = True
                centro = c1
                sinalx = sinal_
            c2 = centro + array([2*sinal[0], sinal[1]])*valores[:,7]
            sinal_ = sign(array([lon, lat]) - c2)
            if sinal_[0]==1 and sinal_[1]==1 and ok == False:
                nome+='-2'
                centro = c2
                sinalx = sinal_
            elif sinal_[0]==1 and sinal_[1]==-1 and ok == False:
                nome+='-5'
                centro = c2
                sinalx = sinal_
            elif sinal_[0]==-1 and sinal_[1]==1 and ok == False:
                nome+='-1'
                centro = c2
                sinalx = sinal_
            elif sinal_[0]==-1 and sinal_[1]==-1 and ok == False:
                nome+='-4'
                centro = c2
                sinalx = sinal_
        sinal = sinalx
    if ScaleD > 1000:
            return nome
    
    # Escala 1:1.000
    if ScaleD <= 1000:
        centro = centro + sinal*valores[:,8]
        sinal = sign(array([lon, lat]) - centro)
        if sinal[0]==-1 and sinal[1]==1:
            nome+='-A'
        elif sinal[0]==1 and sinal[1]==1:
            nome+='-B'
        elif sinal[0]==-1 and sinal[1]==-1:
            nome+='-C'
        elif sinal[0]==1 and sinal[1]==-1:
            nome+='-D'
        return nome
