import math
import atmosphere
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
f=open('output.txt','w')

n=5
stall_margin=7 #m/s

#def round_value(func):
#    return round(func,n) 
##%% Mission Requirements
#f.write("Mission Requirements\n\n")
#endurance=0 #min
#f_range=30 #km
#stall_margin=7 #m/s
#min_airspeed=10 #m/s
#
#f.write('Endurance:{} min\t\tFlight Range:{} km\t\tStall Margin:{} m/s\t\tMinimum Airspeed:{} m\s\n '.format(endurance,f_range,stall_margin,min_airspeed))

#%% Payload Requirements
payload_mass=1 #kg
payload_power=0 #W

f.write('Pay Load Requirements\nPayload Mass:{} kg\t\tPayload Power Requirements:{} Watt\n'.format(payload_mass,payload_power))
#%% Aircraft
airframe_mass=1.952 # kg
avionics_power=0 #W
fuselage_drag_coeff=0.03 
zero_lift_drag_coeff=0.02

f.write('\nAircraft Requirements\nAirframe Mass:{} kg\t\tAvionics Power:{} Watt\t\tFuselage Drag Coefficient:{} \t\tZero Lift Coefficient "C_Do":{}\n'.format(airframe_mass,avionics_power,fuselage_drag_coeff,zero_lift_drag_coeff))

#%% Cruise Speed
cruise_speed=25 #m/s
cruise_altitude=2500 #m
#%% Environment
air_density,air_temperature=atmosphere.densityGradient(cruise_altitude)
#air_density=1.11
#print('Air Density:{} kg/m3'.format(air_density))

f.write('\nCruise Data\nCruise Speed:{} m/s\t\tCruise Altitude:{} m\t\tAir Density:{} kg/m3\t\t\nAir Temperture:{} K\n'.format(cruise_speed,cruise_altitude,round(air_density,n),round(air_temperature,n)))

#%% Propulsion and Batteries Inputs
battery_capacity=5300 #mah
battery_mass_single=.512 #kg
cell_volatage=4.2 #V
cell_in_series=4 
no_of_batteries=2
total_capacity_used=90 # %
overall_efficiency= 100# %


f.write('\nBattery and Propulsion Inputs\nBattery Capacity:{} mAh\t\tSingle Battery Mass:{} kg\t\tCell Voltage:{} V\t\tCell in Series:{}\nNumber of Battery:{}\t\t\t\tTotal Capacity Used:{} %\t\t\tOverall Propulsive Efficiency:{}\n'.format(battery_capacity,battery_mass_single,cell_volatage,cell_in_series,no_of_batteries,total_capacity_used,overall_efficiency))

#%% WIng Inputs
wing_loading= 12.5 #%%kg/m2  
aspect_ratio=8
taper_ratio=0.8
oswald_efficiency=1.78*(1-0.045*np.power(aspect_ratio,0.68))-0.64
max_lift_coefficient=1.5

f.write('\nWing Inputs\nWing Loading:{} kg/m2\t\tAspect Ratio:{}\t\tTaper Ratio:{}\t\tOswald Efficiency "e":{}\nMax Lift Coefficient "c_Lmax":{}\n'.format(wing_loading,aspect_ratio,taper_ratio,oswald_efficiency,max_lift_coefficient))

#%% Calculations
total_battery_capacity=no_of_batteries*battery_capacity
#print('Total Battery Capacity:{} mAh'.format(total_battery_capacity))
voltage=cell_volatage*cell_in_series
#print('Total Voltage:{} V:'.format(voltage))
battery_mass=no_of_batteries*battery_mass_single
#battery_mass=voltage*battery_capacity/energy_density/1000*no_of_batteries
#print('Battery mass:',battery_mass)
#total_mass=payload_mass+airframe_mass+battery_mass
total_mass=3.5
#print('Total Mass "m":',total_mass)
f.write('\nBattery Calculations\nTotal Battery Capacity:{} mAh\t\tTotal Voltage:{} V\t\tTotal Battery Mass:{} kg\n'.format(total_battery_capacity,voltage,battery_mass))
f.write('\nTotal Aircraft Mass:{} kg\n'.format(total_mass))

#%% Main Wing
wing_area=total_mass/wing_loading
b=(aspect_ratio*wing_area)**0.5/2
#print('Wing Area "S":',wing_area)
#print('Semi_span "b":',b)
root_chord=(2*wing_area)/(2*b*(1+taper_ratio))
#print('root_chord:',root_chord)
tip_chord=taper_ratio*root_chord
#print('Tip Chord:',tip_chord)
avg_chord=(tip_chord+root_chord)/2
#print('Average Chord:',avg_chord)

f.write('\nWing Calculations\nWing Area:{} m2\t\tSpan:{} m\t\tSemi-Span:{} m\nRoot Chord:{} m\t\tTip Chord:{} m\n'.format(round(wing_area,n),round(2*b,n),round(b,n),round(root_chord,n),round(tip_chord,n)))
#%%
mass_fraction=(battery_mass+payload_mass)/total_mass
#print('Mass Fraction:',mass_fraction)
f.write('Mass Fraction:{} %\n'.format(round(mass_fraction,n)*100))

