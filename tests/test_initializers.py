   
def test_initializers():
    from suiteorbits import initializers as init
    from galpy.potential import NFWPotential
    import numpy as np

    n_orbits = 10

    ### varyE_fixLz()
    pot = NFWPotential()
    E_range = [-0.3, -0.2]
    E_list = np.linspace(E_range[0], E_range[1], n_orbits)
    Lz = pot.LcE(E_list[0])
    o = init.varyE_fixLz(E_range, n_orbits, Lz, pot) # initialize particles
    assert o.shape == (n_orbits, ), \
        f"orbit has shape {o.shape} but should have shape ({n_orbits}, )"
    assert np.all(np.abs(o.E(pot=pot) - np.linspace(E_range[0], E_range[1], n_orbits)) < 1e-5) == True, \
        f"Orbit energies are not of the orbit object are not as expected.\nThe predicted energies are off by {np.sum(o.E(pot=pot) - np.linspace(E_range[0], E_range[1], n_orbits))} in total.\n Try using a high resolution, r_res."
    assert np.all(np.abs(o.Lz() - Lz) < 1e-10) == True, \
        f"Orbit Lz values are not as expected.\nThe predicted Lz values are off by {np.sum(o.Lz(pot=pot) - Lz)} in total."
    assert np.all(np.abs(o.vr() < 1e-10)) == True, \
        f"Initial radial velocities of initialized particles are non-zero. Particles should be initialized at apocenter. \nThe predicted vr values are off by {np.sum(o.vr())} in total."
    
    
    