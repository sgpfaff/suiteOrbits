from galpy.orbit import Orbit

suiteValues = ['r_apo', 'start_time'] # values which you can probe in the suite

orbitMethods = [method for method in dir(Orbit) if callable(getattr(Orbit, method)) and not method.startswith("__")] # values which you can use to analyze the results