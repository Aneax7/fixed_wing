# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 22:10:02 2018

@author: xajsc
"""
import atmosphere
import numpy as np
import matplotlib.pyplot as plt

AR=8
e=1.78*(1-0.045*np.power(AR,0.68))-0.64
k=1/(np.pi*AR*e)
V=25 # Cruise Velocity m/s
V_end=15 
C_D0=0.03 # Zero lift drag coefficient
n=1/np.cos(45*np.pi/180) # Load Factor
ROC_max=5 # Rate of climb
h=2400 # Cruise Altitude
g=9.81
c_D_to=0.2 # Drag coefficient takeoff
S_g=100 # Ground Run
V_lo=15 # Lift off velocity
mu=0.04 # Ground friction coefficient
cL_to=1.6 # Lift coefficient at take off
P_s=ROC_max
eff_prop=0.8
plane_mass=3.5 # Mass of plane
L_Dmax=1

def q_calculate(h,V):
    rho,temp=atmosphere.densityGradient(h)
    q= 0.5*rho*V**2
    return q

def power_calc(tw,V):
    pw=tw*V/(eff_prop)
    return pw

#%% For desired specific energy level
def specific_energy(w_s,P_s,h):
    '''q = dynamic pressure at the selected airspeed and altitude
    P_s = specific energy level at the condition
    V = airspeed'''
    q=q_calculate(h,V)
    tw=q*(C_D0/w_s+k*(n/q)**2*(w_s))+P_s/V
    pw=power_calc(tw,V)
    return tw
 
#%% For level constant velocity turn
def constant_velocity(w_s,h):   
    ''' c_D0= minimum drag coefficient
    k = lift-induced drag constant
    q = dynamic pressure at the selected airspeed and altitude (N/m 2 )
    S = wing area ( m2 )
    T = thrust ( N)
    W = weight ( N)
    n = load factor = 1=cos (phi)
    w_s=W/S'''
    q=q_calculate(h,V)
    tw=q*(C_D0/w_s+k*(n/q)**2*(w_s)) 
    pw=power_calc(tw,V)
    return tw

#%% Desired rate of climb
def rate_climb(w_s,h):
    '''V_v = vertical speed'''
    rho,temp=atmosphere.densityGradient(h)    
    # V=(2/rho*w_s*(k/(3*c_Dmin))**0.5)**0.5
    # print(V)
    q=q_calculate(h,V)
    tw= ROC_max/V+q/w_s*C_D0+k/q*w_s
    pw=power_calc(tw,V)
    return tw

#%% Desired cruise speed
def tcruise_speed(w_s,h):
    q=q_calculate(h,V)
    tw=q*C_D0/w_s+k/q*w_s
    pw=power_calc(tw,V)
    return tw

#%% Desired Service Ceiling
def service_ceiling(w_s,h):
    '''r = air density at the desired altitude.
        V_v =0.508 m/s if using the SI-system''' 
    V_vs=0.508 
    rho,temp=atmosphere.densityGradient(h)    
    tw=V_vs/(2/rho*w_s*(k/(3*C_D0))**0.5)**0.5+4*(k*C_D0/3)**0.5
    pw=power_calc(tw,V)
    return tw

#%% Takeoff
def take_off(h):
    rho,temp=atmosphere.densityGradient(h)
    w_s=0.5*rho*V_end**2*cL_to/1.21
    return w_s

def cl_cmax(w_s,V,h):
    q_stall=q_calculate(h,V)
    return w_s/q_stall
w_s=5
cv_ws=[]
w_s_c=[]
sc_ws=[]
rc_ws=[]
to_ws=[]
se_ws=[]
cs_ws=[]
cl_max=[]
cl2_max=[]
cl3_max=[]
cl4_max=[]
while w_s <=205:
    ws_cv=constant_velocity(w_s,h)
    ws_rc=rate_climb(w_s,h)
    ws_cs=tcruise_speed(w_s,h)
    ws_sc=service_ceiling(w_s,5500)
    #ws_to=take_off(h)
    ws_se=specific_energy(w_s,P_s,h)
    cl=cl_cmax(w_s,V,h)
    cl2=cl_cmax(w_s,8,h)
    cl3=cl_cmax(w_s,10,h)
    cl4=cl_cmax(w_s,15,h)
    cv_ws.append(ws_cv)
    sc_ws.append(ws_sc)
    rc_ws.append(ws_rc)
    cs_ws.append(ws_cs)
    se_ws.append(ws_se)
    w_s_c.append(w_s/g)
    cl_max.append(cl)
    cl2_max.append(cl2)
    cl3_max.append(cl3)
    cl4_max.append(cl4)
    w_s=w_s+1
    

fig, ax1 = plt.subplots()
ax1.plot(w_s_c,cv_ws,label='Constant Velocity Turn')
ax1.plot(w_s_c,sc_ws,label='Service Ceiling')
ax1.plot(w_s_c,rc_ws,label='Rate of climb')
ax1.plot(w_s_c,cs_ws,label='Cruise Speed')
plt.plot(w_s_c,se_ws,label='Specific Energy')

ax1.set_xlabel('W/S kg/m2')
ax1.set_ylabel('T/W ') 
#plt.axis([0, 200, 0, 150])
plt.legend(bbox_to_anchor=(0.2, 1), loc=2, borderaxespad=0.) 
plt.grid(True)
ax1.tick_params('y', colors='b')


ax2 = ax1.twinx()
ax2.plot(w_s_c, cl_max,label="cL max (25)")
ax2.plot(w_s_c, cl2_max,label="cL max (8)")
ax2.plot(w_s_c, cl3_max,label="cL max (10)")
ax2.plot(w_s_c, cl4_max,label="cL max (15)")


ax2.set_ylabel('cL_max', color='r')
ax2.tick_params('y', colors='r')
fig.tight_layout()
plt.legend(bbox_to_anchor=(0.7, 1), loc=2, borderaxespad=0.) 
#%% Break Horse Power Required at sea level
tw_g= 0.5*g
p_bhp=tw_g*V*plane_mass/eff_prop
print(p_bhp)
rhoh,temph=atmosphere.densityGradient(h)
rhosea,tempsea=atmosphere.densityGradient(0)
sigma=rhoh/rhosea
bhp_sea_level= p_bhp/(1.132*sigma-0.132)
print(bhp_sea_level)


plt.show()