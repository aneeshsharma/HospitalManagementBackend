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


@app.route('/api/v1/resources/doctor/sign-up', methods=['POST'])
def api_doctor_sign_up():
    req_data = request.get_json()
    print(req_data)

    fields = ("department_no", "name", "address", "position")
    values = tuple([req_data[_] for _ in fields])
    if None in values:
        return "invalud data", 400

    fields_str = ', '.join(fields)

    query = f'INSERT INTO doctor ({fields_str}) VALUES {values}'
    print(query)
    try:
        cursor.execute(query)
    except Exception as e:
        print(e)
        return "invalid data", 400
    db.commit()
    return "done", 200


@app.route('/api/v1/resources/pharmacy/sign-up', methods=['POST'])
def api_pharmacy_sign_up():
    req_data = request.get_json()
    print(req_data)

    fields = ("department_no", "name", "contact")
    values = tuple([req_data[_] for _ in fields])
    if None in values:
        return "invalud data", 400

    fields_str = ', '.join(fields)

    query = f'INSERT INTO pharmacy ({fields_str}) VALUES {values}'
    print(query)
    try:
        cursor.execute(query)
    except Exception as e:
        print(e)
        return "invalid data", 400
    db.commit()
    return "done", 200


@app.route('/api/v1/resources/doctor/login', methods=['GET'])
def api_doctor_login():
    name = request.args.get('name')
    cursor.execute(f'SELECT doctor_id FROM doctor WHERE name="{name}"')
    row = cursor.fetchone()
    result = {
        'doctor_id': row[0],
    }
    return jsonify(result)


@app.route('/api/v1/resources/pharmacy/login', methods=['GET'])
def api_pharmacy_login():
    name = request.args.get('name')
    cursor.execute(f'SELECT pharmacy_id FROM pharmacy WHERE name="{name}"')
    row = cursor.fetchone()
    result = {
        'pharmacy_id': row[0],
    }
    return jsonify(result)


@app.route('/api/v1/resources/doctor/patient', methods=['POST', 'GET'])
def api_patient():
    if request.method == 'POST':
        req_data = request.get_json()
        print(req_data)

        fields = ("age", "name", "contact")
        values = tuple([req_data[_] for _ in fields])
        if None in values:
            print('Null value found')
            return "invalud data", 400

        fields_str = ', '.join(fields)

        query = f'INSERT INTO patient ({fields_str}) VALUES {values}'
        print(query)
        try:
            cursor.execute(query)
        except Exception as e:
            print(e)
            return "invalid data", 400
        db.commit()
        return "done", 200
    else:
        patient_id = request.args.get('patient_id')
        query = f'SELECT patient_id, age, name, contact FROM patient WHERE patient_id="{patient_id}"'
        if not patient_id:
            query = f'SELECT patient_id, age, name, contact FROM patient'
        print(query)
        try:
            cursor.execute(query)
        except Exception as e:
            print(e)
            return "Server Error", 500
        data = cursor.fetchall()
        result = []
        for row in data:
            result.append({
                'patient_id': row[0],
                'age': row[1],
                'name': row[2],
                'contact': row[3],
            })
        return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
