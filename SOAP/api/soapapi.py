from pysimplesoap.server import SoapDispatcher, SOAPHandler, WSGISOAPHandler
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

ip = "192.168.1.28"
port = "5000"

dispatcher = SoapDispatcher(
'TransServer',
location = "http://127.0.0.1:8050/",
action = 'http://127.0.0.1:8050/', # SOAPAction
namespace = "http://example.com/sample.wsdl", prefix="ns0",
trace = True,
ns = True)

#Function
def settransactiondetails(sessionId,msisdn,amount,language):
		#Some Code here
		#And more code here
		sid = "test"
		return {'sessionId':sid,'responseCode':0}

# register the user function
dispatcher.register_function('InitiateTransfer', settransactiondetails,
    returns={'sessionId': str,'responseCode':int}, 
    args={'sessionId': str,'msisdn': str,'amount': str,'language': str})


# get all the trains function and registering
def getalltrains():
		# Get request to the API
		response = requests.get("http://" + ip + ":" + port + "/trains/available")
		return {'statusCode':response.status_code,'trainsJson':response.text}

dispatcher.register_function('GetAllTrains', getalltrains,
		returns={
			'statusCode': int,
			'trainsJson': str,
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

print("Starting server...")
httpd = HTTPServer(("", 8050), SOAPHandler)
httpd.dispatcher = dispatcher
httpd.serve_forever()