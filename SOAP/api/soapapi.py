from pysimplesoap.server import SoapDispatcher, SOAPHandler, WSGISOAPHandler
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

ip = "192.168.73.255"
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
		response = requests.get("http://" + ip + ":" + port + "/trains")
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
		return {'statusCode':response.status_code,'trainsJson':response.text}
		# return {'statusCode':response.status_code,'trainsJson':{"test":"test"}}

dispatcher.register_function('GetTrainsByDate', gettrainsbydate,
		returns={
			'statusCode': int,
			'trainsJson': str,
		},
		args={'date': str})



print("Starting server...")
httpd = HTTPServer(("", 8050), SOAPHandler)
httpd.dispatcher = dispatcher
httpd.serve_forever()