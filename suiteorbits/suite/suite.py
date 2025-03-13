from abc import ABC, abstractmethod
import numpy as np
from ..constants import orbitMethods, suiteValues
from .initializers import _initializer
from ..plot import plot, scatter
import galpy
import warnings


# class AbstractSuite(ABC):
#     def __init__(self, dims, dim_ranges, dim_steps, **kwargs):
#         '''
#         Parameters:
#         ----------
#         dims: str or ndarray of str
#             dimensions to probe in the suite

#         dim_ranges : ndarray
#             ranges of values to probe along each dimension

#         dim_steps : ndarray
#             number of orbits to explore for each dimension
#         '''
#         super().__init__( **kwargs)
#         if type(dims) == str:
#             self.dims = dims
#         else:
#             assert all(item in suiteValues for item in dims), \
#                 'All elements of dims must be a method the galpy orbit object: \n' + ', '.join(suiteValues)
#             self.dims = dims
        
#         # Check that dim_ranges and dim_res are the correct dimensions
#         assert dim_ranges.shape == (len(dims), 2), \
#             f"'dim_ranges' must have shape ({len(dims)}, 2) but it has shape {dim_ranges.shape}"
#         assert dim_steps.shape == (len(dims),), \
#             f"'dim_res' must have shape ({len(dims)},) but it has shape {dim_steps.shape}"
        
#         self.dim_ranges = dim_ranges
#         self.dim_res = dim_steps

#     @abstractmethod
#     def _initialize(self):
#         pass


# class Suite1D(AbstractSuite):
#     '''
#     Suite class for exploring 1 parameter.
#     '''
#     def __init__(self, dims, dim_ranges, dim_steps, **kwargs):
#         '''
#         Parameters:
#         ----------
#         dims: str or ndarray of str
#             dimensions to probe in the suite

#         dim_ranges : ndarray
#             ranges of values to probe along each dimension

#         dim_steps : ndarray
#             number of orbits to explore for each dimension
#         '''
#         super().__init__(dims, dim_ranges, dim_steps, **kwargs)

#         assert dims.shape == (1,), \
#             f"'dims' must have shape (1,) but it has shape {dims.shape}"
#         self.dims = dims
#         self.dim_ranges = dim_ranges
#         self.dim_steps = dim_steps
    

#     def _initialize(self):
#         '''
#         Initialize orbits

#         *** 
#         add feature to vary where along the orbit the orbit starts. 
#         For now, we'll just assume it starts at apocenter.
#         ***
#         '''
#         pass

#     def run(self):
#         '''
#         Run the suite

#         Returns
#         -------
#         galpy.orbit.Orbit
#             Orbit object with the results of the suite
#         '''
#         pass


# class Suite2D(AbstractSuite):
#     '''
#     Suite class for exploring 2 parameters.
#     '''
#     def __init__(self, dims, dim_ranges, dim_steps, **kwargs):
#         '''
#         Parameters:
#         ----------
#         dims: str or ndarray of str
#             dimensions to probe in the suite

#         dim_ranges : ndarray
#             ranges of values to probe along each dimension

#         dim_steps : ndarray
#             number of orbits to explore for each dimension
#         '''
#         super().__init__(dims, dim_ranges, dim_steps, **kwargs)

#         assert dims.shape == (2,), \
#             f"'dims' must have shape (2,) but it has shape {dims.shape}"
    

#     def _initialize(self):
#         '''
#         Initialize orbits
#         '''
#         pass



# class Suite():
#     '''
#     Suite class for exploring n parameters.
#     '''
#     def __init__(self, 
#                  dims, 
#                  dim_ranges, 
#                  dim_steps, 
#                  potential, 
#                  integ_time={'t_start':0, 't_end':10, 'steps':10000}, 
#                  integ_kwargs={},
#                  init_kwargs={}, 
#                  show_updates = True,
#                  auto_run = True,
#                  **kwargs):
#         '''
#         Parameters:
#         ----------
#         dims: str or ndarray of str
#             dimensions to probe in the suite

#         dim_ranges : ndarray
#             ranges of values to probe along each dimension

#         dim_steps : ndarray
#             number of orbits to explore for each dimension

#         potential : galpy.potential.Potential
#             The galpy potential object to use for the suite.

#         integ_time : dict
#             Dictionary with the start, end, and number of timesteps for the integration.

#         integ_kwargs : dict
#             Keyword arguments to pass to the integration function.

#         init_kwargs : dict
#             Additional keyword arguments to pass to the initializer function.
        
#         show_updates : bool
#             Print updates to the console.
        
#         auto_run : bool
#             Automatically run the suite after initialization, using the potential used to make the particles.
#             Can bypass this feature by setting auto_run=False and integrating the suite manually with .integrate().
#         '''
#         if type(dims) == str:
#             self.dims = dims
#             # Check that dim_ranges and dim_res are the correct dimensions
#             assert dim_ranges.shape == (2,), \
#                 f"'dim_ranges' must have shape (2,) but it has shape {dim_ranges.shape}"
#             assert isinstance(dim_steps, int), \
#                 f"'dim_res' must be an integer but is has shape {type(dim_steps)}"
#         else:
#             assert all(item in suiteValues for item in dims), \
#                 'All elements of dims must be a method the galpy orbit object: \n' + ', '.join(suiteValues)
#             self.dims = dims
#             # Check that dim_ranges and dim_res are the correct dimensions
#             assert dim_ranges.shape == (len(dims), 2), \
#                 f"'dim_ranges' must have shape ({len(dims)}, 2) but it has shape {dim_ranges.shape}"
#             assert dim_steps.shape == (len(dims),), \
#                 f"'dim_res' must have shape ({len(dims)},) but it has shape {dim_steps.shape}"
        
