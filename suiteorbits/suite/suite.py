from abc import ABC, abstractmethod
import numpy as np
from ..constants import orbitMethods, suiteValues
from .initializers import _initializer
from ..plot import plot, scatter
import galpy
import warnings


class Suite():
    '''
    Suite class for exploring n parameters.
    '''
    def __init__(self,
                 dim_res=100, 
                 pot=None, 
                 integ_time={'t_start':0.0, 't_end':10.0, 'steps':10000}, 
                 integ_kwargs={},
                 init_kwargs={}, 
                 show_updates = True,
                 auto_run = True,
                 **kwargs
                 ):
        '''
        Attributes
        ----------
        **kwargs 
            Keyword arguments to pass to the initializer function.

        dim_res : float (1D) or list
            number of orbits to explore for each dimension, in order of the way they were passed in *args.

        potential : galpy.potential.Potential
            The galpy potential object to use for the suite.

        integ_time : dict
            Dictionary with the start, end, and number of timesteps for the integration.

        integ_kwargs : dict
            Keyword arguments to pass to the integration function.

        init_kwargs : dict
            Additional keyword arguments to pass to the initializer function.
        
        show_updates : bool
            Print updates to the console.
        
        auto_run : bool
            Automatically run the suite after initialization, using the potential used to make the particles.
            Can bypass this feature by setting auto_run=False and integrating the suite manually with .integrate().

        Methods
        -------
        plot(d1, d2, color_by=None, orb_inds=None, time_inds=None, style='line', **kwargs)
            Plot the orbits in the suite.        
        '''
        #     assert dim_ranges.shape == (2,), \
        #         f"'dim_ranges' must have shape (2,) but it has shape {dim_ranges.shape}"
        #     assert isinstance(dim_steps, int), \
        #         f"'dim_res' must be an integer but is has shape {type(dim_steps)}"
        # else:
        #     assert all(item in suiteValues for item in dims), \
        #         'All elements of dims must be a method the galpy orbit object: \n' + ', '.join(suiteValues)
        #     self.dims = dims
        #     # Check that dim_ranges and dim_res are the correct dimensions
        #     assert dim_ranges.shape == (len(dims), 2), \
        #         f"'dim_ranges' must have shape ({len(dims)}, 2) but it has shape {dim_ranges.shape}"
        #     assert dim_steps.shape == (len(dims),), \
        #         f"'dim_res' must have shape ({len(dims)},) but it has shape {dim_steps.shape}"
        
        # # ensure that the potential is a galpy potential object
        assert isinstance(pot, galpy.potential.Potential) or (isinstance(pot, list) and all(isinstance(item, galpy.potential.Potential) for item in pot)),\
            'potential must be a galpy potential or a list of galpy potentials'
    
        self.dim_res = dim_res
        self.kwargs = kwargs
        self.potential = pot

        
        self.integ_time = integ_time
        self.integ_kwargs = integ_kwargs
        self.init_kwargs = init_kwargs
        self.ts = np.linspace(integ_time['t_start'], integ_time['t_end'], integ_time['steps']) # integration timesteps

        if show_updates == True:
            print(f'Initializing orbits...')
        self.orbits = self._initialize() # intial conditions of the orbit, galpy orbit object
        
        if show_updates == True:
            print(f'Integrating orbits...')
        if auto_run == True:
            self._run()
        
    def _initialize(self):
        '''
        Initialize orbits

        Returns
        -------
        galpy.orbit.Orbit
            Orbit object with initial phase space positions of each orbit
        '''
        return _initializer(self.kwargs, self.dim_res, self.potential, **self.init_kwargs)
        
    def _run(self):
        '''
        Run the suite of orbits.
        '''
        self.orbits.integrate(self.ts, self.potential, **self.integ_kwargs)
        return None

    def rangeValue(self, value, orb_inds = None, time_inds = None):
        '''
        Calculate the change in a value of the orbits.
        Range of the value.

        Parameters
        ----------
        value : str
            String cooresponding to name of galpy orbit object method with 
            which to calculate the change in energy.
        orb_inds : list
            List of indices of the orbits to calculate the change in energy for.

        time_inds : list
            List of indices of the timesteps to calculate the change in energy for.
        '''

        if type(orb_inds) == type(None) and type(time_inds) == type(None):
            values = self.orbits._parse_plot_quantity(value)
        elif type(time_inds) == type(None):
            values = self.orbits._parse_plot_quantity(value)[orb_inds]
        elif type(orb_inds) == type(None):
            values = self.orbits._parse_plot_quantity(value)[:, time_inds]
        else:
            values = self.orbits._parse_plot_quantity(value)[orb_inds][:, time_inds]
        return np.ptp(values, axis=-1)
    
    def deltaValue(self, value, time_ind = -1, orb_inds = None):
        '''
        Calculate the change in a value of the orbits from the initial
        value to final value.
        final minus initial value.

        Parameters
        ----------
        value : str
            String cooresponding to name of galpy orbit object method with 
            which to calculate the change in energy.
        orb_inds : list
            List of indices of the orbits to calculate the change in energy for.
        time_inds : list
            time at which to calculate the value change.
        '''

        if type(orb_inds) == type(None):
            initial_value = self.orbits._parse_plot_quantity(value)[:, 0]
            final_value = self.orbits._parse_plot_quantity(value)[:, time_ind]
        else:
            intial_value = self.orbits._parse_plot_quantity(value)[orb_inds][:, 0]
            final_value = self.orbits._parse_plot_quantity(value)[orb_inds][:, time_ind]
        return final_value - initial_value

    
    def plot(self, 
             d1='R', 
             d2='vR', 
             color_by = 'E',
             orb_inds=None, 
             time_inds=None,
             style='line',
             **kwargs):
        """        
        Plotting routine for orbit suite.
        
        Parameters
        ----------
        d1 : str
            Quantity to plot on the x-axis.
        
        d2 : str
            Quantity to plot on the y-axis.
        
        color_by : str
            Quantity to color the orbits by. Default is 'E' for energy. The string should
            coorespond to a method of the galpy orbit object.

        orbit_inds : list
            List of indices of the orbits to plot.
        
        time_inds : list
            List of indices of the timesteps to plot.
        
        style : str
            Style of the plot. Options are 'line' or 'scatter'.
        
        **kwargs
            Additional keyword arguments to pass to the plotting function.
            
         """
        if 'c' in kwargs:
            warnings.warn('A color is provided yet color_by is not None. The color provided will be used.')
            color_by = None
        
        # obtain and index the quantities to plot
        if type(time_inds) == type(None) and type(orb_inds) == type(None):
            x = self.orbits._parse_plot_quantity(d1)
            y = self.orbits._parse_plot_quantity(d2)
        elif type(time_inds) == type(None):
            x = self.orbits._parse_plot_quantity(d1)[orb_inds]
            y = self.orbits._parse_plot_quantity(d2)[orb_inds]
        elif type(orb_inds) == type(None):
            x = self.orbits._parse_plot_quantity(d1)[:, time_inds]
            y = self.orbits._parse_plot_quantity(d2)[:, time_inds]
        else:
            x = self.orbits._parse_plot_quantity(d1)[orb_inds][:, time_inds]
            y = self.orbits._parse_plot_quantity(d2)[orb_inds][:, time_inds]

        if type(color_by) == type(None):
            if style == 'line':
                plot(x, y, **kwargs)
            elif style == 'scatter':
                scatter(x, y, **kwargs)
        else:
            if isinstance(color_by, str):
                try:
                    if type(orb_inds) == type(None) and type(time_inds) == type(None):
                        c = self.orbits._parse_plot_quantity(color_by)
                    elif type(time_inds) == type(None):
                        c = self.orbits._parse_plot_quantity(color_by)[orb_inds]
                    elif type(orb_inds) == type(None):
                        c = self.orbits._parse_plot_quantity(color_by)[:, time_inds]
                    else:
                        c = self.orbits._parse_plot_quantity(color_by)[orb_inds][:, time_inds]
                except:
                    # warnings.warn(f'Cannot color by {color_by}. Defaulting to black.')
                    c=c
            elif isinstance(color_by, np.ndarray):
                c = color_by.copy()
            
            if style == 'line':
                    plot(x, y, c=c, **kwargs)
            elif style == 'scatter':
                    scatter(x, y, c=c, **kwargs)
        
    
    # def plot3d(self):
    #     '''
    #     3D plotting routine for orbit suite.
    #     '''
    #     pass

    # def animate(self):
    #     '''
    #     Animation routine for orbit suite.
    #     '''
    #     pass

    # def interactive_plot(self):
    #     '''
    #     Interactive plot routine for orbit suite.
    #     '''
    #     pass

