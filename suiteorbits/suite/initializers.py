'Functions to initialize the particles in the suite'
import numpy as np
from ..utils import eval_potential
from galpy.orbit import Orbit
import astropy.units as u

def _initializer(dims, dim_res, potential, **kwargs):
    '''Find and apply the initializer based on the provided quantities.
    
    Parameters:
    ----------
    dims : dict
        Dictionary of dimensions (keys) and their ranges (values).
    '''
    if 'E' in dims and 'Lz' in dims:
            # ADD: warn user if the potential is not spherically symmetric.
            if isinstance(dims['E'], list) and isinstance(dims['Lz'], float):
                return varyE_fixLz(dims['E'], dim_res, dims['Lz'], potential, **kwargs)
            elif isinstance(dims['E'], float) and isinstance(dims['Lz'], list):
                 assert False, 'Building suites of orbits with the same energy and different angular momentum is not yet supported.'
            elif isinstance(dims['E'], list) and isinstance(dims['Lz'], list):
                assert False, 'Building 2D suites of orbits with varying energy and angular momentum is not yet supported.'
            else:
                assert False, 'E and Lz should be either lists or floats.'
            
    
def varyE_fixLz(E_range, E_res, Lz, potential, _res=int(1e6), r_range=[0.01, 50], **kwargs):
    '''
    Initialize n particles with varying energy and the same angular momentum.
    
    Parameters:
    ----------
    E_range : ndarray
        Range of energies to explore, in units of km^2/s^2.
    E_res : int
        Resolution of the energy list.
    Lz : float
        Angular momentum of the energies, in units of kpc km/s
    potential : galpy.potential.Potential
        The galpy potential object to use.
    _res : int
        Resolution of the radius and energy list. Default is 1e4.
    **kwargs : dict
        Additional keyword arguments to pass to the Orbit object.
    
    Returns:
    -------
    Orbit
        An Orbit object with n particles initialized at apocenter with varying energy and the same angular momentum.

    Notes:
    -----
    Particles are initialized at apocenter (v_r = 0) and tangential velocity in only one direction.
    Assumes a spherically symmetric potential.

    Needed:
    ------
    * Add way to automate the resolution of the radius and energy lists.
    * Add way to automate the radius range, resolution, and scaling.
    * Add way to automate the energy resolution and scaling.

    '''
    r_list = np.linspace(r_range[0], r_range[1], _res) # list of radii at which the potential is calculated
    E_list = np.linspace(E_range[0], E_range[1], E_res) # list of energies to explore

    r_apo_ind_list = [np.argmin(np.abs(eval_potential(potential, r_list, 0) + (0.5 * Lz**2 / r_list**2) - _E)) for _E in E_list] # list of r_list indices associated with apocenter of orbit of each E and given Lz.
    r = r_list[r_apo_ind_list]
    vT = Lz / r
    return Orbit([[r[i], 0, vT[i], 0, 0, 0] for i in range(0, len(E_list))]) # [R,vR,vT(,z,vz,phi)]


def general():
    '''General initialization for any provided quantities.'''