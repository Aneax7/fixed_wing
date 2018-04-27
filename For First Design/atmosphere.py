'''TO CALCULATE DENSITY AND ALTITUDE
inputs for density:
1. geometric altitude

output for density:
1. value of density

input of altitude:
1. density
2. pressure

output for altitude:
1. geometric height
'''

#code starts here

a=-6.5e-3 #Lapse rate
rEarth=6371000 #radius of Earth
h0=0 #sea level height
g=9.80665 #acceleration due to gravity
p0=101325 #pressure at sea level
d0=1.225 #density at sea level
T0=288.16 #reference temperature in kelvin
R=286.9 #gas constant

import math

# density calculation

def densityGradient(h2,h1=0,T1=288.16,p1=101325,d1=1.225): # to calculate density in gradient region
    h1geoPo=h1*(rEarth/(rEarth+h1))
    h2geoPo=h2*(rEarth/(rEarth+h2))
    T2=T1+a*(h2geoPo-h1geoPo)
    d2=d1*(T2/T1)**-(g/(a*R)+1)
    return (d2,T2)

def pressureGradient(h2,h1=0,T1=288.16,p1=101325,d1=1.225):
    h1geoPo=h1*(rEarth/(rEarth+h1))
    h2geoPo=h2*(rEarth/(rEarth+h2))
    T2=T1+a*(h2geoPo-h1geoPo)
    p2=p1*(T2/T1)**(-g/(a*R))
    return p2,T2

def densityIsothermal(h2,h1=0,T=288.16,d1=1.225):
    h1geoPo=h1*(rEarth/(rEarth+h1))
    h2geoPo=h2*(rEarth/(rEarth+h2))
    d2=d1*math.exp(-g/(R*T)*(h2geoPo-h1geoPo))
    return d2

def pressureIsothermal(h2,h1=0,T=288.16,p1=1.225):
    h1geoPo=h1*(rEarth/(rEarth+h1))
    h2geoPo=h2*(rEarth/(rEarth+h2))
    p2=p1*math.exp(-g/(R*T)*(h2geoPo-h1geoPo))
    return p2

def density(h):
    if h<11000:
        d,T=densityGradient(h,h0,T0,p0,d0)
        return d,T
    if h>=11000:
        d11,T=densityGradient(11000,h0,T0,p0,d0)
        d=densityIsothermal(h,11000,T,d11)
        return d,T

def pressure(h):
    if h<11000:
        p,T=pressureGradient(h,h0,T0,p0,d0)
        return p,T
    if h>=11000:
        p11,T=pressureGradient(11000,h0,T0,p0,d0)
        p=pressureIsothermal(h,11000,T,p11)
        return p,T


# for altitude
def geoPotential(hg):
    return hg*(rEarth/(rEarth+hg))

def geometric(h):
    return h*(rEarth/(rEarth-h))

def temperatureAltitude(T1,T2,h1):
    return (T2-T1)/a+h1

def altPressureGradient(h1,T1,p1,p2):
    T2=T1*(p2/p1)**(-a*R/g)
    Talt=temperatureAltitude(T1,T2,h1)
    return geoPotential(Talt)
def altDensityGradient(h1,T1,d1,d2):
    T2=T1*(d2/d1)**(-a*R/(g+a*R))
    Talt=temperatureAltitude(T1,T2,h1)
    return geoPotential(Talt)

def altPressureIsothermal(h1,T,p1,p2):
    return h1-R*T/g*math.log(p2/p1)

def altDensityIsothermal(h1,T,d1,d2):
    return h1-R*T/g*math.log(d2/d1)

def pressureAltitude(p):
    p11,T11=pressureGradient(11000,h0,T0,p0,d0)
    if p>p11:
        return geometric(altPressureGradient(h0,T0,p0,p))
    if p<=p11:
        return geometric(altPressureIsothermal(11000,T11,p11,p))
def densityAltitude(d):
    d11,T11=densityGradient(11000,h0,T0,p0,d0)
    if d>d11:
        return geometric(altDensityGradient(h0,T0,d0,d))
    if d<=d11:
        return geometric(altDensityIsothermal(11000,T11,d11,d))
