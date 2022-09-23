CREATE DATABASE IF NOT EXISTS trains;

USE trains;

create table IF NOT EXISTS reservations
(
    id      int auto_increment
        primary key,
    class_1 int not null,
    class_2 int not null,
    class_3 int not null
);

create table IF NOT EXISTS trains
(
    id                int auto_increment
        primary key,
    departure_station linestring null,
    arrival_station   linestring null,
    departure_date    datetime   null,
    arrival_date      datetime   null,
    total_seats       int        not null,
    nb_class_1        int        not null,
    nb_class_2        int        not null,
    nb_class_3        int        not null
);
