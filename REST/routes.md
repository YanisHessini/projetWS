# Les routes disponibles par les services

## REST, via Flask

1. `GET /trains` : liste des trajets de trains dans la base de données
2. `GET /trains/<id>` : informations sur le trajet de train d'identifiant `<id>`
3. `GET /trains/departures/<departure>` : liste des trajets de trains partant de la gare `<departure>`
4. `GET /trains/arrivals/<arrival>` : liste des trajets de trains arrivant à la gare `<arrival>`
5. `GET /trains/period/<period>` : liste des trajets de trains partant au jour `<period>`
6. `GET /trains/stations/` : liste des trains passant par une gare de *départ* et *d'arrivée*
7. `GET /trains/available/` : liste des trains disponibles
8. `GET /trains/prices/` : liste des prix des trajets de trains
9. `POST /trains/book/` : réserver un trajet de train, avec un *ID* et une *classe*. 


## SOAP
