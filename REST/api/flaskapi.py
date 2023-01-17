from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import mysql.connector
import sys
import os
import json
import base64

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/")
def hello_world():
    return {"helloString":"Hello, World"}

@app.route("/trains",methods=['GET'])
@cross_origin()
def get_trains():
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM trains")
  myresult = []
  for r in mycursor.fetchall():
      myresult.append(
			{
				'id':r[0],
				'departure_station':r[1],
				'arrival_station':r[2],
				'departure_date':r[3],
				'arrival_date':r[4],
				'total_seats':r[5],
				'nb_class_1':r[6],
				'nb_class_2':r[7],
				'nb_class_3':r[8],
				'current_nb_class_1':r[9],
				'current_nb_class_2':r[10],
				'current_nb_class_3':r[11],
				'price_class_1':r[12],
				'price_class_2':r[13],
				'price_class_3':r[14],
				'completed':r[15],
				'available_seats':r[16]
			})

  return myresult

mydb = mysql.connector.connect(
  host="db",
  user="root",
  password="root",
  database="trains"
)

# Route basée sur l'ID du train
@app.route("/trains/<id>",methods=['GET'])
@cross_origin()
def get_train(id):
	mycursor = mydb.cursor()
	mycursor.execute("SELECT * FROM trains WHERE id = %s", (id,))
	myresult = mycursor.fetchone()
	return {
		'id':myresult[0],
		'departure_station':myresult[1],
		'arrival_station':myresult[2],
		'departure_date':myresult[3],
		'arrival_date':myresult[4],
		'total_seats':myresult[5],
		'nb_class_1':myresult[6],
		'nb_class_2':myresult[7],
		'nb_class_3':myresult[8],
		'current_nb_class_1':myresult[9],
		'current_nb_class_2':myresult[10],
		'current_nb_class_3':myresult[11],
		'price_class_1':myresult[12],
		'price_class_2':myresult[13],
		'price_class_3':myresult[14],
		'completed':myresult[15],
		'available_seats':myresult[16]
	}

# Route basée sur le départ, sous format heure, jour, mois
@app.route("/trains/departures/<departure>",methods=['GET'])
@cross_origin()
def get_train_departure(departure):
	mycursor = mydb.cursor()
	mycursor.execute("SELECT * FROM trains WHERE DATEDIFF(departure_date, %s) BETWEEN -1 AND 1", (departure,))
	myresult = []

	for r in mycursor.fetchall():
		myresult.append(
			{
				'id':r[0],
				'departure_station':r[1],
				'arrival_station':r[2],
				'departure_date':r[3],
				'arrival_date':r[4],
				'total_seats':r[5],
				'nb_class_1':r[6],
				'nb_class_2':r[7],
				'nb_class_3':r[8],
				'current_nb_class_1':r[9],
				'current_nb_class_2':r[10],
				'current_nb_class_3':r[11],
				'price_class_1':r[12],
				'price_class_2':r[13],
				'price_class_3':r[14],
				'completed':r[15],
				'available_seats':r[16]
			})

	return myresult

# Route basée sur l'arrivée, sous format année, mois, jour, heure
@app.route("/trains/arrivals/<arrival>",methods=['GET'])
@cross_origin()
def get_train_arrival(arrival):
	mycursor = mydb.cursor()
	mycursor.execute("SELECT * FROM trains WHERE DATEDIFF(arrival_date, %s) BETWEEN -1 AND 1", (arrival,))
	myresult = []
	for r in mycursor.fetchall():
		myresult.append(
			{
				'id':r[0],
				'departure_station':r[1],
				'arrival_station':r[2],
				'departure_date':r[3],
				'arrival_date':r[4],
				'total_seats':r[5],
				'nb_class_1':r[6],
				'nb_class_2':r[7],
				'nb_class_3':r[8],
				'current_nb_class_1':r[9],
				'current_nb_class_2':r[10],
				'current_nb_class_3':r[11],
				'price_class_1':r[12],
				'price_class_2':r[13],
				'price_class_3':r[14],
				'completed':r[15],
				'available_seats':r[16]
			})

	return myresult


# Route basée sur une période de temps, à partir d'une date, sous format heure, jour, mois
@app.route("/trains/period/<period>",methods=['GET'])
@cross_origin()
def get_train_period(period):
	date = period.split('-')
	year = date[0]
	month = date[1]
	day = date[2]
	mycursor = mydb.cursor()
	mycursor.execute("SELECT * FROM trains WHERE YEAR(departure_date) = %s AND MONTH(departure_date) = %s AND DAY(departure_date) = %s", (year,month,day))
	myresult = []
	for r in mycursor.fetchall():
		myresult.append(
			{
				'id':r[0],
				'departure_station':r[1],
				'arrival_station':r[2],
				'departure_date':r[3],
				'arrival_date':r[4],
				'total_seats':r[5],
				'nb_class_1':r[6],
				'nb_class_2':r[7],
				'nb_class_3':r[8],
				'current_nb_class_1':r[9],
				'current_nb_class_2':r[10],
				'current_nb_class_3':r[11],
				'price_class_1':r[12],
				'price_class_2':r[13],
				'price_class_3':r[14],
				'completed':r[15],
				'available_seats':r[16]
			})

	return myresult

