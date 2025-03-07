from abc import ABC, abstractmethod
import numpy as np
from ..constants import orbitMethods, suiteValues

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



class Suite():
    '''
    Suite class for exploring n parameters.
    '''
    def __init__(self, dims, dim_ranges, dim_steps, **kwargs):
        '''
        Parameters:
        ----------
        dims: str or ndarray of str
            dimensions to probe in the suite

        dim_ranges : ndarray
            ranges of values to probe along each dimension

        dim_steps : ndarray
            number of orbits to explore for each dimension
        '''
        if type(dims) == str:
            self.dims = dims
        else:
            assert all(item in suiteValues for item in dims), \
                'All elements of dims must be a method the galpy orbit object: \n' + ', '.join(suiteValues)
            self.dims = dims
        
        # Check that dim_ranges and dim_res are the correct dimensions
        assert dim_ranges.shape == (len(dims), 2), \
            f"'dim_ranges' must have shape ({len(dims)}, 2) but it has shape {dim_ranges.shape}"
        assert dim_steps.shape == (len(dims),), \
            f"'dim_res' must have shape ({len(dims)},) but it has shape {dim_steps.shape}"
        
        self.dim_ranges = dim_ranges
        self.dim_res = dim_steps
    

    def _initialize(self):
        '''
        Initialize orbits
        '''
        pass