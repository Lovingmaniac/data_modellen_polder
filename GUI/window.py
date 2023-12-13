import tkinter as tk
from tkinter import ttk

# window
window = tk.Tk()
window.title('Pixel Polder')
window.geometry('800x500')

# title
title_label = ttk.Label(master= window, text= 'Welkom in de Pixel Polder', font= 'arial 24 bold')
title_label.pack()

# input
input_frame = ttk.Frame(master= window)

# entry variables
var_percipitation = tk.IntVar()
var_evaporation = tk.IntVar()
var_area = tk.IntVar()
var_soil = tk.StringVar()
var_percentage_openwater = tk.IntVar()
var_percentage_paved = tk.IntVar()
var_percentage_unpaved = tk.IntVar()

#entry labels
label_percipitation = ttk.Label(master= input_frame, text= 'neerslag')
label_evaporation = ttk.Label(master= input_frame, text= 'verdamping')
label_area = ttk.Label(master= input_frame, text= 'oppervlakte')
label_soil = ttk.Label(master= input_frame, text= 'grondsoort')
label_percentage_openwater = ttk.Label(master= input_frame, text= 'percentage open water')
label_percentage_paved = ttk.Label(master= input_frame, text= 'percentage verhard')
label_percentage_unpaved = ttk.Label(master= input_frame, text= 'percentage onverhard')


# entry fields
entry_percipitation = ttk.Entry(master= input_frame, textvariable= var_percipitation)
entry_evaporation = ttk.Entry(master= input_frame, textvariable= var_evaporation)
entry_area = ttk.Entry(master= input_frame, textvariable= var_area)
entry_soil = ttk.Entry(master= input_frame, textvariable= var_soil)
entry_percentage_openwater = ttk.Entry(master= input_frame, textvariable= var_percentage_openwater)
entry_percentage_paved = ttk.Entry(master= input_frame, textvariable= var_percentage_paved)
entry_percentage_unpaved = ttk.Entry(master= input_frame, textvariable= var_percentage_unpaved)

entries = [entry_percipitation, entry_evaporation, entry_area, entry_soil, entry_percentage_openwater, entry_percentage_paved, entry_percentage_unpaved]
labels = [label_percipitation, label_evaporation, label_area, label_soil, label_percentage_openwater, label_percentage_paved, label_percentage_unpaved]

for entry in entries:
    entry.pack()

input_frame.pack()
#run
window.mainloop()