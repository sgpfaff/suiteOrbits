'Functions to initialize the particles in the suite'
import numpy as np
from galpy.orbit import Orbit
import astropy.units as u

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

    r_apo_ind_list = [np.argmin(np.abs(potential(r_list, 0) + (0.5 * Lz**2 / r_list**2) - _E)) for _E in E_list] # list of r_list indices associated with apocenter of orbit of each E and given Lz.
    r = r_list[r_apo_ind_list]
    vT = Lz / r
    return Orbit([[r[i], 0, vT[i], 0, 0, 0] for i in range(0, len(E_list))]) # [R,vR,vT(,z,vz,phi)]


    