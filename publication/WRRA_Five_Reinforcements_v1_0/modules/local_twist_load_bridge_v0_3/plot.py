from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent;a=np.load(P/'3D_plane.npz');raw=a['raw'];out=a['projected'];mag=a['field_magnitude'];n=mag.shape[0]
k=np.fft.fftfreq(n,d=1/n);kx,ky=np.meshgrid(k,k,indexing='ij')
curl=np.fft.ifftn(1j*kx*np.fft.fftn(raw[1])-1j*ky*np.fft.fftn(raw[0])).real
correction=np.sqrt(np.sum((raw-out)**2,axis=0))/np.sqrt(np.sum(raw**2,axis=0))*100
fig,axes=plt.subplots(1,3,figsize=(11.8,3.7),layout='constrained')
for ax,arr,title,cmap,label in zip(axes,[mag,curl,correction],['Prescribed source-field magnitude','Curl from direct RAR scaling','Required potential-field correction'],['viridis','coolwarm','magma'],['|g_N| / a_T','Dimensionless curl z','Local vector difference (%)']):
 im=ax.imshow(arr.T,origin='lower',extent=[0,16,0,16],cmap=cmap,aspect='equal');ax.set(xlabel='x (kpc)',ylabel='y (kpc)',title=title);fig.colorbar(im,ax=ax,shrink=.82,label=label)
fig.suptitle('Conditional periodic 3D test; positive background plus contrast and prescribed harmonic field',fontsize=11)
fig.savefig(P/'three_dimensional_receiver.png',dpi=180);plt.close(fig)
