import scipy.io
import numpy as np
from pylab import plot, xlabel, ylabel, show, title, scatter, imshow, colorbar, xlim
# Load the .mat file in
data = scipy.io.loadmat('P1_36')
# Print to see what you are dealing with, as well as the the variable type
print(data)
print(type(data))
# The data is a dictionary so we use data.keys to find where the data is?
print(data.keys())
# Find the type of data that is being stored and how much of it there is
print(type(data['Pperp1e']), data['Pperp1e'].shape)
# Check what type each entry in the array is
#print("Hello")
#print(type(data['P1'][0][0]),data['P1'][0][0].shape)
# Make a color graph of the correct data in the file
abs_data = np.absolute(data['Pperp1e'])
sumbx = np.sum(abs_data, 0) # line of x vals,
print(abs_data.shape)
print(sumbx.shape)
x_pos_of_xline = np.argmin(sumbx) # first index
zcut_of_xline = abs_data[:,x_pos_of_xline]
z_pos_of_xline = np.argmin(zcut_of_xline) # zeroth index

print(x_pos_of_xline)
print(z_pos_of_xline)

imshow(data['Pperp1e'],cmap= "jet")
# # print("wow")
# #print(data['bx'])
# colorbar()
show()


