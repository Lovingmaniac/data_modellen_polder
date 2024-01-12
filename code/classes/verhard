from gauge_area import Gauge_area

# function for the waterflow out of the paved area
def supply(Q, precipitation, t):
    waterlevel = precipitation - Q * t / gauge_area.area
    #gauge_area.supply = waterlevel + gauge_area.waterlevel
    return waterlevel

# empty lists
time_list = []
total_water = []

# defining parameters
Q = 1                   #m3/hr
precipitation = 0.12    #m/hr
t = 0                   #hr
eind_tijd = 10
gauge_area = Gauge_area(1, 20, 0, 100, 0)
gauge_area.set_waterlevel(0)

# waterflow on the paved system
while t <= eind_tijd:
    time_list.append(t)
    Qf = supply(Q, precipitation, t)
    total_water.append(Qf)
    if Qf <= 0:
        Qf = 0
        break
    print(round(Qf,3))
    t += 1