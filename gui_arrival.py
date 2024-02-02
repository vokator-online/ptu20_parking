import sqlite3
import PySimpleGUI as sg
from parking_db import connection, cursor
from typing import Any
from datetime import datetime
from gui_departure import get_parked_car

def insert_arrival(
        values: list[Any],
        connection: sqlite3.Connection = connection,
        cursor: sqlite3.Cursor = cursor,
    ) -> bool:
    if len(values['-PLATE-']) == 0 or values["-PLATE-"].startswith(' '):
        sg.PopupOK("Plate cannot be empty and must not start with a space", title="Input Error")
        return False
    parked_car = get_parked_car(values)
    if parked_car:
        sg.PopupOK(f"This car is already parked from {parked_car[1][:19]}")
        return False
    try:
        with connection:
            cursor.execute("INSERT INTO car (plate) VALUES (?)", (values["-PLATE-"],))
    except Exception:
        sg.PopupAutoClose(f"Car with plate {values['-PLATE-']} already exists", 
                          auto_close_duration=1, title="Car Found")
    try:
        with connection:
            cursor.execute("SELECT id, plate FROM car WHERE plate = ?", (values["-PLATE-"],))
            car = cursor.fetchone()
    except Exception as error:
        sg.PopupOK(f"Error {error.__class__.__name__}: {error}", title="Error")
        return False
    try:
        arrival_time = datetime.now()
        with connection:
            cursor.execute(
                "INSERT INTO parking (arrival, car_id) VALUES (DATETIME(?), ?)",
                (arrival_time, car[0])
            )
    except Exception as error:
        sg.PopupOK(f"DB error {error.__class__.__name__}: {error}", title="DB Error")
        return False
    else:
        sg.PopupAutoClose(f"Arrival of {values['-PLATE-']} registered at {arrival_time} successfully",
                          title="Success", auto_close_duration=2)
        return True

def register_arrival(main_window: sg.Window):
    main_window.hide()
    layout = [
        [sg.Text("Plate Number:"), sg.Input(key="-PLATE-", size=15)],
        [
            sg.Button("Register", key="-REGISTER-"),
            sg.Button("Return", key="-RETURN-"),
        ],
    ]
    window = sg.Window(
        "Register Arrival | Parking PTU20",
        layout,
        element_padding=10,
    )
    while True:
        event, values = window.read()
        if event in [sg.WINDOW_CLOSED, "-RETURN-"]:
            break
        if event == "-REGISTER-" and insert_arrival(values):
            break
    window.close()
    main_window.un_hide()
