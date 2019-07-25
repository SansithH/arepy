import arepy as apy
import numpy as np

'''
Example:

grid = apy.coord.gridSquareXY([200,200],[0.4, 1.3, 4.3, 8.3])
'''

class grid:
    def __init__(self,bins,extent=None,points='centers',scatter=None,**opt):
        self.bins = [bins] if np.isscalar(bins) else bins
        self.nbins = [(b if np.isscalar(b) else len(b)) for b in self.bins]
        self.ndim = len(self.bins)
        self.scatter = scatter
        if extent is None:
            self.extent = np.array([[0,1],[0,1],[0,1]]) 
        else:
            self.extent = np.reshape(extent,(int(len(extent)/2),2),'C')
        if points=='centers':
            shift = [ (self.extent[b,1]-self.extent[b,0])*0.5/self.bins[b] for b in range(self.ndim) ]
            self.xi = [ np.linspace(self.extent[b,0],self.extent[b,1],self.bins[b],endpoint=False)+shift[b] for b in range(self.ndim) ]
        elif points=='edges':
            self.xi = [ np.linspace(self.extent[b,0],self.extent[b,1],self.bins[b]) for b in range(self.ndim) ] 
        coord,shape = self._setCoordinates(**opt)
        self.coords = coord
        self.shape = shape
        self.indexes = np.arange(len(coord)).reshape(tuple(shape))

    def _setScatter(self,coord):
        if self.scatter is not None:
            coord += (np.random.rand(len(coord),self.ndim)-0.5) * self.scatter
        return coord

    def __getitem__(self,index):
        if ~np.isscalar(index):
            index = self.indexes[index]
        return self.coords[index]

    # convert data to some standardized shape
    def reshapeData(self,data):
        return data

###########################
# Grid Volumes
###########################
class gridCube(grid):
    def _setCoordinates(self):
        self.xxi = np.meshgrid(*self.xi)
        # ordered as: x*ny*nz + y*nz + z
        coord = np.vstack([ np.ravel(self.xxi[1]), np.ravel(self.xxi[0]), np.ravel(self.xxi[2]) ]).T 
        self._setScatter(coord)

        self.npix = len(coord)
        self.data = {}

        # flat list of coordinates
        return coord, self.nbins

    def getPixFromCoord(self,coord):
        pixSize = (self.extent[:,1]-self.extent[:,0]) / self.nbins     # calculate pixel direction in each dimension
        coord = coord-self.extent[:,0]                                 # shift coordinates to origin
        return np.floor( coord / pixSize ).astype(int)                  # calculate pixel indexes        

    def addAtCoord(self,prop,coord,value):
        pix = self.getPixFromCoord(coord)
        self.addAtPix(prop,pix,value)

    def addAtPix(self,prop,pix,value):
        if np.ndim(pix)>1:          # use only particles within the extent
            ids =  (0<=pix[:,0])&(pix[:,0]<self.nbins[0]) 
            ids &= (0<=pix[:,1])&(pix[:,1]<self.nbins[1])
            ids &= (0<=pix[:,2])&(pix[:,2]<self.nbins[2])
            pix,value = pix[ids],value if np.isscalar(value) else value[ids]
            npix = len(pix)
        if prop not in self.data:   # create a new data if it does not exists
            dshape = np.array(value).shape[1:]
            dtype = np.array(value).dtype
            self.data[prop] = np.zeros(tuple(self.nbins)+dshape,dtype=dtype)
        np.add.at( self.data[prop], tuple(pix.T), value )
            

###########################
# Grid Surfaces
###########################
class gridSquareXY(grid):
    def _setCoordinates(self,zfill=None):
        self.xxi = np.meshgrid(*self.xi)
        # ordered as: x*ny + y
        coord = np.vstack([ np.ravel(self.xxi[1]), np.ravel(self.xxi[0]) ]).T 

        # flat list of coordinates
        if zfill is not None:
            coord = [[x,y,zfill] for (x,y) in coord]
        return coord, self.nbins

    def reshapeData(self,data):
        return data.reshape(self.nbins)

