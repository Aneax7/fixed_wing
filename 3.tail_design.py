# Assumption- thrust line and cg line co-incides
# For detail analysis use Digital Datcom

import numpy as np
import pandas as pd
import lifting_line_theory as llt

def knots_to_ms(V):
	V_ms=0.514444*V
	return V_ms
def feet_to_m(h):
    h_m=0.3048*h
    return h_m

df=pd.read_csv('wing_design.csv')
df=pd.DataFrame.transpose(df)

df2=pd.read_csv('standard_atmosphere.csv',skiprows=[1]);
df2.set_index('altitude',inplace=True)

m_to=850
Df_max=1.1 #max fuselage diameter
V_c=knots_to_ms(95) # Cruise velocity
cruise_altitude=feet_to_m(10000)
alpha_f=1 # fuselage angle of attack during cruise
g=9.81 #acceleration due to gravity

####### Wing Parameters ##########
S=18 
AR=28
MAC=0.8
taper_ratio=0.8
i_w=3
alpha_twist=-1.1
sweep_le=8
dihedral_angle=5

C_Lalpha=5.8 # Wing lift curve slope
################################### 

###################################################################################
# Requirements ####################### Symbol ######### Typical Values ############
# Static Longitudinal Stability       Cm_alpha          -0.3 to -1.5  (1/rad)     #
# Static margin                       h_np-h_cg          0.1-0.3                  #
# Dynamic Longitudinal Stability      Cm_q               -5 to -40
# Static Directional Stability        Cn_beta            0.05 to 0.4
# Dynamic Directional Stability       Cn_r               -0.1 to -1
####################################################################################

##############################################
## Type #########   C_ht  ###### C_vt ######## 
# GA twin prop       0.8         0.07
# GA single prop     0.7         0.04
# Moter Glider       0.6         0.03 
# Transport jets     1           0.08 
# Jet Trainer       0.7          0.06 
# Jet-Fighter       0.4          0.07 
##############################################

# Horizontal Tail Volume Coefficient #
V_H=0.6

# Optimum tail moment arm #
K_C=1.2 #co-relation factor
l=lopt=K_C*(4*MAC*S*V_H/(np.pi*Df_max))**0.5

########################################################
# For Vertical Location of Horizontal Tail
# ht<l*tan(alpha_s-i_w+3) &&
# ht>l*tan(alpha_s-i_w-3) 
########################################################

# Tail Planform Area #
S_h=MAC*S*V_H/l

# Cruise Lift Coefficient #
density_c=df2.loc[cruise_altitude, 'density']
C_L=C_Lc=2*m_to*g/(density_c*V_c**2*S)

# Wing Fuselage Aerodynamic Pitching Moment Coefficient #

Cm_af=-0.013 # Wing airfoil pitching moment coefficient
Cm0_wf=Cm_af*(AR*(np.cos(sweep_le/57.3))**2)/(AR+2*np.cos(sweep_le/57.3))+0.01*alpha_twist

####################################################################################
# Typical Vaules of l/Lf for different aircraft configurations
# engine installed at the nose and has aft tail     - 0.6
# engines above the wing and has aft tail           - 0.55
# engine installed at the aft of fuselafe and has tail- 0.45
# engine installed under wing and has aft tail      - 0.5
# Glider                                            -   0.65
#####################################################################################
lopt_Lf=0.65

# Fuselage Length #
Lf=lopt/lopt_Lf

######################################################################################
# h0 : non-dimensional wing/fuselage aerodynamic center (Xac_wf/MAC) position - 0.2-0.25
# h  : non-dimensional aircraft cg position (X_cg/MAC) - must be known prior to horizontal tail design
#      best value for initial design - mid value between most forward and most aft cg i.e 0.2
# del_h : non-dimensional center of gravity limit- most aft cg- most forward cg - 0.1-0.3
# cg_c: aircraft cg during cruise with respect to fuselage length 
# cg_p: position of aircraft cg ahead of wing fuselage ac
#######################################################################################
h0=0.23
cg_c=0.32
cg_p=0.07 # in meters

Xapex=-h0*MAC+cg_c*Lf+cg_p # Location of wing leading edge from front fuselage tip
X_cg=h0*MAC-cg_p
X_bar_cg=h=X_cg/MAC

eff_h=0.98 # horizontal tail efficiency
h=0.114
# Required Horizontal Tail Coefficient at cruise #
C_Lh=(Cm0_wf+C_L*(h-h0))/(V_H)

#%% Choice of Airfoil for Horizontal Tail #
# Symmetric and Thinner than wing airfoil

# Airfoil Characteristics #
C_li=0
C_dmin=0.005
Cm=0
Cl_Cdmax=83.3
alpha_0=0
alpha_s=13
C_lmax=1.3
C_lalpha_h=6.7

#%% Horizontal Tail Parameters #
AR_h=2/3*AR
taper_ratio_h=taper_ratio
sweep_le_h=10
dihedral_angle_h=5
twist_angle_h=0.0001 # put 0.0001 if twist angle is 0.  

#%% Determine wing setting angle to produce required tail coefficient #

# Tail Lift Curve Slope #
C_Lalpha_heff=C_lalpha_h/(1+C_lalpha_h/(np.pi*AR_h))

# Tail angle of attack in cruise #
alpha_h=C_Lh/C_Lalpha_heff*57.3
alpha_h=-1.5
C_Lh_calc=llt.llt(S_h,AR_h,alpha_h,taper_ratio_h,twist_angle_h,C_Lalpha_heff,alpha_0)

C_Lcheck=C_Lh-C_Lh_calc
if (C_Lcheck>0):
    pass
else:
    raise ('C_L available less than C_L required')
    
# Downash angle at zero angle of attack #
epsilon_0=2*C_Lc/(np.pi*AR)
# Downwash slope #
deps_dalpha=2*C_Lalpha/(np.pi*AR)

#Downwash#
epsilon=(epsilon_0+deps_dalpha*i_w/57.3)*57.3

# Tail Setting Angle #
i_h=alpha_h-alpha_f+epsilon

# Determined Horizontal Tail Parameters #
b_h=(AR_h*S_h)**0.5
MAC_h=S_h/(b_h)
Cr_h=(1.5*(1+taper_ratio_h)*MAC_h)/(1+taper_ratio_h+taper_ratio_h**2)
Ct_h=taper_ratio_h*Cr_h

# Aircraft static longitudinal stability < 0 #
Cm_alpha=C_Lalpha*(h-h0)-C_Lalpha_heff*eff_h*S_h/S*(l/MAC-h)*(1-deps_dalpha)

