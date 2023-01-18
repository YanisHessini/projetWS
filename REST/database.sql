CREATE DATABASE IF NOT EXISTS trains;

USE trains;

create table IF NOT EXISTS trains (
    id int auto_increment primary key,
    departure_station  text null,
    arrival_station    text null,
    departure_date     datetime   null,
    arrival_date       datetime   null,
    total_seats        int        not null,
    nb_class_1         int        not null,
    nb_class_2         int        not null,
    nb_class_3         int        not null,
		current_nb_class_1 int 				not null,
		current_nb_class_2 int 				not null,
		current_nb_class_3 int 				not null,
		price_class_1      int        not null,
		price_class_2      int        not null,
		price_class_3      int        not null,
		complete 					 boolean    not null,
		available_seats    int        not null,

		CONSTRAINT departure_date_before_arrival_date CHECK (departure_date < arrival_date),
		CONSTRAINT total_seats_greater_than_0 CHECK (total_seats > 0),
		CONSTRAINT nb_class_1_greater_than_0 CHECK (nb_class_1 > 0),
		CONSTRAINT nb_class_2_greater_than_0 CHECK (nb_class_2 > 0),
		CONSTRAINT nb_class_3_greater_than_0 CHECK (nb_class_3 > 0),
		CONSTRAINT price_class_1_greater_than_0 CHECK (price_class_1 > 0),
		CONSTRAINT price_class_2_greater_than_0 CHECK (price_class_2 > 0),
		CONSTRAINT price_class_3_greater_than_0 CHECK (price_class_3 > 0)
);

create table IF NOT EXISTS reservations (
    id int auto_increment primary key,
    first_name text null,
    last_name text null,
    id_train int not null,
	class int not null,
		foreign key (id_train) references trains(id)
);

