import math
#%% Inputs
wing_area=0.377 #m2
mac=0.218
span=1.74

#%% Horizontal Stabilizer
hvolume_ratio=0.6
hmoment_arm=0.8
haspect_ratio=4
htaper_ratio=0.8
harea=hvolume_ratio*mac*wing_area/hmoment_arm
print("Harea:",harea)
hsemi_span=(haspect_ratio*harea)**0.5/2
print('Hsemi:',hsemi_span)
hroot_chord=(2*harea)/(2*hsemi_span*(1+htaper_ratio))
print("Hroot:",hroot_chord)
htip_chord=htaper_ratio*hroot_chord
print("Htip:",htip_chord)
sweep_angle=math.atan((hroot_chord-htip_chord)*0.75)/hsemi_span*180/math.pi
print('Sweep Angle:',sweep_angle)

#%% Vertical Stabilizer
vvolume_ratio=0.035
vmoment_arm=0.8
v_aspect_ratio=2
vtaper_ratio=0.7
varea=vvolume_ratio*wing_area*span/vmoment_arm
print('Varea:',varea)
vspan=(v_aspect_ratio*varea)**0.5
print('Vertical Span',vspan)
vroot_chord=(2*varea)/(vspan*(1+vtaper_ratio))
print("vroot_chord:",vroot_chord)
vtip_chord=vtaper_ratio*vroot_chord

print("vtip_chord:",vtip_chord)
#%% Rate of climb
# R_C=5
# power_for_rateofclimb=(total_mass-1)*9.81+500
# print(power_for_rateofclimb)