def eval_potential(pot, *args, **kwargs):
    '''evaluate the potential or list of potentials'''
    if isinstance(pot, list):
        return sum([p(*args, **kwargs) for p in pot])
    else:
        return pot(*args, **kwargs)