# Route basée sur deux stations, départ et arrivée

@app.route("/trains/stations/",methods=['GET'])
def get_train_stations():
	departure = request.args.get('departure')
	arrival = request.args.get('arrival')
	mycursor = mydb.cursor()
	mycursor.execute("SELECT * FROM trains WHERE departure_station = %s AND arrival_station = %s", (departure,arrival))
	myresult = []
	for r in mycursor.fetchall():
		myresult.append(
			{
				'id':r[0],
				'departure_station':r[1],
				'arrival_station':r[2],
				'departure_date':r[3],
				'arrival_date':r[4],
				'total_seats':r[5],
				'nb_class_1':r[6],
				'nb_class_2':r[7],
				'nb_class_3':r[8],
				'current_nb_class_1':r[9],
				'current_nb_class_2':r[10],
				'current_nb_class_3':r[11],
				'price_class_1':r[12],
				'price_class_2':r[13],
				'price_class_3':r[14],
				'completed':r[15],
				'available_seats':r[16]
			})

	return myresult

# Route donnant les trains encore disponibles

@app.route("/trains/available",methods=['GET'])
def get_train_available():
	mycursor = mydb.cursor()
	# TODO : Ajouter la condition sur la date de départ
	# mycursor.execute("SELECT * FROM trains WHERE available_seats > 0 AND departure_date > NOW()")
	mycursor.execute("SELECT * FROM trains WHERE available_seats > 0")
	myresult = []
	for r in mycursor.fetchall():
		myresult.append(
			{
				'id':r[0],
				'departure_station':r[1],
				'arrival_station':r[2],
				'departure_date':r[3],
				'arrival_date':r[4],
				'total_seats':r[5],
				'nb_class_1':r[6],
				'nb_class_2':r[7],
				'nb_class_3':r[8],
				'current_nb_class_1':r[9],
				'current_nb_class_2':r[10],
				'current_nb_class_3':r[11],
				'price_class_1':r[12],
				'price_class_2':r[13],
				'price_class_3':r[14],
				'completed':r[15],
				'available_seats':r[16]
			})

	return myresult

# Route donnant les trains au prix compris entre deux valeurs, pour une classe donnée
@app.route("/trains/prices/",methods=['GET'])
def get_train_prices():
	minimum = request.args.get('min')
	maximum = request.args.get('max')
	passenger_class = request.args.get('class')

	mycursor = mydb.cursor()
	query = "SELECT * FROM trains WHERE price_class_" + passenger_class + " BETWEEN " + minimum + " AND " + maximum
	mycursor.execute(query)
	myresult = []
	for r in mycursor.fetchall():
		myresult.append(
			{
				'id':r[0],
				'departure_station':r[1],
				'arrival_station':r[2],
				'departure_date':r[3],
				'arrival_date':r[4],
				'total_seats':r[5],
				'nb_class_1':r[6],
				'nb_class_2':r[7],
				'nb_class_3':r[8],
				'current_nb_class_1':r[9],
				'current_nb_class_2':r[10],
				'current_nb_class_3':r[11],
				'price_class_1':r[12],
				'price_class_2':r[13],
				'price_class_3':r[14],
				'completed':r[15],
				'available_seats':r[16]
			})

	return myresult
	

# Route qui permet de réserver un billet, incrémentant le nombre de places réservées pour la classe donnée
@app.route("/trains/book",methods=['POST'])
def book_train():
	# JSON contains several JSON objects, with first_name, last_name, id_train, class
	data = request.get_json()

	# On vérifie si le train a assez de places pour le nombre de personnes demandées et la classe

	numTrains = len(data)
	print(numTrains, file=sys.stderr)

	# On ajoute toutes les réservations

	for trainJson in data:
		# On vérifie si le train est complet avec numTrains
		mycursor = mydb.cursor()
		mycursor.execute("SELECT * FROM trains WHERE id = %s", (data[trainJson]['id_train'], ))
		train = mycursor.fetchone()

		# utiliser la colonne current_nb_class_1, current_nb_class_2, current_nb_class_3 selon la classe demandée

		if train[9] + numTrains > train[6] and data[trainJson]['class'] == '1':
			return "Le train n°" + str(data[trainJson]['id_train']) + " n'a pas assez de places en première classe.", 400
		elif train[10] + numTrains > train[7] and data[trainJson]['class'] == '2':
			return "Le train n°" + str(data[trainJson]['id_train']) + " n'a pas assez de places en deuxième classe.", 400
		elif train[11] + numTrains > train[8] and data[trainJson]['class'] == '3':
			return "Le train n°" + str(data[trainJson]['id_train']) + " n'a pas assez de places en troisième classe.", 400


		mycursor = mydb.cursor()
		query = "INSERT INTO reservations (first_name, last_name, id_train, class) VALUES (%s, %s, %s, %s)"
		val = (data[trainJson]['first_name'], data[trainJson]['last_name'], data[trainJson]['id_train'], data[trainJson]['class'])
		mycursor.execute(query, val)
		mydb.commit()

	return "Réservation de " + str(numTrains) + " billets pour le train n°" + str(data[trainJson]['id_train']) + " effectuée avec succès.", 200


