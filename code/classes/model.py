import matplotlib.pyplot as plt

def p_o():
    return 1.5

def p_v(t):
    if t < 1:
        return 0
    elif t >= 1 and t < 2: 
        return 60
    else:
        return 0

def p_w(t):
    if t < 1:
        return 0
    elif t >= 1 and t < 2: 
        return 60
    else:
        return 0

def s():
    return -0.009

def e_w():
    return 0.0

def e_o():
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
        h0 = h0 + (p_o() + p_v(t) + p_w(t) + s() - e_w() - e_o() - pump()) * dt
        h_list.append(round(h0,2))
        t_list.append(t)
        t += dt
    
    plt.plot(t_list,h_list)
    
    plt.show()
    
    print(t_list)
    print(h_list)

    return h_list, t_list

hoogte()
