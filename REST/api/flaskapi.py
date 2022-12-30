from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import mysql.connector
import sys
import os
import json
import base64

app = Flask(__name__)
cors = CORS(app)
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
	data = request.get_json()

	# On vérifie si le train est complet
	mycursor = mydb.cursor()
	mycursor.execute("SELECT * FROM trains WHERE id = %s", (data['id'], ))
	train = mycursor.fetchone()
	
	# Si la classe demandée est pleine, on renvoie une erreur
	if train[8+int(data['class'])] == train[5+int(data['class'])]:
		return "Le train n°" + str(data['id']) + " est complet pour la classe " + str(data['class']) + ".", 400

	mycursor = mydb.cursor()
	query = "UPDATE trains SET current_nb_class_" + data['class'] + " = current_nb_class_" + data['class'] + " + 1 WHERE id = " + data['id'] + " AND current_nb_class_" + data['class'] + " < nb_class_" + data['class']
	mycursor.execute(query)
	mydb.commit()




	mycursor = mydb.cursor()
	query = "SELECT price_class_" + data['class'] + " FROM trains WHERE id = " + data['id']
	mycursor.execute(query)
	price = mycursor.fetchone()[0]

	

	return "Billet pour le train n°" + data['id'] + " réservé pour la classe " + data['class'] + " au prix de " + str(price) + " €."
	


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


# faire quelque chose d'utile avec la connexion

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)