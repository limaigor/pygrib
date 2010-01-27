from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pygrib
import numpy as np
try:
    import spharm
except:
    raise ImportError("requires pyspharm (python spherical harmonic module) from http://code.google.com/p/pyspharm")

grbs = pygrib.open('../sampledata/spectral.grb')
for g in grbs:
    if g['name'] == 'Temperature' and\
    g['scaledValueOfFirstFixedSurface']==99598:
        fld = g['values']
        break

print fld.min(), fld.max(), fld.shape
fldr = fld[0::2]
fldi = fld[1::2]
fld = np.zeros(fldr.shape,'F')
fld.real = fldr
fld.imag = fldi
nlons = 360;  nlats = 181
s = spharm.Spharmt(nlons,nlats)
print fld.real[0:10]
print fld.imag[0:10]
data = s.spectogrd(fld)
print data.min(),data.max()
lons = (360./nlons)*np.arange(nlons)
lats = 90.-(180./(nlats-1))*np.arange(nlats)
lons, lats = np.meshgrid(lons, lats)
# stack grids side-by-side (in longitiudinal direction), so
# any range of longitudes (between -360 and 360) may be plotted on a world map.
lons = np.concatenate((lons-360,lons),1)
lats = np.concatenate((lats,lats),1)
data = np.concatenate((data,data),1)
# setup miller cylindrical map projection.
m = Basemap(llcrnrlon=-180.,llcrnrlat=-90,urcrnrlon=180.,urcrnrlat=90.,\
            resolution='l',area_thresh=10000.,projection='mill')
x, y = m(lons,lats)
CS = m.contourf(x,y,data,15,cmap=plt.cm.jet)
ax = plt.gca()
pos = ax.get_position()
l, b, w, h = pos.bounds
cax = plt.axes([l+w+0.025, b, 0.025, h]) # setup colorbar axes
plt.colorbar(drawedges=True, cax=cax) # draw colorbar
plt.axes(ax)  # make the original axes current again
m.drawcoastlines()
# draw parallels
delat = 30.
circles = np.arange(-90.,90.+delat,delat)
m.drawparallels(circles,labels=[1,0,0,0])
# draw meridians
delon = 60.
meridians = np.arange(-180,180,delon)
m.drawmeridians(meridians,labels=[0,0,0,1])
plt.title(g['name']+' from Spherical Harmonic Coeffs')
plt.show()