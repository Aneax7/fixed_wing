import numpy as np
import lifting_line_theory as llt
import llt_flap_deflection as llt_f
import pandas as pd

df=pd.read_csv('standard_atmosphere.csv',skiprows=[1]);
df.set_index('altitude',inplace=True)

def knots_to_ms(V):
	V_ms=0.514444*V
	return V_ms
S_ref=18.1
m=1800
V_c=knots_to_ms(130)
V_s=knots_to_ms(60)
g=9.81

dihedral_angle=-5
sweep_angle=0
i_w=1.85
AR=7
lambdai=0.8
twist_angle=-1.5
S=S_ref*np.cos(dihedral_angle)

C_lalpha=6.3
alpha_0=-3

CL_wing=llt.llt(S,AR,i_w,lambdai,twist_angle,C_lalpha,alpha_0)
print('CL wing:{}'.format(CL_wing))


# sweep_c2=0
# x=b/2*np.sin(sweep_c2*np.pi/180)
# b_eff=2*((b/2)**2-x**2)**0.5
# print(b_eff)
# AR_eff=b_eff**2/S

# ih=x-Ct/2
# print(ih)
# sweep_le=np.arctan((Cr-Ct)/b)
# print(sweep_le)
# sweep_c4=np.arctan((Cr-Ct)/(2*b))*57.3
# print(sweep_c4)

# sweep_le=np.arctan((Cr/2+ih)/(b_eff/2))*180/np.pi
# print(sweep_le)
# sweep_c4=np.arctan((Ct/2+(Cr/2+ih)-Cr/4)/(b_eff/2))*180/np.pi
# print(sweep_c4)
# sweep_te=np.arctan(())

e=1.78*(1-0.045*AR**0.64)-0.64 # for straight wing
# e=4.61*(1-0.045*AR**0.68)(np.cos(sweep_le))**0.15-3.1 # for swept wing


#%% Flap Parameters
V_to=1.2*V_s
density_0=df.loc[0, 'density']
C_L_to=(2*m*g)/(density_0*V_to**2*S_ref)

cf_c=0.2  #flap chord to wing chord
bf_b=0.6  #flap span to wing span
alpha_to=8.88#max angle of attack during takeoff
delta_f=13 #max flap deflection at takeoff

del_alpha_0flap=-1.15*cf_c*delta_f
alpha_0_fd=alpha_0+del_alpha_0flap

CL_wing_f=llt_f.llt(S,AR,alpha_to,lambdai,twist_angle,C_lalpha,alpha_0,alpha_0_fd)
print('CL wing with flap deflection:{}'.format(CL_wing_f))
alpha_to_fus=alpha_to-i_w

b=(AR*S_ref)**0.5
MAC=S_ref/(b)
Cr=(1.5*(1+lambdai)*MAC)/(1+lambdai+lambdai**2)
Ct=lambdai*Cr

b_f=bf_b*b
c_f=cf_c*MAC

df=pd.DataFrame({ 'W':m,
	'S':S,'V_c':V_c,'V_s':V_s,
	'sea_level_density':density_0,
						 'C_Lc_w' : CL_wing,
                         'e':e,
                         'dihedral_angle':dihedral_angle,
                         'sweep_angle':sweep_angle,
                         'i_w':i_w,
                         'AR':AR,
                         'taper_ratio':lambdai,
                         'twist_angle':twist_angle,
                         'b':b,
                         'MAC':MAC,
                         'Cr':Cr,
                         'Ct':Ct,
                         'C_L_to' : C_L_to,
                         'V_to':V_to,
                         'bf_b':bf_b,
                         'cf_c':cf_c,
                         'b_f m':b_f,
                         'c_f m':c_f},index=[0])
df=pd.DataFrame.transpose(df)
df.to_csv('wing_design.csv', encoding='utf-8',sep=',')