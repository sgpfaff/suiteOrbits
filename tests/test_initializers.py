   
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
    

def test_suite():
    import suiteorbits as so
    from suiteorbits import initializers as init
    import galpy
    from galpy.potential import NFWPotential
    import numpy as np
    pot = NFWPotential()
    n_orbits = 10
    E_range = np.array([-0.3, -0.2])
    E_list = np.linspace(E_range[0], E_range[1], n_orbits)
    Lz = pot.LcE(E_list[0])
    o_direct = init.varyE_fixLz(E_range, n_orbits, Lz, pot) # initialized directly from initializer
    suite = so.Suite('E', E_range, n_orbits, pot, Lz=Lz)

    assert isinstance(suite.orbits, galpy.orbit.Orbit), \
        f"Suite.orbits is not a galpy Orbit object but is {type(suite.orbits)}"
    assert suite.orbits.shape == (n_orbits, ), \
        f"Suite.orbits has shape {suite.orbits.shape} but should have shape ({n_orbits}, )"
    assert np.all(np.abs(suite.orbits.E(pot=pot) - E_list < 1e-6)) == True, \
        f"Suite.orbits energies are not as expected.\nThe predicted energies are off by {np.sum(suite.orbits.E(pot=pot) - E_list)} in total."
    assert np.all(np.abs(suite.orbits.Lz(pot=pot) - Lz) < 1e-10) == True, \
        f"Suite.orbits Lz values are not as expected.\nThe predicted Lz values are off by {np.sum(suite.orbits.Lz(pot=pot) - Lz)} in total."
    assert np.all(np.abs(suite.orbits.E(pot=pot) - o_direct.E(pot=pot) < 1e-10)) == True, \
        f"Suite.orbits disagrees with direct implementation of initializer."
    
    

    
    