import streamlit as st

#Defenition that contains all the necessary information for page 1
def page_one():
    st.title("DE PIXELPOLDER")
    st.write()
    st.write("Welkom bij de interactieve poldersimulatie! Laat je het regenen met pijpenstelen of zonnestralen?")
    st.write("Pas de parameters op pagina 2 aan en bekijk wat het effect is op de waterstanden in de polder.")

#Defenition that contains all the necessary information for page 2
def page_two():
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
    area = st.slider("Oppervlakte polder in ha", 50, 20000)

    global percentage_paved, percentage_unpaved, percentage_water
    percentage_paved = st.slider('Percentage verhard oppervlakte: ', 0, 100)
    percentage_unpaved = st.slider('Percentage onverhard oppervlakte: ', 0, 100-percentage_paved)
    percentage_water = 100 - percentage_paved - percentage_unpaved
    st.write(f'Verhoudingen polder: \n verhard= {percentage_paved} \n onverhard= {percentage_unpaved} \n openwater= {percentage_water}')

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

        #return mvx, mvy
        
    mv(20, 3, 2, 2, 0)

    #Create model for groundwaterlevel
    def groudnwater(precipitation, season, soil, start_waterlevel, distance_waterways, simulation_duration):
        
        #Rainfall selection
        if precipitation == '40mm':
            P = [(40/1000)] + [(0/1000)] * (simulation_duration-1)
        elif precipitation == '60mm':
            P = [(60/1000)] + [(0/1000)] * (simulation_duration-1)
        elif precipitation == '80mm':
            P = [(80/1000)] + [(0/1000)] * (simulation_duration-1)
        elif precipitation == '100mm':
            P = [(100/1000)] + [(0/1000)] * (simulation_duration-1)
            
        #Evaporation selection
        if season == 'Lente':
            E = [(0.083/1000)] * simulation_duration
        elif season == 'Zomer':
            E = [(0.124/1000)] * simulation_duration
        elif season == 'Herfst':
            E = [(0.033/1000)] * simulation_duration
        elif season == 'Winter':
            E = [(0.013/1000)] * simulation_duration
        
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
                q = (k * i) * 3600
                hg = hg + P[hour]/1000 - E[hour]/1000 - q
            
            #If the groundwaterlevel is below the waterlevel, water will move from the groundwater to the surfacewater at speed q
            elif h - hg > 0:
                i = abs(h - hg) / (0.5 * L)
                q = (k * i) * 3600
                hg = hg + P[hour]/1000 - E[hour]/1000 + q
            
            #If the groundwaterlevel and the waterlevel are equal, no water will move between the waterstorages
            else:
                hg = hg + P[hour]/1000 - E[hour]/1000
            
            #The time is the amount of hours after startingpoint
            time = hour + 1
            
            #Add the new groundwaterlevel for each hour in the simulation
            hgl.append(hg)
            t.append(time)
            
        #return hgl, t

    groudnwater(precipitation=precipitation, season=season, soil=soil, start_waterlevel=-1, distance_waterways=20, simulation_duration=120)

    #Create model for visualisation
    def visualise():
        import plotly.graph_objects as go
        import pandas as pd

        #Code to calculate the intersections between the groundlevel and groundwaterlevel
        mv_df = pd.DataFrame({'x':mvx, 'y':mvy})

        #Intersection 1
        a1 = (mv_df.y[1] - mv_df.y[0]) / (mv_df.x[1] - mv_df.x[0])
        b1 = mv_df.y[1] - a1 * mv_df.x[1]
        int1 = (hgl[0] - b1) / a1

        #Intersection 2
        a2 = (mv_df.y[3] - mv_df.y[2]) / (mv_df.x[3] - mv_df.x[2])
        b2 = mv_df.y[3] - a2 * mv_df.x[3]
        int2 = (hgl[0] - b2) / a2

        #Intersection 3
        a3 = (mv_df.y[5] - mv_df.y[4]) / (mv_df.x[5] - mv_df.x[4])
        b3 = mv_df.y[5] - a3 * mv_df.x[5]
        int3 = (hgl[0] - b3) / a3

        #Intersection 4
        a4 = (mv_df.y[7] - mv_df.y[6]) / (mv_df.x[7] - mv_df.x[6])
        b4 = mv_df.y[7] - a4 * mv_df.x[7]
        int4 = (hgl[0] - b4) / a4

        mv_df = pd.DataFrame({'x':mvx, 'y':mvy}) 

        fig = go.Figure(
            layout = {
                'showlegend': False,
                'xaxis': {
                    'range': [0, 48],
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
            y=[hgl[0], hgl[0]], 
            mode='lines', 
            marker = {'color' : 'skyblue'}))

        st.write(fig)
    
    visualise()


#Defenition that contains all the necessary infomation for page 3    
# def page_three():
#     global time
#     time = st.slider('Tijdlijn voor aantal uur vanaf de start van de regenbui', 0, 120)

#Code to select a page and to visualise the appropriate information
st.sidebar.write("""# Selectie menu""")
menu = st.sidebar.radio('Selecteer een pagina', ('Welkom',  'Parameters', 'Visualisatie'))

if menu == 'Welkom':
    page_one()     
    
elif menu == 'Parameters':
    page_two()
    
# elif menu == 'Visualisatie':
#     page_two()
#     page_three()    
    