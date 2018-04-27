def llt(S,AR,i_w,lambdai,twist_angle,C_lalpha,alpha_0):
	import numpy as np
	import matplotlib.pyplot as plt

	N=9
	# S=18.1
	# AR=8
	# lambdai=0.6 #taper ratio
	# twist_angle=-1
	# i_w=2 # wing setting angle
	# C_lalpha=6.3 # Lift cureve slope
	# alpha_0=-1.5 #zero lift angle of attack
	b=(AR*S)**0.5
	MAC=S/b
	Croot=(1.5*(1+lambdai)*MAC)/(1+lambdai+lambdai**2)
	theta=np.arange(np.pi/(2*N),np.pi/2+np.pi/(2*N),np.pi/(2*N))
	if i_w>0 and twist_angle>0:
		alpha= np.arange(i_w+twist_angle,i_w,-twist_angle/(N-1))
	else:
		alpha= np.arange(i_w+twist_angle,i_w-twist_angle/(N-1),-twist_angle/(N-1))
	print(len(alpha))
	z=(b/2)*np.cos(theta)
	c=Croot*(1-(1-lambdai)*np.cos(theta)) #% Mean Aerodynamics Chord at each segment (m)
	mu= c * C_lalpha / (4 * b)
	print(len(mu))
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

	CL = 4*b*sum2/ c;
	CL1=np.hstack((np.array([0]),CL))
	y_s=np.hstack((np.array(b/2),z))
	

	plt.figure(1)
	plt.plot(1)
	plt.plot(y_s/(b/2),CL1)
	plt.xlabel('Semi-span location (m)')
	plt.ylabel('Lift coefficient') 
	#plt.axis([0, b/2, 0, 0.4])
	plt.grid(True)
	CL_wing = np.pi * AR * A[0]
	plt.show()
	return CL_wing