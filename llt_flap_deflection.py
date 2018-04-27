def llt(S,AR,i_w,lambdai,twist_angle,C_lalpha,alph_0,alph_0_fd,):
	import numpy as np
	import matplotlib.pyplot as plt

	N=9 # number of segments
	# S=18.1
	# AR=7
	# lambdai=0.8 # Aspect Ratio
	# twist_angle=-1.5 # Twist angle
	# i_w=10 # Wing Swtting Angle
	# C_lalpha=6.3 # Lift curve slope
	# alph_0=-3 # flap up zero-lift angle of attack deg
	# alph_0_fd=-6 #flap down zero lift angle of attack def
	b=(AR*S)**0.5 
	bf_b=0.6 # flap-to-wing span ratio
	MAC=S/b
	Croot=(1.5*(1+lambdai)*MAC)/(1+lambdai+lambdai**2)
	theta=np.arange(np.pi/(2*N),np.pi/2+np.pi/(2*N),np.pi/(2*N))
	if i_w>0 and twist_angle>=0:
		alpha= np.arange(i_w+twist_angle,i_w-0.5*twist_angle/(N-1),-twist_angle/(N-1))
	else:
		alpha= np.arange(i_w+twist_angle,i_w-twist_angle/(N-1),-twist_angle/(N-1))	
	alpha_0=np.zeros(N)
	for i in range(1,N+1):
		if (i/N)>(1-bf_b):
			alpha_0[i-1]=alph_0_fd # flap down zero lift AOA
		else:
			alpha_0[i-1]=alph_0 # Flap up zero lift AOA
	z=(b/2)*np.cos(theta)
	c=Croot*(1-(1-lambdai)*np.cos(theta)) #% Mean Aerodynamics Chord at each segment (m)
	mu= c * C_lalpha / (4 * b)
	LHS = mu*(alpha-alpha_0)/57.3
	
	B=np.zeros((N,N))
	for i in np.arange(1,N+1):
		for j in np.arange(1,N+1):
			B[i-1][j-1]=np.sin((2*j-1)*theta[i-1]) * (1 + (mu[i-1] * (2*j-1)) /np.sin(theta[i-1]))

	A = np.linalg.solve(B, LHS)
	sum1=np.zeros((N))
	sum2=np.zeros((N))
	for i in np.arange(N):
		for j in np.arange(N):
			sum1[i] = sum1[i] + (2*(j+1)-1) * A[j]*np.sin((2*(j+1)-1)*theta[i]);
			sum2[i] = sum2[i] + A[j]*np.sin((2*(j+1)-1)*theta[i]);

	# CL = 4*b*sum2/ c;
	# print(CL)
	# CL1=np.hstack((np.array([0]),CL))
	# y_s=np.hstack((np.array(b/2),z))
	# print(y_s)

	# plt.figure(1)
	# plt.plot(1)
	# plt.plot(y_s,CL1)
	# plt.xlabel('Semi-span location (m)')
	# plt.ylabel('Lift coefficient') 
	# plt.axis([0, b/2, 0, 0.4])
	# plt.grid(True)
	CL_wing = np.pi * AR * A[0]
	return CL_wing
#