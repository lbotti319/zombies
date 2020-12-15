import matplotlib.pyplot as plt

def basic_plot(solution):
    plt.plot(solution.t, solution.y.T[:,:3])
    plt.xlabel('t')
    plt.legend(['Susceptibles', 'Zombies', 'Undead'], shadow=True, loc='upper right')
    plt.title('Population Changes Over Time')
    plt.show()


def behavior_plot(solution):
	fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=[15,8])

	ax1.plot(solution.t, solution.y.T[:,[0,1,2,3]])
	ax1.set_xlabel('t')
	ax1.legend(['Susceptibles', 'Zombies', 'Exposed', 'Quarantined'], shadow=True, loc='upper right')
	ax1.set_title('Population Changes Over Time')

	ax2.plot(solution.t, solution.y.T[:,[5,6]])
	ax2.set_xlabel('t')
	ax2.legend(['x_S', 'x_E'], shadow=True, loc='upper right')
	ax2.set_title('Population Support')

	ax3.plot(solution.t, solution.y.T[:,[7]])
	ax3.set_xlabel('t')
	ax3.legend(['Loss'], shadow=True, loc='upper right')
	ax3.set_title('Socio-Economic Loss from murder')


	plt.show()