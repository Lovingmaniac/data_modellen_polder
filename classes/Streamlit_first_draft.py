#Import packages
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

    global evaporation
    evaporation = st.selectbox('Selecteer een seizoen voor de verdamping', ("Lente", "Zomer", "Herfst", "Winter"))

    global area
    area = st.slider('Geef aan wat de grootte is van de polder in ha', 50, 2000)

#Defenition that contains all the necessary infomation for page 3    
def page_three():
    pass

#Code to select a page and to visualise the appropriate information
st.sidebar.write("""# Selectie menu""")
menu = st.sidebar.radio('Selecteer een pagina', ('Welkom',  'Parameters', 'Visualisatie'))

if menu == 'Welkom':
    page_one()     
    
elif menu == 'Parameters':
    page_two()
    
elif menu == 'Visualisatie':
    page_three()  