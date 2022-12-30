# Les routes disponibles par les services

## REST, via Flask

1. `GET /trains` : liste des trajets de trains dans la base de données
2. `GET /trains/<id>` : informations sur le trajet de train d'identifiant `<id>`
3. `GET /trains/departures/<departure>` : liste des trajets de trains partant de la gare `<departure>`
4. `GET /trains/arrivals/<arrival>` : liste des trajets de trains arrivant à la gare `<arrival>`
5. `GET /trains/stations/<departure>&<arrival>` : liste des trajets de trains passant par les gares `<departure>` et `<arrival>`





## SOAP
