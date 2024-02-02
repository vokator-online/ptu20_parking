import sqlite3
import PySimpleGUI as sg
from parking_db import connection, cursor
from typing import Any

def get_tariff_list(
        connection: sqlite3.Connection = connection, 
        cursor: sqlite3.Cursor = cursor,
    ) -> list[Any]:
    with connection:
        cursor.execute("SELECT * FROM tariff ORDER BY duration_hours")
        tariff_list = cursor.fetchall()
    return tariff_list

def db_insert_tariff(
        values: tuple[str, Any], 
        connection: sqlite3.Connection = connection,
        cursor: sqlite3.Cursor = cursor,
    ) -> bool:
    try:
        duration_hours = int(values["-DURATION-"])
        price_per_hour = float(values["-RATE-"])
    except ValueError:
        sg.PopupOK("You must enter numeric values", title="Error")
        return False
    query = "INSERT INTO tariff (duration_hours, price_per_hour) VALUES (?, ?)"
    try:
        with connection:
            cursor.execute(query, (duration_hours, price_per_hour))
    except Exception as error:
        sg.PopupOK(f"Database error {error.__class__.__name__}: {error}", title="DB Error")
        return False
    sg.PopupAutoClose("Insertion Successful", auto_close_duration=2, title="Success")
    return True

def add_tariff(tariff_manager_window: sg.Window) -> bool:
    tariff_manager_window.hide()
    layout = [
        [sg.Text("max hours:", size=10), sg.Input(key="-DURATION-", size=7, justification="right")],
        [sg.Text("hourly rate:", size=10), sg.Input(key="-RATE-", size=7, justification="right")],
        [sg.Button("Add", key="-ADD-"), sg.Button("Cancel", key="-CANCEL-")],
    ]
    window = sg.Window(
        "Add tariff | Parking PTU20", 
        layout, 
        element_padding=10,
    )
    success = False
    while True:
        event, values = window.read()
        if event in [sg.WINDOW_CLOSED, "-CANCEL-"]:
            break
        if event == "-ADD-":
            success = db_insert_tariff(values)
            if success:
                break
    window.close()
    tariff_manager_window.un_hide()
    return success

def db_remove_tariff(
        values: tuple[str, Any], 
        tariff_list: list[Any],
        connection: sqlite3.Connection = connection,
        cursor: sqlite3.Cursor = cursor,
    ) -> bool:
    tariff_to_remove = tariff_list[values["-TARIFF-LIST-"][0]]
    if sg.PopupYesNo(f"Remove tariff up to {tariff_to_remove[1]} hours at"
                     f"{tariff_to_remove[2]} EUR/hour rate?", title="Remove?") == "Yes":
        try:
            with connection:
                cursor.execute("DELETE FROM tariff WHERE id=?", (tariff_to_remove[0],))
        except Exception as error:
            sg.PopupOK(f"Database error {error.__class__.__name__}: {error}", title="DB Error")
            return False
        else:
            sg.PopupAutoClose("Removal Successful", auto_close_duration=2, title="Success")
            return True
    else:
        return False
    
def refresh_tariff_table(window: sg.Window) -> list[Any]:
    tariff_list = get_tariff_list()
    display_tariff_list = [(tariff[1], tariff[2]) for tariff in tariff_list]
    window["-TARIFF-LIST-"].update(values=display_tariff_list)
    return tariff_list

def manage_tariffs(main_window: sg.Window):
    main_window.hide()
    tariff_list = get_tariff_list()
    display_tariff_list = [(tariff[1], tariff[2]) for tariff in tariff_list]
    layout = [
        [sg.Table(display_tariff_list, key="-TARIFF-LIST-",
                     headings=["max hours", "hourly rate"], 
                     expand_x=True, expand_y=True)],
        [
            sg.Button("Add", key="-ADD-"), 
            sg.Button("Remove", key="-REMOVE-"),
            sg.Button("Return", key="-RETURN-"),
        ],
    ]
    window = sg.Window(
        "Tariffs | Parking PTU20", 
        layout, 
        element_padding=10,
        size=(500, 500),
    )
    while True:
        event, values = window.read()
        if event in [sg.WINDOW_CLOSED, "-RETURN-"]:
            break
        if event == "-ADD-":
            if add_tariff(window):
                tariff_list = refresh_tariff_table(window)
        if event == "-REMOVE-":
            if values["-TARIFF-LIST-"] and \
                    len(values["-TARIFF-LIST-"]) > 0 and \
                    db_remove_tariff(values, tariff_list):
                tariff_list = refresh_tariff_table(window)

    window.close()
    main_window.un_hide()
