import pymysql
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")

db = pymysql.connect(DB_HOST, DB_USER,
                     DB_PASS, DB_NAME)
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print("Database version : %s " % data)

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    name = os.environ.get("NAME", "World")
    return "Hello {}!".format(name)


@app.route("/version")
def version():
    return "Version {}!".format(data)


@app.route('/api/v1/resources/doctor/getPatient', methods=['POST'])
def api_addPatient():
    if 'patientID' in request.args:
        patientID = int(request.args['id'])
    else:
        return "Error 404"
    patient = {"patientID": patientID}
    return jsonify(patient)


@app.route('/api/v1/resources/common/getDepartment', methods=['GET'])
def api_getDepartments():
    cursor.execute('SELECT department_name, department_no FROM department')
    data = cursor.fetchall()
    result = []
    for row in data:
        result.append({
            'department_name': row[0],
            'department_no': row[1],
        })
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
