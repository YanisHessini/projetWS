from pysimplesoap.client import SoapClient
import json


wsdl_url = "http://127.0.0.1:8050/"
c = SoapClient(wsdl=wsdl_url, soap_ns='soap', trace=False)
# print(c.InitiateTransfer(sessionId="sid", msisdn="254722000000", amount="100", language="en"))

# response = c.GetAllTrains()
# print(response)

response = c.GetTrainsSearch(departureStation='Paris', 
														arrivalStation='Lille',
														departureDate='2023-01-02',
														arrivalDate='2023-01-02',
														passClass='1',
														nbTickets='1')

print(response)