#         # ensure that the potential is a galpy potential object
#         assert isinstance(potential, galpy.potential.Potential) or (isinstance(potential, list) and all(isinstance(item, galpy.potential.Potential) for item in potential)),\
#             'potential must be a galpy potential or a list of galpy potentials'
        
#         self.potential = potential
#         self.dim_ranges = dim_ranges
#         self.dim_res = dim_steps
#         self.integ_time = integ_time
#         self.integ_kwargs = integ_kwargs
#         self.init_kwargs = init_kwargs
#         self.ts = np.linspace(integ_time['t_start'], integ_time['t_end'], integ_time['steps']) # integration timesteps
#         self.kwargs = kwargs
#         print(self.kwargs)

#         if show_updates == True:
#             print(f'Initializing orbits...')
#         self.orbits = self._initialize() # intial conditions of the orbit, galpy orbit object
        
#         if show_updates == True:
#             print(f'Integrating orbits...')
#         if auto_run == True:
#             self._run()
        
#     def _initialize(self):
#         '''
#         Initialize orbits

#         Returns
#         -------
#         galpy.orbit.Orbit
#             Orbit object with initial phase space positions of each orbit
#         '''
#         # if self.dims == 'E' and 'Lz' in self.kwargs:
#         #     # ADD: warn user if the potential is not spherically symmetric.
#         #     return varyE_fixLz(self.dim_ranges, self.dim_res, self.kwargs['Lz'], self.potential, **self.init_kwargs)

#         return _initializer(self.dims, self.dim_ranges, self.dim_res, self.potential, **self.init_kwargs)
        
#     def _run(self):
#         '''
#         Run the suite

#         Returns
#         -------
#         None
#             Updates orbit internally
#         '''
#         self.orbits.integrate(self.ts, self.potential, **self.integ_kwargs)
#         return None
    
#     def plot(self, 
#              d1='R', 
#              d2='vR', 
#              color_by = 'E',
#              orb_inds=None, 
#              time_inds=None,
#              style='line',
#              **kwargs):
#         x = self.orbits._parse_plot_quantity(d1)[orb_inds][:, time_inds]
#         y = self.orbits._parse_plot_quantity(d2)[orb_inds][:, time_inds]

#         if color_by == None:
#             if style == 'line':
#                 plot(x, y, **kwargs)
#             elif style == 'scatter':
#                 scatter(x, y, **kwargs)
#         else:
#             if isinstance(color_by, str):
#                 try:
#                     c = self.orbits._parse_plot_quantity(color_by)[orb_inds][:, time_inds]
#                 except:
#                     # warnings.warn(f'Cannot color by {color_by}. Defaulting to black.')
#                     c=c
#             elif isinstance(color_by, np.ndarray):
#                 c = color_by.copy()
            
#             if style == 'line':
#                     plot(x, y, c=c, **kwargs)
#             elif style == 'scatter':
#                     scatter(x, y, c=c, **kwargs)
        
    
#     def plot3d(self):
#         pass

#     def animate(self):
#         pass

#     def interactive_plot(self):
#         pass

class Suite():
    '''
    Suite class for exploring n parameters.
    '''
    def __init__(self,
                 dim_res=100, 
                 pot=None, 
                 integ_time={'t_start':0, 't_end':10, 'steps':10000}, 
                 integ_kwargs={},
                 init_kwargs={}, 
                 show_updates = True,
                 auto_run = True,
                 **kwargs
                 ):
        '''
        Parameters:
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
        # assert isinstance(potential, galpy.potential.Potential) or (isinstance(potential, list) and all(isinstance(item, galpy.potential.Potential) for item in potential)),\
        #     'potential must be a galpy potential or a list of galpy potentials'
        #print(*kwargs)
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
        #if self.
        # if self.dims == 'E' and 'Lz' in self.kwargs:
        #     # ADD: warn user if the potential is not spherically symmetric.
        #     return varyE_fixLz(self.dim_ranges, self.dim_res, self.kwargs['Lz'], self.potential, **self.init_kwargs)
        return _initializer(self.kwargs, self.dim_res, self.potential, **self.init_kwargs)
        
    def _run(self):
        '''
        Run the suite

        Returns
        -------
        None
            Updates orbit internally
        '''
        self.orbits.integrate(self.ts, self.potential, **self.integ_kwargs)
        return None
    
    def plot(self, 
             d1='R', 
             d2='vR', 
             color_by = 'E',
             orb_inds=None, 
             time_inds=None,
             style='line',
             **kwargs):
        x = self.orbits._parse_plot_quantity(d1)[orb_inds][:, time_inds]
        y = self.orbits._parse_plot_quantity(d2)[orb_inds][:, time_inds]

        if color_by == None:
            if style == 'line':
                plot(x, y, **kwargs)
            elif style == 'scatter':
                scatter(x, y, **kwargs)
        else:
            if isinstance(color_by, str):
                try:
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
        
    
    def plot3d(self):
        pass

    def animate(self):
        pass

    def interactive_plot(self):
        pass

