import matplotlib.pyplot as plt

def percipitation_unpaved():
    """
    water that will flow through the unpaved surface
    In: 
    OUT: 
    Unit: mm/hr
    """
    return 1.5

def percipitation_paved(area_ha, percipitation, t):
    """
    Water that will flow over the paved surface into the open water area
    In:
    Out: 
    Unit: mm/hr
    """
    area_m2 = area_ha * 10000 #m²
    percipitation_mhr = percipitation / 1000 #m/hr
    
    if t < 1:
        return 0
    elif t >= 1 and t < 2: 
        return area_m2 * percipitation_mhr #m³/hr
    else:
        return 0

def percipitation_water(t):
    """
    Percipitation that will land directly in the open water
    IN:
    OUT:
    Unit: mm/hr
    """
    
    if t < 1:
        return 0
    elif t >= 1 and t < 2: 
        return 60
    else:
        return 0

def seepage():
    """
    Seepage into the system
    Negative --> outgoing
    Positive --> incoming
    Unit: mm/hr
    """
    return -0.009

def evaporation_water():
    """
    Evaporation over the surface of the water
    Unit: mm/hr
    """

    return 0.0

def evaporation_unpaved():
    """
    Evaporation over the unpaved surface
    Unit: m/hr
    """
    return 0.208

def pump():
    """
    The amount of water that gets pumped out
    Unit: mm/hr
    """
    return 5

def hoogte():
    
    t = 0
    dt = 0.1
    h0 = 0
    t_eind = 24
    
    t_list = []
    h_list = []
    

    while t < t_eind:
        # breakpoint()
        h0 = h0 + (percipitation_unpaved() + percipitation_paved(area_ha, percipitation, t) + percipitation_water(t) + seepage() - evaporation_water() - evaporation_unpaved() - pump()) * dt
        h_list.append(round(h0,2))
        t_list.append(t)
        t += dt
    
    plt.plot(t_list,h_list)
    
    plt.show()

hoogte()
