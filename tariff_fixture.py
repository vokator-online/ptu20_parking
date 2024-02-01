import sqlite3

connection = sqlite3.connect("parking.db")
cursor = connection.cursor()

def populate_tariffs(
        connection: sqlite3.Connection = connection, 
        cursor: sqlite3.Cursor = cursor,
    ):
    tariffs = [
        (2, 0),
        (8, 2),
        (24, 1),
        (24 * 7, 0.5),
        (24 * 365, 0.2),
    ]
    query = "INSERT INTO tariff (duration_hours, price_per_hour) VALUES (?, ?)"
    with connection:
        cursor.executemany(query, tariffs)

if __name__ == "__main__":
    populate_tariffs()
