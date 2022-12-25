from flask import Flask,request
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
        myresult.append({'id':r[0],'departure_station':r[1],'arrival_station':r[2],'departure_date':r[3],'arrival_date':r[4],'total_seats':r[5],'nb_class_1':r[6],'nb_class_2':r[7],'nb_class_3':r[8]})
    return myresult

mydb = mysql.connector.connect(
    host="db",
    user="root",
    password="root",
    database="streetworkout"
)

# faire quelque chose d'utile avec la connexion


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)