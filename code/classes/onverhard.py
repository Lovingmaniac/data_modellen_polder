#x mm blokbui
P40 = []
P60 = [0,0,0,0.06,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
P80 = []
P100 = []

#Verdamping zomer en winter
Ez = [0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0]
Ew = [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0]


def groundwater_ts(neerslag, verdamping, doorlatendheid, simulatieduur, hg0):
    import matplotlib.pyplot as plt
    #create lists
    t_list = []
    hg_list = []

    #assign values to variables 
    S = simulatieduur
    hg = hg0
    k = doorlatendheidpip
    
    #start list with values for t=0
    t_list.append(0)
    hg_list.append(hg0)

    #for loop to go through 
    for i in list(range(1, S, 1)):
        
        P = neerslag[i-1]
        E = verdamping[i-1] 

        t = i
        hg = hg + P/1000 - E/1000 * k

        t_list.append(t)
        hg_list.append(hg)
    
    plot = plt.plot(t_list, hg_list)
        
    return t_list, hg_list, plot

t, hg, plot = groundwater_ts(neerslag=P60, verdamping=Ew, doorlatendheid=1, simulatieduur=24, hg0=-1)


# In[ ]:


# x mm blokbui
P40 = 40
P60 = 60
P80 = 80
P100 = 100

#Verdamping zomer en winter
Ez = 3
Ew = 1

def groundwater_lv(neerslag, verdamping, doorlatendheid, begin_waterstand, afstand_waterwegen, afstand_ondoorlatendelaag):
    import matplotlib.pyplot as plt
    
    #create lists for time, waterlevel 2x and bulge groundwater
    hg_list = []

    #assign values to variables 
    h1 = begin_waterstand
    hg = begin_waterstand
    h2 = begin_waterstand
    k = doorlatendheid
    P = neerslag
    E = verdamping
    L = afstand_waterwegen
    D = afstand_ondoorlatendelaag
    
    #calculation groundwater Hooghoudt
    h = ((P/1000 - E/1000) * L ** 2) / (8 * k * D)

    h1 = h1 * -1
    h2 = h2 * -1
    hg = hg - h

    hg_list.append(h1)
    hg_list.append(hg)
    hg_list.append(h2)

    plot = plt.plot(hg_list)
        
    return hg_list, plot

t, hg, plot = groundwater_lv(neerslag=P60, verdamping=Ew, doorlatendheid=0.8, begin_waterstand=1, afstand_waterwegen=10, afstand_ondoorlatendelaag=5)