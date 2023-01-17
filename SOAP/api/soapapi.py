from pysimplesoap.server import SoapDispatcher, SOAPHandler, WSGISOAPHandler
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import socket
import sys

ip = "projetws-api-1"
port = "5000"

dispatcher = SoapDispatcher(
'TransServer',
location = "http://127.0.0.1:8050/",
action = 'http://127.0.0.1:8050/', # SOAPAction
namespace = "http://example.com/sample.wsdl", prefix="ns0",
trace = True,
ns = True)


# get all the trains function and registering
def getalltrains():
		# Get request to the API
		response = requests.get("http://" + ip + ":" + port + "/trains/available")
		return {'statusCode':response.status_code,'trainsJson':response.text}

dispatcher.register_function('GetAllTrains', getalltrains,
		returns={
			'statusCode': int,
			'trainsJson': {},
		},
		args={})


# get trains by date function and registering
def gettrainsbydate(date):
		# Get request to the API
		response = requests.get("http://" + ip + ":" + port + "/trains/departures/" + date)
		return {'statusCode':response.status_code,'trainsJson':response}

dispatcher.register_function('GetTrainsByDate', gettrainsbydate,
		returns={
			'statusCode': int,
			'trainsJson': str,
		},
		args={'date': str})

# get trains by id function 
def gettrainsbyid(id):
		# Get request to the API
		response = requests.get("http://" + ip + ":" + port + "/trains/id/" + id)
		return {'statusCode':response.status_code,'trainsJson':response.text}

dispatcher.register_function('GetTrainsById', gettrainsbyid,
		returns={
			'statusCode': int,
			'trainsJson': str,
		},
		args={'id': str})

# get trains with exhaustive search function and registering

def gettrainssearch(departureStation, arrivalStation, departureDate, arrivalDate, passClass, nbTickets):
		# Get request to the API, params are in snake case
		response = requests.get("http://" + ip + ":" + port + "/trains/search", params={
			'departure_station': departureStation,
			'arrival_station': arrivalStation,
			'departure_date': departureDate,
			'arrival_date': arrivalDate,
			'passenger_class': passClass,
			'nb_tickets': nbTickets
		})

		return {'statusCode':response.status_code,'trainsJson':response.text}

dispatcher.register_function('GetTrainsSearch', gettrainssearch,
		returns={
			'statusCode': int,
			'trainsJson': str,
		},
		args={
			'departureStation': str,
			'arrivalStation': str,
			'departureDate': str,
			'arrivalDate': str,
			'passClass': int,
			'nbTickets': int
		})

# get booking with a user

def getbookinguser(firstName, lastName):
		# Get request to the API, params are in snake case
		response = requests.get("http://" + ip + ":" + port + "/trains/search/user/"+str(firstName)+"-"+str(lastName))

		return {'statusCode':response.status_code,'bookingJson':response.text}

dispatcher.register_function('GetBookingUser', getbookinguser,
		returns={
			'statusCode': int,
			'bookingJson': str,
		},
		args={
			'firstName': str,
			'lastName': str,
		})

# cancel a booking with its id

def cancelbooking(id):
		# Get request to the API
		response = requests.delete("http://" + ip + ":" + port + "/trains/cancel/"+str(id))

		return {'statusCode':response.status_code}

dispatcher.register_function('CancelBooking', cancelbooking,
		returns={
			'statusCode': int
		},
		args={
			'id': str,
		})


# book train function and registering

def booktrain(firstName, lastName, trainId, passClass):
		# Get request to the API
		response = requests.post("http://" + ip + ":" + port + "/trains/book", json={
			"1": {
				'first_name': firstName,
				'last_name': lastName,
				'id_train': str(trainId),
				'class': str(passClass),
			}
			})

		return {'statusCode':response.status_code,'bookingResponse':response.text}

dispatcher.register_function('BookTrain', booktrain,
		returns={
			'statusCode': int,
			'bookingResponse': str,
		},
		args={
			'firstName': str,
			'lastName': str,
			'trainId': int,
			'passClass': int,
		})


class MySOAPHandler(SOAPHandler):
	def do_OPTIONS(self):
		self.send_response(200)       
		# Echo back origin field
		self.send_header('Access-Control-Allow-Origin', self.headers['Origin'])
		self.send_header('Access-Control-Allow-Credentials', 'true')

		# Echo back Access Control Request headers
		self.send_header('Access-Control-Allow-Headers', self.headers['Access-Control-Request-Headers'])

		self.send_header("Access-Control-Max-Age", "1")
		self.end_headers()
	
	def do_POST(self):
		self.send_response(200)
		self.send_header('Access-Control-Allow-Origin', self.headers['Origin'])
		self.end_headers()

		SOAPHandler.do_POST(self)
		

print("Starting server...")
httpd = HTTPServer(("", 8050), MySOAPHandler)
httpd.dispatcher = dispatcher
httpd.serve_forever()