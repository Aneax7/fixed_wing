import numpy as np
import scipy as sp
import atmosphere
import matplotlib.pyplot as plt
f=open('reverse.txt','w')
n=5
#%% Inputs %%#
payload_power=0
payload=0
root_chord=0.235
tip_chord=0.185
#semi_span=0.9
span=1.7
wing_area=0.28
total_mass=2.5   #gross mass of aircraft
cruise_speed=18 #m/s
cruise_altitude=2500 #m
zero_lift_drag_coeff=0.03
fuselage_drag_coeff=0.02
max_lift_coefficient=1.5
#%% Propulsion and Batteries Inputs
battery_capacity=5300 #mah
battery_mass_single=.512 #kg
cell_volatage=4.3 #V
cell_in_series=4 
no_of_batteries=1
total_capacity_used=90 # %
overall_efficiency= 100# %
avionics_power=0 #W

#%% Environment %%#
air_density,air_temperature=atmosphere.densityGradient(cruise_altitude)

#%% Battery Calculations %%#
total_battery_capacity=no_of_batteries*battery_capacity

voltage=cell_volatage*cell_in_series

battery_mass=no_of_batteries*battery_mass_single

#%% Wing Parameters Calclation %%#

taper_ratio=tip_chord/root_chord
#wing_area=span/2*(root_chord+tip_chord)

wing_loading=total_mass/wing_area
aspect_ratio=span**2/wing_area
oswald_efficiency=1.78*(1-0.045*np.power(aspect_ratio,0.68))-0.64
mac=2/3*root_chord*((1+taper_ratio+taper_ratio**2)/(1+taper_ratio))
y_mac=span/6*((1+2*taper_ratio)/(1+taper_ratio))

f.write('\nWing Calculations\nWing Area:{} m2\t\tSpan:{} m\t\tWing Loading:{} kg/m2\nAspect Ratio:{} \t\tTaper Ratio:{} \n'.format(round(wing_area,n),round(span,n),round(wing_loading,n),round(aspect_ratio,n),round(taper_ratio,n)))
f.write('\nOswald Efficiency:{}\t\tMean Aerodynamic Chord:{} m\n'.format(round(oswald_efficiency,n),round(mac,n)))

k=1/(np.pi*oswald_efficiency*aspect_ratio)
print("k:",k)
min_drag_airspeed=(2*total_mass*9.81/(air_density*wing_area))**0.5*(k/(zero_lift_drag_coeff+fuselage_drag_coeff))**0.25
min_power_airspeed=min_drag_airspeed*1/(3)**(1/4)
min_air_stallspeed=((2*total_mass*9.81)/(air_density*wing_area*max_lift_coefficient))**0.5
stall_margin_calculated=cruise_speed-min_air_stallspeed
f.write('\nSpeed Calculations\nMinimum Drag Speed:{} m/s\t\tMinimum Power Speed:{} m/s\t\tStall Speed:{} m/s\n'.format(round(min_drag_airspeed,n),round(min_power_airspeed,n),round(min_air_stallspeed,n)))

c=0
def lift_drag_propulsion(velocity,c):
	c_L=((2*total_mass*9.81)/(air_density*wing_area*velocity**2))

	c_D=zero_lift_drag_coeff+fuselage_drag_coeff+c_L**2*k

	drag=0.5*c_D*wing_area*air_density*velocity**2

	lift=drag*c_L/c_D

	lift_to_drag=c_L/c_D

	propulsive_power_required=drag*velocity/(overall_efficiency/100)
	
	i_prop=propulsive_power_required/voltage

#%% Current Required
	i_avio=avionics_power/voltage

	i_pay=payload_power/voltage

	total_current_required=i_prop+i_avio+i_pay

	time_of_flight=(total_battery_capacity/1000)*(total_capacity_used/100)/(i_prop+i_pay+i_avio)

	total_range=time_of_flight*velocity

	if c==0:
		print('Propulsive Power Required',propulsive_power_required) 
		f.write('\nLift Drag Calculations\nCoefficient of Lift "c_L":{}\t\tCoefficient of Drag "c_D":{}\t\tDrag:{} N\nLift:{} N\t\t\t\t\t\tLift to Drag Ratio "L/D":{}\n'.format(round(c_L,n),round(c_D,n),round(drag,n),round(lift,n),round(lift_to_drag,n)))
		f.write('\nStall Margin:{} m/s\t\tPropulsive Power Required:{} Watt\n'.format(round(stall_margin_calculated,n),round(propulsive_power_required,n)))
		f.write('\nCruise Propeller Current Requirement:{} A\t\tAvionics Current Requirement:{} A\nPayload Current Requirement:{}\t\t\t\t\t\tTotal Current Requirement:{} A\n'.format(round(i_prop,n),round(i_avio,n),round(i_pay,n),round(total_current_required,n)))
		f.write('\nTime of Flight:{} min\t\tTotal Range:{} km\n'.format(round(time_of_flight*60,n),round(total_range*3600/1000,n)))
		c=c+1
	return propulsive_power_required,time_of_flight,total_range,drag,lift

propulsive_power_required,time_of_flight,total_range,drag,lift=lift_drag_propulsion(cruise_speed,c)
f.close()

#%% Plot Generation
f1=open('output_plot.txt','w')
for v in range(6,41):
    propulsive_power_required,time_of_flight,total_range,drag,lift=lift_drag_propulsion(v,2)
    f1.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(v,round(time_of_flight*60,n),round(total_range*3600/1000,n),round(propulsive_power_required,n),round(drag,n),round(lift,n)))
f1.close()

f2=open('output_plot.txt','r')
x,y,z,pr,d,l=[],[],[],[],[],[]

for line in f2:
    p = line.split()
    x.append(float(p[0]))
    y.append(float(p[1]))
    z.append(float(p[2]))
    pr.append(float(p[3]))
    d.append(float(p[4]))
    l.append(float(p[5]))
plt.figure(1)
plt.plot(1)
plt.plot(cruise_speed*np.ones(2),[1,np.max(y)+50],label='cruise speed')
plt.plot(min_air_stallspeed*np.ones(2),[1,np.max(y)+50],label='min speed')
plt.plot(x,y,label='time of flight "min"')
plt.plot(x,z,label='range "km"')
plt.xlabel('Velocity m/s')
plt.ylabel('Flight Time and Range')
plt.legend(bbox_to_anchor=(0.5, 1), loc=2, borderaxespad=0.) 

plt.figure(2)
plt.plot(x,pr)
plt.xlabel('Velocity m/s')
plt.ylabel('Propulsive Power Required') 

plt.figure(3)
plt.plot(x,d,label='Drag')
plt.plot(x,l,label='Lift')
plt.xlabel('Velocity m/s')
plt.ylabel('Lift Drag "N"') 
plt.legend(bbox_to_anchor=(0.5, 1), loc=2, borderaxespad=0.) 

l_d=np.divide(l,d)
plt.figure(4)
plt.plot(x,l_d)
plt.xlabel('Velocity m/s')
plt.ylabel('Lift/Drag')
plt.show()