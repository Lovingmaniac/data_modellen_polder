import matplotlib.pyplot as plt

def percipitation_unpaved():
    return 1.5

def percipitation_paved(t):
    if t < 1:
        return 0
    elif t >= 1 and t < 2: 
        return 60
    else:
        return 0

def percipitation_water(t):
    if t < 1:
        return 0
    elif t >= 1 and t < 2: 
        return 60
    else:
        return 0

def seepage():
    return -0.009

def evaporation_water():
    return 0.0

def evaporation_unpaved():
    return 0.208

def pump():
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
        h0 = h0 + (percipitation_unpaved() + percipitation_paved(t) + percipitation_water(t) + seepage() - evaporation_water() - evaporation_unpaved() - pump()) * dt
        h_list.append(round(h0,2))
        t_list.append(t)
        t += dt
    
    plt.plot(t_list,h_list)
    
    plt.show()

hoogte()
