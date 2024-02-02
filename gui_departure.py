import sqlite3
import PySimpleGUI as sg
from parking_db import connection, cursor
from typing import Any
from datetime import datetime, timedelta
from gui_tariffs import get_tariff_list
from math import ceil

def get_duration_in_hours(duration: timedelta) -> int:
    duration_hours = duration.days * 24 + duration.seconds / 3600
    rounded_up_duration = ceil(duration_hours)
    return rounded_up_duration

def find_tariff(duration: timedelta) -> tuple:
    duration_hours = duration.days * 24 + duration.seconds / 3600
    tariff_list = get_tariff_list()
    selected_tariff = tariff_list[0]
    for tariff in tariff_list:
        # print(duration_hours, tariff)
        if duration_hours > tariff[1]:
            continue
        else:
            selected_tariff = tariff
            break
    else:
        selected_tariff = tariff_list[-1]
    # print(selected_tariff)
    return selected_tariff

def process_departure(
    values: list[Any],
    connection: sqlite3.Connection = connection,
    cursor: sqlite3.Cursor = cursor,
) -> bool:
    try:
        query = """SELECT parking.id, arrival FROM parking 
        JOIN car ON car_id = car.id
        WHERE plate=? AND departure IS NULL"""
        with connection:
            cursor.execute(query, (values["-PLATE-"],))
            parking_entry = cursor.fetchone()
    except Exception as error:
        sg.PopupOK(f"DB Error {error.__class__.__name__}: {error}", title="DB Error")
        return False
    # print(parking_entry)
    if not parking_entry:
        sg.PopupOK(f"Car with plate {values['-PLATE-']} is not parked here.")
        return False
    departure_time = datetime.now()
    parking_duration = departure_time - datetime.fromisoformat(parking_entry[1])
    tariff = find_tariff(parking_duration)
    duration = get_duration_in_hours(parking_duration)
    total_price = tariff[2] * duration
    # print(tariff, duration, total_price)
    try:
        with connection:
            cursor.execute("UPDATE parking SET departure=?, tariff_id=?, total_price=? "
                           "WHERE id=?", (departure_time, tariff[0], total_price, parking_entry[0]))
    except Exception as error:
        sg.PopupOK(f"DB error {error.__class__.__name__}: {error}", title="DB Error")
        return False
    else:
        sg.PopupOK(f"{values['-PLATE-']} total duration: {duration} h, price: {total_price}", title="Success")
        return True

def register_departure(main_window: sg.Window):
    main_window.hide()
    layout = [
        [sg.Text("Plate Number:"), sg.Input(key="-PLATE-", size=15)],
        [
            sg.Button("Register", key="-REGISTER-"),
            sg.Button("Return", key="-RETURN-"),
        ],
    ]
    window = sg.Window(
        "Register Departure | Parking PTU20",
        layout,
        element_padding=10,
    )
    while True:
        event, values = window.read()
        if event in [sg.WINDOW_CLOSED, "-RETURN-"]:
            break
        if event == "-REGISTER-" and process_departure(values):
            break
    window.close()
    main_window.un_hide()
