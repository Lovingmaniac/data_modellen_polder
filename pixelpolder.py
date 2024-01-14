import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout = 'wide')

#Defenition that contains all the necessary information for page 1
def page_one():
    st.title("DE PIXELPOLDER")
    st.write()
    st.write("Welkom bij de interactieve poldersimulatie! Laat je het regenen met pijpenstelen of zonnestralen?")
    st.write("Pas de parameters op pagina 2 aan en bekijk wat het effect is op de waterstanden in de polder.")

#Defenition that contains all the necessary information for page 2
def page_two():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Parameters")
        st.write("Vul onderstaande parameters in om een polder na te bootsen.")
        st.write()

        global soil
        soil = st.selectbox('Selecteer de grondsoort', ("Zand", "Klei", "Veen"))

        global precipitation
        precipitation = st.selectbox('Selecteerd het aantal mm neerslag', ("40mm", "60mm", "80mm", "100mm"))

        global season
        season = st.selectbox('Selecteer een seizoen voor de verdamping', ("Lente", "Zomer", "Herfst", "Winter"))

        global area
        area = st.slider("Oppervlakte polder in ha", 50, 20000, value = 8000)

        global percentage_paved, percentage_unpaved, percentage_water
        percentage_paved = st.slider('Percentage verhard oppervlakte: ', 0, 97, value= 30)
        percentage_unpaved = st.slider('Percentage onverhard oppervlakte: ', 1, 99-percentage_paved)
        percentage_water = 100 - percentage_paved - percentage_unpaved
        st.write(f'Verhoudingen polder: verhard= {percentage_paved}') 
        st.write(f'onverhard= {percentage_unpaved} openwater= {percentage_water}')

        global pumpcapacity
        pumpcapacity = st.slider('Geef de pompcapaciteit in m³/min', 0, 3000, value= 500)

        global seepage
        seepage = st.slider("Wat is de kwel (positief) of wegzijging (negatief) in mm/dag", min_value=-5, max_value=5, value= 0)


    def rainfall_selection():
        if precipitation == '40mm':
            return 40
        elif precipitation == '60mm':
            return 60
        elif precipitation == '80mm':
            return 80
        elif precipitation == '100mm':
            return 100

    def season_selection():
        if season == 'Lente':
            return 0.083
        elif season == 'Zomer':
            return 0.124
        elif season == 'Herfst':
            return 0.033
        elif season == 'Winter':
            return 0.013
        
    #Create model for groundlevel
    def mv(L, slope, depth, width, groundlevel):

        #Point on the x-axis for groundlevel
        xa = 0
        xb = xa + slope * depth
        xc = xb + width
        xd = xc + slope * depth
        xe = xd + L
        xf = xe + slope * depth
        xg = xf + width
        global xh
        xh = xg + slope * depth

        #Points on the y-axis for groundlevel
        ya = groundlevel
        yb = ya - depth
        yc = yb
        yd = yc + depth
        ye = yd
        yf = ye - depth
        yg = yf
        yh = yg + depth

        #Create lists of the points for groundlevel
        global mvx
        global mvy
        mvx = [xa,xb,xc,xd,xe,xf,xg,xh]
        mvy = [ya,yb,yc,yd,ye,yf,yg,yh]
        
    mv(100, 3, 0.5, 2, 0)

    #Create model for groundwaterlevel
    def groundwater(precipitation, season, soil, start_waterlevel, distance_waterways, simulation_duration):
        
        P = [(rainfall_selection()/1000)] + [(0/1000)] * (simulation_duration-1)
        E = [(season_selection()/1000)] * simulation_duration     
        
        #Soil selection
        if soil == 'Zand':
            k = 5
        elif soil == 'Klei':
            k = 0.5
        elif soil == 'Veen':
            k = 0.01
            
        #Define other start valuables
        h = start_waterlevel
        hg = start_waterlevel
        L = distance_waterways
        
        #Create empty lists to fill with resultst with a for-loop
        global hgl
        global t
        hgl = []
        t = []
        
        #Assign startvalues to lists
        hgl.append(hg)
        t.append(0)
        
        #For loop to calculate the groundwaterlevel every hour after the specified amount of rainfall
        for hour in range(0, simulation_duration):
            #If the waterlevel is below the groundwaterlevel, water will move from the groundwater to the surfacewater at speed q
            if h - hg < 0:
                i = abs(h - hg) / (0.5 * L)
                Q = (k * i) * 3600 * abs(h-hg) * 2
                hg = hg + P[hour]/1000 - E[hour]/1000 - Q/L
            
            #If the groundwaterlevel is below the waterlevel, water will move from the groundwater to the surfacewater at speed q
            elif h - hg > 0:
                i = abs(h - hg) / (0.5 * L)
                Q = (k * i) * 3600 * abs(h-hg) * 2
                hg = hg + P[hour]/1000 - E[hour]/1000 + Q/L
            
            #If the groundwaterlevel and the waterlevel are equal, no water will move between the waterstorages
            else:
                hg = hg + P[hour]/1000 - E[hour]/1000
            
            #The time is the amount of hours after startingpoint
            time = hour + 1
            
            #Add the new groundwaterlevel for each hour in the simulation
            hgl.append(hg)
            t.append(time)

    simulation_duration = 744
    groundwater(precipitation=precipitation, season=season, soil=soil, start_waterlevel=-0.25, distance_waterways=20, simulation_duration= simulation_duration)

    

    #Create model for visualisation
    def visualise():
        import plotly.graph_objects as go
        import pandas as pd

        #Code to calculate the intersections between the groundlevel and groundwaterlevel
        mv_df = pd.DataFrame({'x':mvx, 'y':mvy})

        #Intersection 1
        a1 = (mv_df.y[1] - mv_df.y[0]) / (mv_df.x[1] - mv_df.x[0])
        b1 = mv_df.y[1] - a1 * mv_df.x[1]
        int1 = (hgl[time] - b1) / a1

        #Intersection 2
        a2 = (mv_df.y[3] - mv_df.y[2]) / (mv_df.x[3] - mv_df.x[2])
        b2 = mv_df.y[3] - a2 * mv_df.x[3]
        int2 = (hgl[time] - b2) / a2

        #Intersection 3
        a3 = (mv_df.y[5] - mv_df.y[4]) / (mv_df.x[5] - mv_df.x[4])
        b3 = mv_df.y[5] - a3 * mv_df.x[5]
        int3 = (hgl[time] - b3) / a3

        #Intersection 4
        a4 = (mv_df.y[7] - mv_df.y[6]) / (mv_df.x[7] - mv_df.x[6])
        b4 = mv_df.y[7] - a4 * mv_df.x[7]
        int4 = (hgl[time] - b4) / a4

        mv_df = pd.DataFrame({'x':mvx, 'y':mvy}) 

        fig = go.Figure(
            layout = {
                'showlegend': False,
                'xaxis': {
                    'range': [0, xh],
                    'showgrid': False,
                    'zeroline': False, 
                    'visible': False
                }
            }
        )

        fig.add_trace(go.Scatter(
            x=mv_df.x, 
            y=mv_df.y, 
            mode='lines', 
            marker = {'color' : 'green'}))
        fig.add_trace(go.Scatter(
            x=[0, int1], 
            y=[hgl[time], hgl[time]], 
            mode='lines', 
            marker = {'color' : 'skyblue'}))
        fig.add_trace(go.Scatter(
            x=[int2, int3], 
            y=[hgl[time], hgl[time]], 
            mode='lines', 
            marker = {'color' : 'skyblue'}))
        fig.add_trace(go.Scatter(
            x=[int4, xh], 
            y=[hgl[time], hgl[time]], 
            mode='lines', 
            marker = {'color' : 'skyblue'}))

        st.write(fig)
        st.write(hgl[time])
        # st.write(hgl)
    


    def model(): 
        def precipitation_unpaved():
            """
            water that will flow through the unpaved surface
            In: 
            OUT: 
            Unit: m³/hr
            """
            area_ha_unpaved = area * (percentage_unpaved/100)
            volume_l = 1.5 * 3600 * area_ha_unpaved
            return volume_l/1000

        def precipitation_paved(t):
            """
            Water that will flow over the paved surface into the open water area
            In:
            Out: 
            Unit: m³/hr
            """

            area_m2 = area * 10000 #m²
            area_m2_paved = area_m2 * (percentage_paved/100)
            precipitation_mhr = rainfall_selection() / 1000 #m/hr

            if t < 1:
                return 0
            elif t >= 1 and t < 2: 
                return area_m2_paved * precipitation_mhr #m³/hr
            else:
                return 0

        def precipitation_water(t):
            """
            Precipitation that will land directly in the open water
            IN:
            OUT:
            Unit: m³/hr
            """
            area_m2 = area * 10000 #m²
            area_m2_water = area_m2 * (percentage_water / 100)
            precipitation_mhr = rainfall_selection() / 1000 #m/hr

            if t < 1:
                return 0
            elif t >= 1 and t < 2: 
                return area_m2_water * precipitation_mhr #m³/hr
            else:
                return 0

        def seepage_in():
            """
            Seepage into the system
            Negative --> outgoing
            Positive --> incoming
            Unit: m³/hr
            """
            seepage_mhr = seepage / 1000 / 24
            area_m2 = area * 10000
            return seepage_mhr * area_m2

        def evaporation_water():
            """
            Evaporation over the surface of the water
            Unit: m³/hr
            """
            
            evaporation = season_selection() #mm/hr
            area_m2 = area * 10000
            area_water_m2 = area_m2 * (percentage_water/100)

            output = (evaporation/1000) * area_water
            return output

        def evaporation_unpaved():
            """
            Evaporation over the unpaved surface
            Unit: m3/hr
            """
            evaporation = season_selection() #mm/hr
            area_m2 = area * 10000
            area_water_m2 = area_m2 * (percentage_unpaved/100)

            output = evaporation/1000

            return output

        def pump():
            """
            The amount of water that gets pumped out
            Unit: m³/hr
            """
            pumpcapacity_hr = pumpcapacity * 60
            
            return pumpcapacity_hr
        
        t = 0
        dt = 0.5
        volume_0 = 50
        t_eind = 24
        
        t_list = []
        v_list = []
        h_list = []

        area_water = area * 10000 * (percentage_water/100)

        while t < t_eind:
            volume_0 = volume_0 + (precipitation_unpaved() + precipitation_paved(t) + precipitation_water(t) + seepage_in() - evaporation_water() - evaporation_unpaved() - pump()) * dt
            h = volume_0 / area_water
            v_list.append(round(volume_0,2))
            t_list.append(t)
            h_list.append(round(h, 5))
            t += dt
        
        values = {'tijd':t_list, 'volume': v_list, 'hoogte': h_list}
        output_df = pd.DataFrame(values)

        return output_df

    with col2:
        st.header('Visualisatie')
        st.write('''In de grafiek hieronder is een simulatie te zien van de grond- en oppervlaktewater in de tijd.
                  Met de slider kan aangegegeven worden welke tijdstap getoond moet worden, delijn verplaatst wel, 
                 maar in een heel kleine mate.''')
        time = st.slider("Tijdverloop in uren",0,simulation_duration)
        visualise()

        st.write('''In deze grafiek is het verloop van de waterstand te zien door een neerslag evenenment. 
                 De neerslag begint na 1 uur en valt daarna gedurende een uur, 
                 waarbij de hoeveelheid wordt bepaald met het keuzemenu neerslag.''')
        plot_waterstand = px.line(model(), x='tijd', y= 'hoogte',
                                   labels= {'tijd': 'tijd (hr)', 'hoogte': 'peilstijging (m)'})
        # plot_volume = px.line(model(), x='tijd', y= 'volume')
        
        st.plotly_chart(plot_waterstand)

    with col3: 
        pass

