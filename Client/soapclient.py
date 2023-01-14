from pysimplesoap.client import SoapClient
import requests
import json

wsdl_url = "http://127.0.0.1:8050/"
c = SoapClient(wsdl=wsdl_url, soap_ns='soap', trace=False)
# print(c.InitiateTransfer(sessionId="sid", msisdn="254722000000", amount="100", language="en"))
response = c.GetAllTrains()
json_object = json.dumps(response, indent = 4)
print(json_object)