INSERT INTO trains (departure_station, arrival_station, departure_date, arrival_date, total_seats, nb_class_1, nb_class_2, nb_class_3, 
current_nb_class_1, current_nb_class_2, current_nb_class_3, price_class_1, price_class_2, price_class_3, complete, available_seats)
SELECT 'Lyon', 'Marseille', '2023-01-19 15:00:00', '2023-01-19 17:00:00', 100, 20, 30, 50, 0, 0, 0, 120, 70, 30, false, 100
UNION ALL
SELECT 'Paris', 'Marseille', '2023-01-20 10:00:00', '2023-01-20 16:00:00', 100, 20, 30, 50, 0, 0, 0, 120, 70, 30, false, 100
UNION ALL
SELECT 'Paris', 'Lyon', '2023-01-21 10:00:00', '2023-01-21 14:00:00', 100, 20, 30, 50, 0, 0, 0, 120, 70, 30, false, 100
UNION ALL
SELECT 'Lyon', 'Nice', '2023-01-19 15:00:00', '2023-01-19 17:00:00', 100, 25, 35, 40, 0, 0, 0, 130, 80, 40, false, 100
UNION ALL
SELECT 'Paris', 'Bordeaux', '2023-01-19 10:00:00', '2023-01-19 16:00:00', 100, 25, 35, 40, 0, 0, 0, 130, 80, 40, false, 100
UNION ALL
SELECT 'Lille', 'Strasbourg', '2023-01-22 10:00:00', '2023-01-22 14:00:00', 100, 25, 35, 40, 0, 0, 0, 130, 80, 40, false, 100
UNION ALL
SELECT 'Marseille', 'Lyon', '2023-01-19 18:00:00', '2023-01-19 20:00:00', 100, 15, 20, 65, 0, 0, 0, 110, 60, 25, false, 100
UNION ALL
SELECT 'Nice', 'Paris', '2023-01-19 12:00:00', '2023-01-19 16:00:00', 100, 15, 20, 65, 0, 0, 0, 110, 60, 25, false, 100
UNION ALL
SELECT 'Bordeaux', 'Lille', '2023-01-19 12:00:00', '2023-01-19 14:00:00', 100, 15, 20, 65, 0, 0, 0, 110, 60, 25, false, 100
UNION ALL
SELECT 'Strasbourg', 'Paris', '2023-01-19 18:00:00', '2023-01-19 20:00:00', 100, 15, 20, 65, 0, 0, 0, 110, 60, 25, false, 100
UNION ALL
SELECT 'Lyon', 'Paris', '2023-01-19 08:00:00', '2023-01-19 10:00:00', 100, 15, 20, 65, 0, 0, 0, 110, 60, 25, false, 100
UNION ALL
SELECT 'Marseille', 'Nice', '2023-01-23 08:00:00', '2023-01-23 12:00:00', 100, 15, 20, 65, 0, 0, 0, 110, 60, 25, false, 100
UNION ALL
SELECT 'Paris', 'Bordeaux', '2023-01-25 15:00:00', '2023-01-25 17:00:00', 100, 15, 20, 65, 0, 0, 0, 110, 60, 25, false, 100
UNION ALL
SELECT 'Lille', 'Strasbourg', '2023-01-26 08:00:00', '2023-01-26 10:00:00', 100, 15, 20, 65, 0, 0, 0, 110, 60, 25, false, 100
UNION ALL
SELECT 'Nice', 'Lyon', '2023-01-27 14:00:00', '2023-01-27 16:00:00', 100, 15, 20, 65, 0, 0, 0, 110, 60, 25, false, 100
UNION ALL
SELECT 'Bordeaux', 'Marseille', '2023-01-19 08:00:00', '2023-01-19 12:00:00', 100, 15, 20, 65, 0, 0, 0, 110, 60, 25, false, 100
UNION ALL
SELECT 'Strasbourg', 'Paris', '2023-01-19 14:00:00', '2023-01-19 16:00:00', 100, 15, 20, 65, 0, 0, 0, 110, 60, 25, false, 100
;
-- Trigger to decrease the number of available seats when a reservation is made
DELIMITER //
CREATE TRIGGER decrease_available_seats
AFTER INSERT ON reservations
FOR EACH ROW
BEGIN
	IF NEW.class = 1 THEN
		UPDATE trains SET current_nb_class_1 = current_nb_class_1 + 1, available_seats = available_seats - 1 WHERE id = NEW.id_train;
	ELSEIF NEW.class = 2 THEN
		UPDATE trains SET current_nb_class_2 = current_nb_class_2 + 1, available_seats = available_seats - 1 WHERE id = NEW.id_train;
	ELSEIF NEW.class = 3 THEN
		UPDATE trains SET current_nb_class_3 = current_nb_class_3 + 1, available_seats = available_seats - 1 WHERE id = NEW.id_train;
	END IF;
END;


-- -- Trigger to increase the number of available seats when a reservation is deleted
CREATE TRIGGER increase_available_seats
AFTER DELETE ON reservations
FOR EACH ROW
BEGIN
	IF OLD.class = 1 THEN
		UPDATE trains SET current_nb_class_1 = current_nb_class_1 - 1, available_seats = available_seats + 1 WHERE id = OLD.id_train;
	ELSEIF OLD.class = 2 THEN
		UPDATE trains SET current_nb_class_2 = current_nb_class_2 - 1, available_seats = available_seats + 1 WHERE id = OLD.id_train;
	ELSEIF OLD.class = 3 THEN
		UPDATE trains SET current_nb_class_3 = current_nb_class_3 - 1, available_seats = available_seats + 1 WHERE id = OLD.id_train;
	END IF;
END;


-- -- Trigger to set the complete field to true when all the seats are booked
CREATE TRIGGER set_complete
AFTER UPDATE ON trains
FOR EACH ROW
BEGIN
	IF NEW.available_seats = 0 THEN
		UPDATE trains SET complete = true WHERE id = NEW.id;
	END IF;
END;
DELIMITER ; 
