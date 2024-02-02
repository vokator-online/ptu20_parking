import PySimpleGUI as sg
from gui_tariffs import manage_tariffs
from gui_arrival import register_arrival
from gui_departure import register_departure
from gui_reports import reports
from datetime import datetime

sg.theme("dark")
sg.set_options(font="sans-serif 20")

main_layout = [
    [
        sg.Button("Arrival", key="-ARRIVAL-", size=10),
        sg.Button("Departure", key="-DEPARTURE-", size=10),
    ],
    [
        sg.Text(datetime.now().strftime("%Y-%m-%d  %H:%M:%S"), key="-TIME-"),
    ],
    [
        sg.Button("Manage Tariffs", key="-TARIFFS-", size=21),
    ],
    [
        sg.Button("Reports", key="-REPORTS-", size=21),
    ],
    [
        sg.Button("Exit", key="-EXIT-", size=21),
    ],
]

main_window = sg.Window(
    "Parking PTU20", 
    main_layout, 
    element_justification="center", 
    element_padding=10,
    finalize=True
)

while True:
    event, values = main_window.read(timeout=0.1)
    if event in [sg.WINDOW_CLOSED, "-EXIT-"]:
        break
    if event == "-TARIFFS-":
        manage_tariffs(main_window)
    if event == "-ARRIVAL-":
        register_arrival(main_window)
    if event == "-DEPARTURE-":
        register_departure(main_window)
    if event == "-REPORTS-":
        reports(main_window)
    main_window["-TIME-"].update(datetime.now().strftime("%Y-%m-%d  %H:%M:%S"))