class gridFieldXY(gridSquareXY):
    def reshapeData(self,data):
        return data

class gridHealpix(grid):
    def _setCoordinates(self,zfill=None): 
        import healpix as hp
        nside = self.bins[0]
        npix = hp.nside2npix(nside)
        coord = np.zeros((npix,3))
        for i in range(npix):
            coord[i,:] = hp.pix2vec(nside,i)
        coord *= self.extent[0][1]
        return coord, [npix]

    def reshapeData(self,data):
        import healpix as hp
        # we rotate the mollview by 90 degrees around z-axis to properly match the x and y axes
        data = hp.visufunc.mollview(data,return_projected_map=True) #,rot=(135,0,0))
        return np.where(data==-np.inf,np.nan,data)

class gridDisc(grid):
    # Different parts of the disk can be located using offsets in 'self.parts'
    def __init__(self,bins,extent=None,points='edges',scatter=None,**opt):
        super().__init__(bins,extent,points,scatter,**opt)

    def _setCoordinates(self):
        coord = [[0,0,0]]
        self.parts = [1]
        for r,rb in enumerate(self.xi[0]):
            if r==0: continue
            lrbin = self.xi[0][r]-self.xi[0][r-1]  # radial bin length
            lcircle = 2 * np.pi * rb               # circumference length
            nabins = int(lcircle/lrbin)            # number of angular bins
            if nabins<2: continue
            self.parts.append( nabins )            # particle offests for different radii
            abins = np.linspace(0,2*np.pi,nabins,endpoint=False) # angular bins
            for a,ab in enumerate(abins):
                coord.append([rb*np.cos(ab),rb*np.sin(ab),0])
        self._setScatter(coord)
        self.split = np.cumsum(self.parts[:-1])    # particle split indexes
        return coord, [len(coord)]

    def reshapeData(self,data):
        return np.split(data, self.split)

###########################
# Grid Lines
###########################
class gridLine(grid):
    def _setCoordinates(self,yfill=None,zfill=None):
        coord = self.xi[0]
        self._setScatter(coord)
        self.parts = [len(coord)]
        # flat list of coordinates
        if zfill is not None and yfill is not None:
            coord = [[x,yfill,zfill] for x in coord]
        return coord, [len(coord)]

# carthesian line profiles X/Z
class gridLineXYZ(gridLine):
    def _setCoordinates(self,xfill=None,yfill=None,zfill=None):
        xcoord, shape = super()._setCoordinates(yfill=yfill,zfill=zfill)
        self.parts = self.parts+[len(self.xi[1]),len(self.xi[2])]  # update particle offset
        self.split = np.cumsum(self.parts[:-1])                    # update particle slit indexes
        ycoord = [[xfill,y,zfill] for y in self.xi[1]]        
        zcoord = [[xfill,yfill,z] for z in self.xi[2]]        
        return np.concatenate((xcoord,ycoord,zcoord),axis=0), [shape[0]+len(ycoord)+len(zcoord)]    

    def reshapeData(self,data):
        parts = np.split(data, self.split)
        return parts[0], parts[1], parts[2]

# polar line profiles R/Z
class gridLineRZ(gridDisc):
    def _setCoordinates(self,xfill=None,yfill=None):
        coord, shape = super()._setCoordinates()
        self.parts = self.parts+[len(self.xi[1])]  # update particle offset
        self.split = np.cumsum(self.parts[:-1])    # update particle slit indexes
        zcoord = [[xfill,yfill,z] for z in self.xi[1]]        
        return np.concatenate((coord,zcoord),axis=0), [shape[0]+len(zcoord)]

    def reshapeData(self,data):
        parts = np.split(data, self.split)
        rline = np.array([np.mean(parts[i]) for i in range(0,len(parts)-1)])
        return rline, parts[-1]