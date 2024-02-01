import sqlite3
import PySimpleGUI as sg
from parking_db import connection, cursor

def get_tariff_list(
        connection: sqlite3.Connection = connection, 
        cursor: sqlite3.Cursor = cursor):
    with connection:
        cursor.execute("SELECT * FROM tariff ORDER BY duration_hours")
        tariff_list = cursor.fetchall()
    return tariff_list

def add_tariff(tariff_manager_window: sg.Window):
    tariff_manager_window.hide()
    layout = [
        [sg.Text("max hours:", size=10), sg.Input(key="-DURATION-", size=7, justification="right")],
        [sg.Text("hourly rate:", size=10), sg.Input(key="-RATE-", size=7, justification="right")],
        [sg.Button("Add", key="-ADD-"), sg.Button("Cancel", key="-CANCEL-")],
    ]
    window = sg.Window(
        "Add tariff | Parking PTU20", 
        layout, 
        font="sans-serif 20", 
        element_padding=10,
    )
    while True:
        event, values = window.read()
        if event in [sg.WINDOW_CLOSED, "-CANCEL-"]:
            break
    window.close()
    tariff_manager_window.un_hide()

def manage_tariffs(main_window: sg.Window):
    main_window.hide()
    layout = [
        [sg.Table(get_tariff_list(), headings=["id", "max hours", "hourly rate"], expand_x=True, expand_y=True)],
        [sg.Button("Add", key="-ADD-"), sg.Button("Remove", key="-REMOVE-")],
    ]
    window = sg.Window(
        "Tariffs | Parking PTU20", 
        layout, 
        font="sans-serif 20", 
        element_padding=10,
        size=(500, 500),
    )
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "-ADD-":
            add_tariff(window)
    window.close()
    main_window.un_hide()