def page_three():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.header("Parameters")
        st.write("Vul onderstaande parameters in om een polder na te bootsen.")
        st.write()

        global soil
        soil = st.selectbox('Selecteer de grondsoort', ("Zand", "Klei", "Veen"))

        global precipitation
        precipitation = st.selectbox('Selecteerd het aantal mm neerslag', ("40mm", "60mm", "80mm", "100mm"))

        global season
        season = st.selectbox('Selecteer een seizoen voor de verdamping', ("Lente", "Zomer", "Herfst", "Winter"))

        global area
        area = st.slider("Oppervlakte polder in ha", 50, 20000, value = 8000)

        global percentage_paved, percentage_unpaved, percentage_water
        percentage_paved = st.slider('Percentage verhard oppervlakte: ', 0, 97, value= 30)
        percentage_unpaved = st.slider('Percentage onverhard oppervlakte: ', 1, 99-percentage_paved)
        percentage_water = 100 - percentage_paved - percentage_unpaved
        st.write(f'Verhoudingen polder: verhard= {percentage_paved}') 
        st.write(f'onverhard= {percentage_unpaved} openwater= {percentage_water}')

        global pumpcapacity
        pumpcapacity = st.slider('Geef de pompcapaciteit in m³/min', 0, 3000, value= 500)

        global seepage
        seepage = st.slider("Wat is de kwel (positief) of wegzijging (negatief) in mm/dag", min_value=-5, max_value=5, value= 0)


    def rainfall_selection():
        if precipitation == '40mm':
            return 40
        elif precipitation == '60mm':
            return 60
        elif precipitation == '80mm':
            return 80
        elif precipitation == '100mm':
            return 100

    def season_selection():
        if season == 'Lente':
            return 0.083
        elif season == 'Zomer':
            return 0.124
        elif season == 'Herfst':
            return 0.033
        elif season == 'Winter':
            return 0.013
        
    #Create model for groundlevel
    def mv(L, slope, depth, width, groundlevel):

        #Point on the x-axis for groundlevel
        xa = 0
        xb = xa + slope * depth
        xc = xb + width
        xd = xc + slope * depth
        xe = xd + L
        xf = xe + slope * depth
        xg = xf + width
        global xh
        xh = xg + slope * depth

        #Points on the y-axis for groundlevel
        ya = groundlevel
        global yb
        yb = ya - depth
        yc = yb
        yd = yc + depth
        ye = yd
        yf = ye - depth
        yg = yf
        yh = yg + depth

        #Create lists of the points for groundlevel
        global mvx
        global mvy
        mvx = [xa,xb,xc,xd,xe,xf,xg,xh]
        mvy = [ya,yb,yc,yd,ye,yf,yg,yh]
        
    mv(100, 3, 0.5, 2, 0)

    def model(): 
        def precipitation_unpaved():
            """
            water that will flow through the unpaved surface
            In: 
            OUT: 
            Unit: mm/hr
            """
            area_ha_unpaved = area * (percentage_unpaved/100)
            volume_l = 1.5 * 3600 * area_ha_unpaved
            return volume_l/1000

        def precipitation_paved(t):
            """
            Water that will flow over the paved surface into the open water area
            In:
            Out: 
            Unit: m³/hr
            """

            area_m2 = area * 10000 #m²
            area_m2_paved = area_m2 * (percentage_paved/100)
            precipitation_mhr = rainfall_selection() / 1000 #m/hr

            if t < 1:
                return 0
            elif t >= 1 and t < 2: 
                return area_m2_paved * precipitation_mhr #m³/hr
            else:
                return 0

        def precipitation_water(t):
            """
            Precipitation that will land directly in the open water
            IN:
            OUT:
            Unit: mm/hr
            """
            area_m2 = area * 10000 #m²
            area_m2_water = area_m2 * (percentage_water / 100)
            precipitation_mhr = rainfall_selection() / 1000 #m/hr

            if t < 1:
                return 0
            elif t >= 1 and t < 2: 
                return area_m2_water * precipitation_mhr #m³/hr
            else:
                return 0

        def seepage_in():
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
            Unit: m³/hr
            """
            
            evaporation = season_selection() #mm/hr
            area_m2 = area * 10000
            area_water_m2 = area_m2 * (percentage_water/100)

            output = (evaporation/1000) * area_water
            return output

        def evaporation_unpaved():
            """
            Evaporation over the unpaved surface
            Unit: m/hr
            """
            evaporation = season_selection() #mm/hr
            area_m2 = area * 10000
            area_water_m2 = area_m2 * (percentage_unpaved/100)

            output = evaporation/1000

            return output

        def pump():
            """
            The amount of water that gets pumped out
            Unit: m³/hr
            """
            pumpcapacity_hr = pumpcapacity * 60
            
            return pumpcapacity_hr
        
        t = 0
        dt = 0.5
        volume_0 = 50
        t_eind = 24
        
        t_list = []
        v_list = []
        h_list = []

        area_water = area * 10000 * (percentage_water/100)

        while t < t_eind:
            volume_0 = volume_0 + (precipitation_unpaved() + precipitation_paved(t) + precipitation_water(t) + seepage_in() - evaporation_water() - evaporation_unpaved() - pump()) * dt
            h = volume_0 / area_water
            v_list.append(round(volume_0,2))
            t_list.append(t)
            h_list.append(round(h, 5))
            t += dt
        
        values = {'tijd':t_list, 'volume': v_list, 'hoogte': h_list}
        output_df = pd.DataFrame(values)

        #Create model for groundwaterlevel
        def groundwater(precipitation, season, soil, start_waterlevel, distance_waterways, simulation_duration):
            
            P = [(rainfall_selection()/1000)] + [(0/1000)] * (simulation_duration-1)
            E = [(season_selection()/1000)] * simulation_duration     
            
            #Soil selection
            if soil == 'Zand':
                k = 5
            elif soil == 'Klei':
                k = 0.5
            elif soil == 'Veen':
                k = 0.01
                
            #Define other start valuables
            volume0 = area_water * start_waterlevel
            h = volume0 / area_water
            hg = start_waterlevel
            L = distance_waterways
            dt = 1
            
            #Create empty lists to fill with resultst with a for-loop
            global hgl
            global hl
            global tl
            hgl = []
            hl = []
            tl = []
            
            #Assign startvalues to lists
            hgl.append(hg)
            hl.append(h)
            tl.append(0)
            
            #For loop to calculate the groundwaterlevel every hour after the specified amount of rainfall
            for hour in range(0, simulation_duration):
                #If the waterlevel is below the groundwaterlevel, water will move from the groundwater to the surfacewater at speed q
                if h - hg < 0:
                    i = abs(h - hg) / (0.5 * L)
                    Q = (k * i) * 3600 * abs(h-hg) * 2
                    volume0 = volume0 + (precipitation_paved(t=(hour+1)) + precipitation_water(t=(hour+1)) + seepage_in() + Q/L - evaporation_water() - evaporation_unpaved() - pump()) * dt
                    dh = volume_0 / area_water
                    h = yb + dh
                    hg = hg + P[hour]/1000 - E[hour]/1000 - Q/L
                
                #If the groundwaterlevel is below the waterlevel, water will move from the groundwater to the surfacewater at speed q
                elif h - hg > 0:
                    i = abs(h - hg) / (0.5 * L)
                    Q = (k * i) * 3600 * abs(h-hg) * 2
                    volume0 = volume0 + (precipitation_paved(t=(hour+1)) + precipitation_water(t=(hour+1)) + seepage_in() - Q/L - evaporation_water() - evaporation_unpaved() - pump()) * dt
                    dh = volume_0 / area_water
                    h = yb + dh
                    hg = hg + P[hour]/1000 - E[hour]/1000 + Q/L
                
                #If the groundwaterlevel and the waterlevel are equal, no water will move between the waterstorages
                else:
                    volume0 = volume0 + (precipitation_paved(t=(hour+1)) + precipitation_water(t=(hour+1)) + seepage_in() - evaporation_water() - evaporation_unpaved() - pump()) * dt
                    dh = volume_0 / area_water
                    h = yb + dh
                    hg = hg + P[hour]/1000 - E[hour]/1000
                
                #The time is the amount of hours after startingpoint
                time = hour + 1
                
                #Add the new groundwaterlevel for each hour in the simulation
                hgl.append(hg)
                hl.append(h)
                tl.append(time)  

        simulation_duration = 120
        groundwater(precipitation=precipitation, season=season, soil=soil, start_waterlevel=-0.25, distance_waterways=20, simulation_duration= simulation_duration)
        time = st.slider("Tijdverloop in uren",0,simulation_duration)

        #Create model for visualisation
        def visualise():
            import plotly.graph_objects as go
            import pandas as pd

            #Code to calculate the intersections between the groundlevel and groundwaterlevel
            mv_df = pd.DataFrame({'x':mvx, 'y':mvy})

            #Intersection 1
            a1 = (mv_df.y[1] - mv_df.y[0]) / (mv_df.x[1] - mv_df.x[0])
            b1 = mv_df.y[1] - a1 * mv_df.x[1]
            int1 = (hgl[time] - b1) / a1
            inta = (hl[time] - b1) / a1

            #Intersection 2
            a2 = (mv_df.y[3] - mv_df.y[2]) / (mv_df.x[3] - mv_df.x[2])
            b2 = mv_df.y[3] - a2 * mv_df.x[3]
            int2 = (hgl[time] - b2) / a2
            intb = (hl[time] - b2) / a2

            #Intersection 3
            a3 = (mv_df.y[5] - mv_df.y[4]) / (mv_df.x[5] - mv_df.x[4])
            b3 = mv_df.y[5] - a3 * mv_df.x[5]
            int3 = (hgl[time] - b3) / a3
            intc = (hl[time] - b3) / a3

            #Intersection 4
            a4 = (mv_df.y[7] - mv_df.y[6]) / (mv_df.x[7] - mv_df.x[6])
            b4 = mv_df.y[7] - a4 * mv_df.x[7]
            int4 = (hgl[time] - b4) / a4
            intd = (hl[time] - b4) / a4

            mv_df = pd.DataFrame({'x':mvx, 'y':mvy}) 

            fig = go.Figure(
                layout = {
                    'showlegend': False,
                    'xaxis': {
                        'range': [0, xh],
                        'showgrid': False,
                        'zeroline': False, 
                        'visible': False
                    }
                }
            )

            fig.add_trace(go.Scatter(
                x=mv_df.x, 
                y=mv_df.y, 
                mode='lines', 
                marker = {'color' : 'green'}))
            fig.add_trace(go.Scatter(
                x=[0, int1], 
                y=[hgl[time], hgl[time]], 
                mode='lines', 
                marker = {'color' : 'skyblue'}))
            fig.add_trace(go.Scatter(
                x=[int2, int3], 
                y=[hgl[time], hgl[time]], 
                mode='lines', 
                marker = {'color' : 'skyblue'}))
            fig.add_trace(go.Scatter(
                x=[int4, xh], 
                y=[hgl[time], hgl[time]], 
                mode='lines', 
                marker = {'color' : 'skyblue'}))
            fig.add_trace(go.Scatter(
                x=[inta, intb], 
                y=[hl[time], hl[time]], 
                mode='lines', 
                marker = {'color' : 'skyblue'}))
            fig.add_trace(go.Scatter(
                x=[intc, intd], 
                y=[hl[time], hl[time]], 
                mode='lines', 
                marker = {'color' : 'skyblue'}))
            
            return fig
            #st.write(fig)
            #st.write(hgl[time])       
        fig = visualise()
        return output_df,fig

    

    with col2:
        st.header('Visualisatie')
        st.write('''In de grafiek hieronder is een simulatie te zien van de grond- en oppervlaktewater in de tijd.
                  Met de slider kan aangegegeven worden welke tijdstap getoond moet worden. Deze grafiek werkt het beste 
                 als de grondsoort Veen is, en het percentage onverhard 1%. Verder is deze code vooral een vorm van magie.''')
                
        model_df, fig = model()
        st.write(fig)

        st.write('''In deze grafiek is het verloop van de waterstand te zien door een neerslag evenenment. 
                 De neerslag begint na 1 uur en valt daarna gedurende een uur, 
                 waarbij de hoeveelheid wordt bepaald met het keuzemenu neerslag.''')
        plot_waterstand = px.line(model_df, x='tijd', y= 'hoogte', range_y= [-0.5, 0.5],
                                   labels= {'tijd': 'tijd (hr)', 'hoogte': 'peilstijging (m)'})
                
        st.plotly_chart(plot_waterstand)

    with col3: 
        pass

#Code to select a page and to visualise the appropriate information
st.sidebar.write("""# Selectie menu""")
menu = st.sidebar.radio('Selecteer een pagina', ('Welkom',  'Model', 'Magie'))

if menu == 'Welkom':
    page_one()     
    
elif menu == 'Model':
    page_two()
    
elif menu == 'Magie':
    page_three()
#     page_two()
#     page_three()    
    