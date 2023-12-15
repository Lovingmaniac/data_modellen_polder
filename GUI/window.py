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

input_frame_percipitation = ttk.Frame(master= input_frame)
input_frame_evaporation = ttk.Frame(master= input_frame)
input_frame_area = ttk.Frame(master= input_frame)
input_frame_soil = ttk.Frame(master= input_frame)
input_frame_percentage_openwater = ttk.Frame(master= input_frame)
input_frame_percentage_paved = ttk.Frame(master= input_frame)
input_frame_percentage_unpaved = ttk.Frame(master= input_frame)

# entry variables
var_percipitation = tk.IntVar()
var_evaporation = tk.IntVar()
var_area = tk.IntVar()
var_soil = tk.StringVar()
var_percentage_openwater = tk.IntVar()
var_percentage_paved = tk.IntVar()
var_percentage_unpaved = tk.IntVar()

#entry labelsc
label_percipitation = ttk.Label(master= input_frame_percipitation, text= 'neerslag').pack(side= 'left', padx= 10)
label_evaporation = ttk.Label(master= input_frame_evaporation, text= 'verdamping').pack(side= 'left')
label_area = ttk.Label(master= input_frame_area, text= 'oppervlakte').pack(side= 'left')
label_soil = ttk.Label(master= input_frame_soil, text= 'grondsoort').pack(side= 'left')
label_percentage_openwater = ttk.Label(master= input_frame_percentage_openwater, text= 'percentage open water').pack(side= 'left')
label_percentage_paved = ttk.Label(master= input_frame_percentage_paved, text= 'percentage verhard').pack(side= 'left')
label_percentage_unpaved = ttk.Label(master= input_frame_percentage_unpaved, text= 'percentage onverhard').pack(side= 'left')


# entry fields
entry_percipitation = ttk.Entry(master= input_frame_percipitation, textvariable= var_percipitation).pack(side= 'right')
entry_evaporation = ttk.Entry(master= input_frame_evaporation, textvariable= var_evaporation).pack(side= 'right')
entry_area = ttk.Entry(master= input_frame_area, textvariable= var_area).pack(side= 'right')
entry_soil = ttk.Entry(master= input_frame_soil, textvariable= var_soil).pack(side= 'right')
entry_percentage_openwater = ttk.Entry(master= input_frame_percentage_openwater, textvariable= var_percentage_openwater).pack(side= 'right')
entry_percentage_paved = ttk.Entry(master= input_frame_percentage_paved, textvariable= var_percentage_paved).pack(side= 'right')
entry_percentage_unpaved = ttk.Entry(master= input_frame_percentage_unpaved, textvariable= var_percentage_unpaved).pack(side= 'right')

input_frame_percipitation.pack()
input_frame_evaporation.pack()
input_frame_area.pack()
input_frame_soil.pack()
input_frame_percentage_openwater.pack()
input_frame_percentage_paved.pack()
input_frame_percentage_unpaved.pack()

input_frame.pack()
#run
window.mainloop()