import sqlite3
import PySimpleGUI as sg
from parking_db import connection, cursor
from typing import Any
from datetime import date, timedelta

def get_parkings(departure_from: str, departure_to: str,
    connection: sqlite3.Connection = connection,
    cursor: sqlite3.Cursor = cursor,
) -> list[Any]:
    query = '''SELECT plate, arrival, departure, price_per_hour, total_price
    FROM parking 
    JOIN car ON car_id = car.id
    JOIN tariff ON tariff_id = tariff.id
    WHERE departure >= DATE(?) AND departure <= DATE(?);'''
    with connection:
        try:
            cursor.execute(query, (departure_from, departure_to))
            parkings = cursor.fetchall()
        except Exception as error:
            sg.PopupOK(f"DB Error {error.__class__.__name__}: {error}", title="DB Error")
            return []
    clean_parkings = []
    for parking in parkings:
        clean_parkings.append((
            parking[0], 
            parking[1][:19], 
            parking[2][:19], 
            f"{parking[3]:0.2f} €", 
            f"{parking[4]:0.2f} €", 
        ))
    return clean_parkings

def get_total_revenue(departure_from: str, departure_to: str,
    connection: sqlite3.Connection = connection,
    cursor: sqlite3.Cursor = cursor,
) -> str:
    query = '''SELECT SUM(total_price) FROM parking 
    WHERE departure >= DATE(?) AND departure <= DATE(?);'''
    with connection:
        try:
            cursor.execute(query, (departure_from, departure_to))
            result = cursor.fetchone()
        except Exception as error:
            sg.PopupOK(f"DB Error {error.__class__.__name__}: {error}", title="DB Error")
            total = 0
        else:
            total = result[0] or 0
    return f"{total:.2f} €"

def reports(main_window: sg.Window):
    main_window.hide()
    minus_week = str(date.today() - timedelta(days=7))
    tomorrow = str(date.today() + timedelta(days=1))
    layout = [
        [
            sg.Text("Period:"),
            sg.Input(key="-FROM-", size=10, default_text=minus_week),
            sg.Text("-"), 
            sg.Input(key="-TO-", size=10, default_text=tomorrow),
            sg.Button("Filter", key="-FILTER-"),
            sg.Button("Return", key="-RETURN-"),
        ],
        [sg.Table(get_parkings(minus_week, tomorrow), 
                  key="-TABLE-", expand_x=True,
                  headings=("Plate", "Arrival", "Departure", "Tariff", "Price"))],
        [sg.Text("Total Revenue:"), sg.Text(get_total_revenue(minus_week, tomorrow), key="-TOTAL-")],
    ]
    window = sg.Window("Reports | Parking PTU20", layout, element_padding=10,)
    while True:
        event, values = window.read()
        if event in [sg.WINDOW_CLOSED, "-RETURN-"]:
            break
        if event == "-FILTER-":
            window["-TABLE-"].update(values=get_parkings(values["-FROM-"], values["-TO-"]))
            window["-TOTAL-"].update(get_total_revenue(values["-FROM-"], values["-TO-"]))
    window.close()
    main_window.un_hide()
