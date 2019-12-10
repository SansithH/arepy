import numpy as np
import arepy as apy
import copy

class subplot:
    """Subplot of a figure
    
    :param int figure: Figure number
    :param int row: Subplot row
    :param int col: Subplot column
    :param bool xyz: Use 3D axes

    .. note:
        
        3D axes works just with a standard matplotlib subplot class.
        It is not possible to use it for 'gridspec', 'imagescpec' or 'axesgrid' plotting classes.
    """
    # Initialize the subplot
    def __init__(self, figure, row, col, xyz=False, **opt):
        self.figure = figure                  # parent figure class
        self.row = row                        # row on the grid
        self.col = col                        # column on the grid
        self.index = row*figure.ncols+col     # subplot index
        self.xyz = xyz
        
        # set options and canvas
        self.opt = figure.opt.copy()  
        self.opt.update(opt)

        self.canvas = {
            'subplot': [self.index,self.row,self.col,self.xyz],      # subplot properties
            'empty': True,      # is canvas empty
            'colorbar': None,   # colorbar of the image
            'colorbarNA': None, # colorbar on a new axis
            'legend': None,     # standard plot legend
            'legendLS': None,   # plot linestyle legend
            'legendM': None,    # plot marker legend
            'other': [],        # other canvas objects
            'axis': {           # axis properties
                'xpos':   'bottom',     # x axis position
                'ypos':   'left',       # y axis position
                'xscale': 'lin',        # x axis scale
                'yscale': 'lin',        # y axis scale
                'tscale': 'lin',        # twin y axis scale
            },
        }
        rc = '%d%d'%(self.row,self.col)
        self.xnorm = 'xnorm_'+rc  # x-axis norm
        self.ynorm = 'ynorm_'+rc  # y-axis norm
        self.znorm = 'znorm_'+rc  # z-axis or image norm
        self.tnorm = 'tnorm_'+rc  # twin y-axis norm
        
        self.twinx = False

    # Setting options
    def setOption(self,**args):
        """Set an option"""
        for key,value in args.items():
            self.opt[key] = value

    # Standard way how to set a norm for the subplot
    def setNorm(self,xdata=None,ydata=None,zdata=None,
                xname=None,yname=None,zname=None,twinx=False,zlim=None):
        if xdata is not None:
            self.xnorm = self.figure.norms.setNorm(xdata,self.xnorm if xname is None else xname)
        if ydata is not None:
            if twinx:
                self.twinx = True
                self.tnorm = self.figure.norms.setNorm(ydata,self.tnorm if yname is None else yname)
            else:
                self.ynorm = self.figure.norms.setNorm(ydata,self.ynorm if yname is None else yname)        
        if zdata is not None:
            if zlim is not None: # clip data within the limit range
                zdata = np.clip(zdata,zlim[0],zlim[1])
            self.znorm = self.figure.norms.setNorm(zdata,self.znorm if zname is None else zname)
                    
    # Add unique objects to the canvas

    def setLegend(self, handles=None, labels=None, **nopt):
        """Set a legend
        
        :param list handles: List of axis object handles (optional)
        :param list[str] labels: Labels
        """
        if 'loc' in nopt and isinstance(nopt['loc'],str):
            nopt['loc'] = nopt['loc'].replace('bottom','lower').replace('top','upper')
        self.canvas['legend'] = {'draw':'legend','handles':handles,'labels':labels,'nopt':nopt}

    def setLegendLS(self, linestyles, labels, color='black', **nopt):
        """Set a line-style legend
        
        :param list[str] linestyle: A set of matplotlib line styles
        :param list[str] labels: Line style labels

        Example::
            
            sp.setLegendLS([':','--'],['foo','bar'])
        """
        if 'loc' in nopt and isinstance(nopt['loc'],str):
            nopt['loc'] = nopt['loc'].replace('bottom','lower').replace('top','upper')
        self.canvas['legendLS'] = {'draw':'legendLS','ls':linestyles,'labels':labels,'color':color,'nopt':nopt}

    def setLegendM(self, markers, labels, color='black', **nopt):
        """Set a marker legend

        :param list[str] markers: A set of matplotlib markers
        :param list[str] labels: A set of marker labels
        
        Example::
            
            sp.setLegendM(['s','^'],['foo','bar'])
        """
        if 'loc' in nopt and isinstance(nopt['loc'],str):
            nopt['loc'] = nopt['loc'].replace('bottom','lower').replace('top','upper')
        self.canvas['legendM'] = {'draw':'legendM','markers':markers,'labels':labels,'color':color,'nopt':nopt}

    def addImage(self, data, extent=(0,1,0,1), norm=None, normType='lin', 
                 normLim=None, xnorm=None, ynorm=None, **kwargs):
        """Add an image
        
        A thin wrapper around the matplotlib imshow class, that additionally sets the image normalization.

        :param [[float]*Y]*X data: Image pixel data on an x and y axis 
        :param tuple[float] extent: Extent of the x and y axis
        :param str norm: Name of the image normalization.
        :param str normType: Type of the norm: 'lin' or 'log'
        :param str xnorm: Name of the x-axis normalization
        :param str ynorm: Name of the y-axis normalization
        """
        xextent = extent[:,:2] if np.ndim(extent)>1 else extent[:2]
        yextent = extent[:,2:] if np.ndim(extent)>1 else extent[2:]
        self.setNorm(xdata=xextent,ydata=yextent,zdata=data,
                     xname=xnorm,yname=ynorm,zname=norm,
                     zlim=normLim)        
        if xnorm is None: self.setOption(xlim=xextent)
        if ynorm is None: self.setOption(ylim=yextent)
        self.canvas['other'].append({'draw':'image','twinx':False,
                                     'data':data,'norm':self.znorm,'normType':normType,
                                     'extent':extent,'kwargs':kwargs})

    def setColorbar(self, location='right', label=None):
        """Set a colorbar

        :param str location: top/right
        """
        self.canvas['colorbar'] = {'location':location,'label':label}

    def setColorbarNA(self, pos, **nopt):
        """Plot a colorbar on arbitrary position
        
        Example::
            
            grp.setColorbarNA(pos=(1.0,0.2,0.01,0.6),label='Mass (g)')
        """
        opt = {'location':'right','label':None}
        opt.update(nopt)
        self.canvas['colorbarNA'] = {'pos':pos,**opt}
        
    def addPlot(self, x, y, twinx=False, xnorm=None, ynorm=None, **nopt):
        """Add a plot to the canvas"""
        self.setNorm(xdata=x,ydata=y,xname=xnorm,yname=ynorm,twinx=twinx)
        opt = {'lw': 1}
        opt.update(nopt)
        self.canvas['other'].append({'draw':'plot','twinx':twinx,'x':x,'y':y,'kwargs':opt})

    def addStep(self, x, y, twinx=False, xnorm=None, ynorm=None, **nopt):
        """Add a step plot to the canvas"""
        self.setNorm(xdata=x,ydata=y,xname=xnorm,yname=ynorm,twinx=twinx)
        opt = {'lw': 1}
        opt.update(nopt)
        self.canvas['other'].append({'draw':'step','twinx':twinx,'x':x,'y':y,'kwargs':opt})

    def addScatter(self, *coord, xnorm=None, ynorm=None,**nopt):
        """Add a scatter to the canvas"""
        opt = {} # default 'c':'black' will disable 'facecolor' and 'edgecolor' !!!
        opt.update(nopt)
        self.setNorm(xdata=coord[0],ydata=coord[1],xname=xnorm,yname=ynorm)
        x,y,z = coord if self.canvas['subplot'][3] else (coord[0],coord[1],None)
        self.canvas['other'].append({'draw':'scatter','twinx':False,'x':x,'y':y,'z':z,'opt':opt})
        
    def addQuiver(self, *coord, **nopt):
        """Add quivers to the canvas"""
        self.canvas['other'].append({'draw':'quiver','twinx':False,'coord':coord,'kwargs':nopt})

    def addBar(self, x, y, twinx=False, **nopt):
        """Add a barplot to the canvas"""
        self.canvas['other'].append({'draw':'bar','twinx':twinx,'x':x,'y':y,'kwargs':nopt})

    def addLine(self, axis, pos, twinx=False, **nopt):
        """Add a line to the plot"""
        opt = {'color':'grey', 'ls':'-', 'label':'', 'lw': 1}
        opt.update(nopt)
        self.canvas['other'].append({'draw':'line','twinx':twinx,'pos':pos,'axis':axis,'kwargs':opt})
        
    def addCircle(self, center, radius, twinx=False, **nopt):        
        """Add a circle to the plot"""
        opt = {'color':'black'}
        opt.update(nopt)
        self.canvas['other'].append({'draw':'circle','twinx':twinx,'center':center,
                                     'radius':radius,'kwargs':opt})
        
    def addRectangle(self, xy, width, height, **nopt):
        """Add a rectangle to the plot"""
        opt = {'color':'grey'}
        opt.update(nopt)
        self.canvas['other'].append({'draw':'rectangle','twinx':False,'xy':xy,
                                     'width':width,'height':height,'kwargs':opt})

    def addText(self, text, loc, bgcolor=None, twinx=False, padding=None, **nopt):
        """Add text to the figure
        
        :param src text: Text string
        :param str loc: Location of the text on the plot
        :param (float)*2 padding: Padding of the text (horizontal,vertical)
        """
        opt = {'color':'black', 'fontsize': 8}
        opt.update(nopt)
        self.canvas['other'].append({'draw':'text','twinx':twinx,'loc':loc,'text':text,
                                     'bgcolor':bgcolor,'padding':padding,'kwargs':opt})


    # Read dataset and add its objects to the canvas
    def readDataset(self, sim, snaps):
        return apy.plot.dataset(self, sim, snaps)

    # Plot all canvas object on the given axis
    def getCanvas(self):

        # create a deep copy of the canvas
        canvas = copy.deepcopy(self.canvas)

        figs = range(self.figure.nfigs)

        # add all axis options
        axOpt = ['title','xlabel','ylabel','zlabel','xlim','ylim','zlim','xscale','yscale',
                 'tlabel','tlim','tscale','group','xflip','xpos','ypos','projection',
                 'xticklabels','yticklabels','xtickparam','ytickparam','tickparam','xysame',
                 'xtickformat']
        for opt in axOpt:
            if opt in self.opt:
                if self.opt[opt] is None: # remove if set to None
                    del self.opt[opt]
                    continue
                canvas['axis'][opt] = self.opt[opt]

        # transform x and y limits
        xnorm = self.figure.norms.getLimits(self.xnorm)
        ynorm = self.figure.norms.getLimits(self.ynorm)
        if 'xlim' not in canvas['axis'] and xnorm is not None:    
            xnormmin = xnorm[1] if canvas['axis']['xscale']=='log' else xnorm[0]
            canvas['axis']['xlim'] = [xnormmin,xnorm[2]]
        if 'ylim' not in canvas['axis'] and ynorm is not None:
            ynormmin = ynorm[1] if canvas['axis']['yscale']=='log' else ynorm[0]
            canvas['axis']['ylim'] = [ynormmin,ynorm[2]]

        # transform t limits
        if self.twinx:
            tnorm = self.figure.norms.getLimits(self.tnorm)
            if 'tlim' not in canvas['axis'] and tnorm is not None:
                tnormmin = tnorm[1] if canvas['axis']['tscale']=='log' else tnorm[0]
                canvas['axis']['tlim'] = [tnormmin,tnorm[2]]

        # flip x axis
        if 'xflip' in canvas['axis'] and canvas['axis']['xflip']:
            canvas['axis']['xlim'] = [canvas['axis']['xlim'][:,1],canvas['axis']['xlim'][:,0]]
            
        # prepare multiple objects
        for i,d in enumerate(canvas['other']):
            if d['draw']=='text':
                if not isinstance(d['loc'],str):
                    canvas['other'][i]['loc'] = d['loc']
            if d['draw']=='scatter':
                canvas['other'][i]['x'] = d['x']
                canvas['other'][i]['y'] = d['y']
            if d['draw']=='image':
                norm = self.figure.norms.getLimits(d['norm'])
                if norm is None:
                    apy.shell.printc("\nWarning: Image overlay norm '%s' is None and will be ignored! (subplot.py)"%d['norm'],'r')                    
                canvas['other'][i]['norm'] = norm
                
        return canvas
    
