import matplotlib.pyplot as plt

def percipitation_unpaved():
    """
    water that will flow through the unpaved surface
    In: 
    OUT: 
    Unit: mm/hr
    """
    return 1.5

def percipitation_paved(area_ha_paved, percipitation, t):
    """
    Water that will flow over the paved surface into the open water area
    In:
    Out: 
    Unit: m³/hr
    """
    area_m2 = area_ha_paved * 10000 #m²
    percipitation_mhr = percipitation / 1000 #m/hr

    if t < 1:
        return 0
    elif t >= 1 and t < 2: 
        return area_m2 * percipitation_mhr #m³/hr
    else:
        return 0

def percipitation_water(area_ha_water, percipitation, t):
    """
    Percipitation that will land directly in the open water
    IN:
    OUT:
    Unit: mm/hr
    """
    area_m2 = area_ha_water * 10000 #m²
    percipitation_mhr = percipitation / 1000 #m/hr

    if t < 1:
        return 0
    elif t >= 1 and t < 2: 
        return area_m2 * percipitation_mhr #m³/hr
    else:
        return 0

def seepage(area, seepage):
    """
    Seepage into the system
    Negative --> outgoing
    Positive --> incoming
    Unit: mm/hr
    """
    seepage_mhr = seepage / 1000 / 24
    area_m2 = area * 10000
    return seepage_mhr * area_m2

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

def pump(pumpcapacity):
    """
    The amount of water that gets pumped out
    Unit: m³/hr
    """
    pumpcapacity_hr = pumpcapacity * 60
    
    return pumpcapacity_hr

def hoogte():
    
    t = 0
    dt = 0.1
    volume_0 = 0
    t_eind = 24
    
    t_list = []
    h_list = []
    

    while t < t_eind:
        # breakpoint()
        volume_0 = volume_0 + (percipitation_unpaved() + percipitation_paved(area_ha, percipitation, t) + percipitation_water(t) + seepage() - evaporation_water() - evaporation_unpaved() - pump(pumpcapacity)) * dt
        h_list.append(round(volume_0,2))
        t_list.append(t)
        t += dt
    
    plt.plot(t_list,h_list)
    
    plt.show()

hoogte()