k=1/(math.pi*oswald_efficiency*aspect_ratio)
min_drag_airspeed=(2*total_mass*9.81/(air_density*wing_area))**0.5*(k/(zero_lift_drag_coeff+fuselage_drag_coeff))**0.25
#print('Minimum Drag Speed "Vm":',min_drag_airspeed)

min_power_airspeed=min_drag_airspeed*1/(3)**(1/4)
#print('Minimum Power Speed "Vmp":',min_power_airspeed)

min_air_stallspeed=((2*total_mass*9.81)/(air_density*wing_area*max_lift_coefficient))**0.5
#print('Stall Speed "Vmin":',min_air_stallspeed)
stall_margin_calculated=cruise_speed-min_air_stallspeed
f.write('\nSpeed Calculations\nMinimum Drag Speed:{} m/s\t\tMinimum Power Speed:{} m/s\t\tStall Speed:{} m/s\n'.format(round(min_drag_airspeed,n),round(min_power_airspeed,n),round(min_air_stallspeed,n)))
c=0
#%% Lift Drag Calculation
def lift_drag_propulsion(velocity,c):
	c_L=((2*total_mass*9.81)/(air_density*wing_area*velocity**2))
	#print('Lift Coefficient "cL":',c_L)

	c_D=zero_lift_drag_coeff+fuselage_drag_coeff+c_L**2*k
	#print('Drag Coefficient "c_D":',c_D)

	drag=0.5*c_D*wing_area*air_density*velocity**2
	#print('Drag in newton":',drag)

	lift=drag*c_L/c_D
	#print('Lift in newton:',lift)
	lift_to_drag=c_L/c_D
	#print("Lift/Drag:",lift_to_drag)

	propulsive_power_required=drag*velocity/(overall_efficiency/100)
	
	i_prop=propulsive_power_required/voltage
	#print('Current Required for propeller:',i_prop)

#%% Current Required
	i_avio=avionics_power/voltage

	i_pay=payload_power/voltage

	total_current_required=i_prop+i_avio+i_pay

	time_of_flight=(total_battery_capacity/1000)*(total_capacity_used/100)/(i_prop+i_pay+i_avio)
	#print('Time of flight in minutes:',time_of_flight*60)

	total_range=time_of_flight*velocity
	#print('Total_range in km:',total_range*3600/1000)
	if c==0:
		print('Propulsive Power Required',propulsive_power_required) 
		f.write('\nLift Drag Calculations\nCoefficient of Lift "c_L":{}\t\tCoefficient of Drag "c_D":{}\t\tDrag:{} N\nLift:{} N\t\t\t\t\t\tLift to Drag Ratio "L/D":{}\n'.format(round(c_L,n),round(c_D,n),round(drag,n),round(lift,n),round(lift_to_drag,n)))
		f.write('\nStall Margin:{} m/s\t\tPropulsive Power Required:{} Watt\n'.format(round(stall_margin_calculated,n),round(propulsive_power_required,n)))
		f.write('\nCruise Propeller Current Requirement:{} A\t\tAvionics Current Requirement:{} A\nPayload Current Requirement:{}\t\t\t\t\t\tTotal Current Requirement:{} A\n'.format(round(i_prop,n),round(i_avio,n),round(i_pay,n),round(total_current_required,n)))
		f.write('\nTime of Flight:{} min\t\tTotal Range:{} km\n'.format(round(time_of_flight*60,n),round(total_range*3600/1000,n)))
		c=c+1
	return propulsive_power_required,time_of_flight,total_range,drag,lift

propulsive_power_required,time_of_flight,total_range,drag,lift=lift_drag_propulsion(cruise_speed,c)



#print('Calculated Stall Margin:',stall_margin_calculated)

#%% Requriement Fulfilled 
#range_re=f_range-total_range*3600/1000
#endurance_re=endurance-time_of_flight
#f.write('\n\nRange Requirement Fulfillment:{}\n'.format(range_re))

#%% Propeller Design
dia=0.254 #m
import propeller_design as pd
power,v_1,effi=pd.propeller_design(drag,cruise_speed,cruise_altitude,dia)
f.write('\n\nPropeller Design\nPropeller Shaft Power:{} Watt\t\tPropeller Outlet Velocity:{} m\s\t\tEfficieny:{}\n'.format(round(power,n),round(v_1,n),round(effi,n)))

#%%
f.close()

#%% Plot Generation
f1=open('output_plot.txt','w')
for v in range(6,41):
    propulsive_power_required,time_of_flight,total_range,drag,lift=lift_drag_propulsion(v,2)
    f1.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(v,round(time_of_flight*60,n),round(total_range*3600/1000,n),round(propulsive_power_required,n),round(drag,n),round(lift,n)))
f1.close()

f2=open('output_plot.txt','r')
x=[]
y=[]
z=[]
pr=[]
d=[]
l=[]
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
#
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

#l=np.array(l)
l_d=np.divide(l,d)
plt.figure(4)
plt.plot(x,l_d)
plt.xlabel('Velocity m/s')
plt.ylabel('Lift/Drag')
plt.show()


