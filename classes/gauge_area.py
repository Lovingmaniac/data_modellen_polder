class Gauge_area():
    def __init__(self,area_id, area, per_openwater, per_paved, per_unpaved):
        self.area_id = area_id
        self.area = area
        self.per_openwater = per_openwater
        self.per_paved = per_paved
        self.per_unpaved = per_unpaved

        self.neighbours = {}
        self.volume = None
        self.waterlevel = None
        self.discharge = None
        self.supply = None

    def add_neighbours(self, gauge_area):
        """Add neighbours to the gauge_area"""
        self.neighbours[gauge_area.area_id] = gauge_area
        
    def get_neighbours(self):
        """Returns all the neighbours of the gauge area"""
        return self.neighbours
    
    def remove_neighbour(self, gauge_area):
        """Remove neighbour from neighbours"""
        
        if gauge_area.area_id in self.neighbours.keys():
            self.neighbours.pop(gauge_area.area_id)

    def get_area_openwater(self):
        return (self.per_openwater / 100) * self.area
    
    def get_area_paved(self):
        return (self.per_paved/ 100) * self.area
    
    def get_area_unpaved(self):
        return (self.per_unpaved / 100) * self.area

    def set_waterlevel(self, waterlevel):
        self.waterlevel = waterlevel

    def set_discharge(self, discharge):
        self.discharge = discharge

    def set_supply(self, supply):
        self.supply = supply

    def set_volume(self, volume):
        self.volume = volume
        
    def __repr__(self):
        return f'(gauge_area_id: {self.area_id})'



#Test code
gauge_area_1 = Gauge_area(1, 20, 30, 50, 20) 
gauge_area_2 = Gauge_area(2, 20, 30, 50, 20)
gauge_area_3 = Gauge_area(3, 20, 30, 50, 20)

gauge_area_1.add_neighbours(gauge_area_2)
gauge_area_1.add_neighbours(gauge_area_3)

print(gauge_area_1.get_neighbours())

gauge_area_1.remove_neighbour(gauge_area_2)

print(gauge_area_1.get_neighbours())

print(f"open water: {gauge_area_1.get_area_openwater()}")
print(f"verhard: {gauge_area_1.get_area_paved()}")
print(f"onverhard: {gauge_area_1.get_area_unpaved()}")

gauge_area_1.set_waterlevel(5)
print(gauge_area_1.waterlevel)