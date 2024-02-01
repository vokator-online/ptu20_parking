import PySimpleGUI as sg
from gui_tariffs import manage_tariffs

sg.theme("dark")
sg.set_options(font="sans-serif 20")

main_layout = [
    [
        sg.Button("Tariffs", key="-TARIFFS-", size=10),
        sg.Button("Cars", key="-CARS-", size=10),
    ],
    [
        sg.Button("Arrival", key="-ARRIVAL-", size=10),
        sg.Button("Departure", key="-DEPARTURE-", size=10),
    ],
    [
        sg.Button("Reports", key="-REPORTS-", size=21),
    ]
]

main_window = sg.Window(
    "Parking PTU20", 
    main_layout, 
    element_justification="center", 
    element_padding=10,
)

while True:
    event, values = main_window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "-TARIFFS-":
        manage_tariffs(main_window)
