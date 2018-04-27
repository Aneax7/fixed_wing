import scipy as sp
from scipy import optimize
import atmosphere
def propeller_design(f_prop,v_0,h,dia):
#    f_prop=6.07
#    v_0=16.75
     density,air_temperature=atmosphere.densityGradient(1000)
#    dia=0.254
     a_p=sp.pi*(dia)**2/4
     def propeller_eqn(p):
        sip,v_1=p
        f1=sip-(0.5*(v_1/v_0)**3+1.5*(v_1/v_0)**2-0.5*(v_1/v_0)-1.5)*0.5*density*v_0**3*a_p
        f2=f_prop-density*(v_1+v_0)*0.5*a_p*(v_1-v_0)
        return f1,f2
     sip, v_1 = sp.optimize.fsolve(propeller_eqn, (20, 20))
     effi=f_prop*v_0/(density*a_p*(v_1+v_0)/2*(v_1**2-v_0**2)/2)
     return sip,v_1,effi