# Route donnant les trains complets

@app.route("/trains/full",methods=['GET'])
def get_train_full():
	mycursor = mydb.cursor()
	mycursor.execute("SELECT * FROM trains WHERE available_seats = 0")
	myresult = []
	for r in mycursor.fetchall():
		myresult.append(
			{
				'id':r[0],
				'departure_station':r[1],
				'arrival_station':r[2],
				'departure_date':r[3],
				'arrival_date':r[4],
				'total_seats':r[5],
				'nb_class_1':r[6],
				'nb_class_2':r[7],
				'nb_class_3':r[8],
				'current_nb_class_1':r[9],
				'current_nb_class_2':r[10],
				'current_nb_class_3':r[11],
				'price_class_1':r[12],
				'price_class_2':r[13],
				'price_class_3':r[14],
				'completed':r[15],
				'available_seats':r[16]
			})

	return myresult

# Route donnant les réservations d'un utilisateur

@app.route("/trains/book/<id>",methods=['GET'])
def get_user_bookings(id):
	mycursor = mydb.cursor()
	mycursor.execute("SELECT * FROM bookings WHERE user_id = %s", (id, ))
	myresult = []
	for r in mycursor.fetchall():
		myresult.append(
			{
				'id':r[0],
				'first_name':r[1],
				'last_name':r[2],
				'id_train':r[3],
				'class':r[4],
			})

	return myresult

# Route permettant de faire une recherche avec tous les critères
# Départ, arrivée, date de départ, date d'arrivée, classe, nombres de tickets à réserver

@app.route("/trains/search",methods=['GET'])
def search_train():
	departure_station = request.args.get('departure_station')
	arrival_station = request.args.get('arrival_station')
	departure_date = request.args.get('departure_date')
	arrival_date = request.args.get('arrival_date')
	passenger_class = request.args.get('passenger_class')
	nb_tickets = request.args.get('nb_tickets')

	mycursor = mydb.cursor()
	# Dates are in the format YYYY-MM-DD HH:MM:SS, but we only need the date part
	query = "SELECT * FROM trains WHERE departure_station = '" + departure_station + "' AND arrival_station = '" + arrival_station + "' \
	AND departure_date LIKE '" + departure_date + "%' AND arrival_date LIKE '" + arrival_date + "%' \
	AND nb_class_" + passenger_class + " >= " + nb_tickets + " AND available_seats >= " + nb_tickets

	mycursor.execute(query)
	myresult = []
	for r in mycursor.fetchall():
		myresult.append(
			{
				'id':r[0],
				'departure_station':r[1],
				'arrival_station':r[2],
				'departure_date':r[3],
				'arrival_date':r[4],
				'total_seats':r[5],
				'nb_class_1':r[6],
				'nb_class_2':r[7],
				'nb_class_3':r[8],
				'current_nb_class_1':r[9],
				'current_nb_class_2':r[10],
				'current_nb_class_3':r[11],
				'price_class_1':r[12],
				'price_class_2':r[13],
				'price_class_3':r[14],
				'completed':r[15],
				'available_seats':r[16]
			})

	return myresult

# Route permettant de faire une recherche avec tous les critères
# Départ, arrivée, date de départ, date d'arrivée, classe, nombres de tickets à réserver

@app.route("/trains/search/user/<user>",methods=['GET'])
def search_train_user(user):
	user_split = user.split('-')
	name = user_split[0]
	last_name = user_split[1]

	mycursor = mydb.cursor()
	# Dates are in the format YYYY-MM-DD HH:MM:SS, but we only need the date part
	query = "SELECT trains.id, departure_station, arrival_station, departure_date, arrival_date, class FROM trains JOIN reservations ON trains.id = reservations.id_train WHERE reservations.first_name = '"+name+"' AND reservations.last_name = '"+last_name+"';" 

	mycursor.execute(query)
	myresult = []
	for r in mycursor.fetchall():
		myresult.append(
			{
				'id':r[0],
				'departure_station':r[1],
				'arrival_station':r[2],
				'departure_date':r[3],
				'arrival_date':r[4],
				'class':r[5],
			})

	return myresult

# faire quelque chose d'utile avec la connexion

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)