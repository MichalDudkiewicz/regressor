# unimodal test function
import numpy
from numpy import arange
from numpy import meshgrid
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

# objective function
def objective(x, y):
	return 2 * x ** 2 + 3 * y ** 2 + 12


if __name__ == '__main__':
	# define range for input
	r_min, r_max = -5.0, 5.0
	# sample input range uniformly at 0.1 increments
	xaxis = arange(r_min, r_max, 0.1)
	yaxis = arange(r_min, r_max, 0.1)
	# create a mesh from the axis
	x, y = meshgrid(xaxis, yaxis)
	# compute targets
	results = objective(x, y)
	# create a surface plot with the jet color scheme
	axis = pyplot.axes(projection='3d')
	axis.plot_surface(x, y, results, cmap='jet')

	step = 1.0
	sigma = 0.01  # std dev
	for x in numpy.arange(r_min, r_max + 0.01, step):
		for y in numpy.arange(r_min, r_max + 0.01, step):
			print(numpy.random.normal(y, sigma, 1)[0], numpy.random.normal(x, sigma, 1)[0], numpy.random.normal(objective(x, y), sigma, 1)[0])

	# show the plot
	pyplot.show()