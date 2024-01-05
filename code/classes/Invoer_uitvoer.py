from gauge_area import Gauge_area

# function for the waterflow in and out of the system
def supply(Q, precipitation, seepage, influent_seepage, t):
    flow = precipitation + seepage - influent_seepage + (Q / gauge_area.area)
    gauge_area.supply = flow * t + gauge_area.waterlevel
    return gauge_area.supply

# empty lists
time_list = []
total_water = []

# defining parameters
Q = 2
precipitation = 0.1
influent_seepage = 0.03
seepage = 0.02
t = 0
eind_tijd = 10
gauge_area = Gauge_area(1, 20, 30, 10, 60)
gauge_area.set_waterlevel(1)

# taking waterflow in the system
while t <= eind_tijd:
    time_list.append(t)
    Qf = supply(Q, precipitation, seepage, influent_seepage, t)
    total_water.append(Qf)
    print(round(Qf,2))
    t += 1

