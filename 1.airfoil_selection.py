import pandas as pd
import numpy as np

df=pd.read_csv('standard_atmosphere.csv',skiprows=[1]);
df.set_index('altitude',inplace=True)

W_initial=2.5 #kg
W_final=3.5 #kg


W_avg=0.5*(W_initial+W_final) #Average Weight of aircraft in cruising flight
V_c=25 #m/s
V_s=10 #m/s
S= 0.3
cruise_altitude= 2500 #m
g=9.81 #m/s^2
#air_density,air_temperature=atmosphere.densityGradient(cruise_altitude)

air_density=df.loc[cruise_altitude, 'density']
#%% Ideal Lift Coefficient

# Aircraft Ideal Cruise Lift Coefficient 
C_Lc=(2*W_avg*g)/(air_density*V_c**2*S)

# Wing Cruise Lift Coefficient
#Assuming 98 % Lift from wing
C_Lc_w=C_Lc/0.98
print('C_L={0:2.4f}'.format(C_Lc_w))
# Wing Airfoil Ideal Lift Coefficient
C_li=C_Lc_w/0.9
print('C_li={0:0.4f}'.format(C_li))

#%% Maximum Lift Coefficient

# Aircraft Maximum Lift Coefficient
#density_sea,air_temperature=atmosphere.densityGradient(0)
density_sea=df.loc[0, 'density']

C_Lmax=(2*W_initial*g)/(density_sea*V_s**2*S)

# Wing Maximum Lift Coefficient 
C_Lmax_w=C_Lmax/0.95
print('C_Lmax={0:0.4f}'.format(C_Lmax_w))
# Wing Airfoil Gross Maximum Lift Coefficient
C_lmax_gross=C_Lmax/0.9
print('C_lmax_total={0:0.4f}'.format(C_lmax_gross))
#%% Select/Design HLD 
# HLD 				C_lHLD (60 deg deflection)
# Plain Flap 		0.7-0.9
# Split Flap 		0.7-0.9
# Slotted flap   	1.3 C_f /C
# HLD contribution to the wing maximum lift coefficient 
C_lHLD=0.4
V_to=1.2*V_s

#Wing Airfoil net maximum lift coefficient
C_lmax=C_lmax_gross-C_lHLD
print('C_lmax={0:0.4f}'.format(C_lmax))

df2=pd.DataFrame({ 'W_initial':W_initial,
	'W_final':W_final,'S':S,'V_c':V_c,'V_s':V_s,
	'cruise_air_altitude':cruise_altitude,'cruise_air_density':air_density,
	'sea_level_density':density_sea,
						 'C_Lc':C_Lc,
						 'C_Lc_w' : C_Lc_w,
                         'C_li' : C_li,
                         'C_Lmax' : C_Lmax,
                         'C_Lmax_w' : C_Lmax_w,
                         'C_lmax_total' : C_lmax_gross,
                         'C_lHLD' : C_lHLD ,
                         'C_lmax_foil' :C_lmax},index=[0])
df2=pd.DataFrame.transpose(df2)
df2.to_csv('airfoil_requirements.csv', encoding='utf-8',sep=',')

#%% Identify the airfoil sections that deliver C_lmax and C_li.