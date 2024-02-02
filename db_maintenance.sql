-- SQLite
SELECT parking.id, arrival, departure, car_id, plate, tariff_id, total_price
FROM parking JOIN car ON car_id = car.id;

UPDATE parking SET arrival=DATETIME("2024-01-31 09:06:08.426270"),
departure=DATETIME("2024-01-31 10:07:03.062513") WHERE id=9;
