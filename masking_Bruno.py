#%%
import numpy as np
import matplotlib.pyplot as plt

Nx = 640
Ny = 320
rho = 0.4
print('tbd should be chosen such that there are ' + str(int(Nx*Ny*rho)) + ' sampling points after masking.')
tbd = 10
x = np.round(np.random.normal(Nx//2, Nx//3, tbd)).astype(int)
y = np.round(np.random.normal(Ny//2, Ny//3, tbd)).astype(int)
ind = np.where(np.logical_and(np.logical_and(x>=0, x<Nx),np.logical_and(y>=0, y<Ny)))
sampling = np.stack((x[ind],y[ind]),1)
mask = np.zeros((Nx,Ny), dtype=bool)
mask[x[ind],y[ind]] = True
unique, counts = np.unique(sampling, return_counts=True, axis=1)
print('There are ' + str(np.sum(mask)) + ' sampling locations before masking.')
plt.scatter(sampling[:,0],sampling[:,1],s=0.1)
plt.show()
#%%