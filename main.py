import pymysql
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import time

from datetime import date

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")


def get_new_cursor():
    db = pymysql.connect(DB_HOST, DB_USER,
                         DB_PASS, DB_NAME)
    cursor = db.cursor()
    return db, cursor


db_, cur = get_new_cursor()

# execute SQL query using execute() method.
cur.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cur.fetchone()
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


@app.route('/api/v1/resources/common/getDepartment', methods=['GET'])
def api_getDepartments():
    db, cursor = get_new_cursor()
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
    db, cursor = get_new_cursor()
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
    db, cursor = get_new_cursor()
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
    db, cursor = get_new_cursor()
    name = request.args.get('name')
    cursor.execute(f'SELECT doctor_id FROM doctor WHERE name="{name}"')
    row = cursor.fetchone()
    result = {
        'doctor_id': row[0],
    }
    return jsonify(result)


@app.route('/api/v1/resources/pharmacy/login', methods=['GET'])
def api_pharmacy_login():
    db, cursor = get_new_cursor()
    name = request.args.get('name')
    cursor.execute(f'SELECT pharmacy_id FROM pharmacy WHERE name="{name}"')
    row = cursor.fetchone()
    result = {
        'pharmacy_id': row[0],
    }
    return jsonify(result)


@app.route('/api/v1/resources/doctor/patient', methods=['POST', 'GET'])
def api_patient():
    db, cursor = get_new_cursor()
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


@app.route('/api/v1/resources/common/drugs', methods=['POST', 'GET'])
def api_drugs():
    db, cursor = get_new_cursor()
    if request.method == 'POST':
        req_data = request.get_json()
        print(req_data)

        fields = ("drug_name", "class")
        values = tuple([req_data[_] for _ in fields])
        if None in values:
            print('Null value found')
            return "invalud data", 400

        fields_str = ', '.join(fields)

        query = f'INSERT INTO drugs ({fields_str}) VALUES {values}'
        print(query)
        try:
            cursor.execute(query)
        except Exception as e:
            print(e)
            return "invalid data", 400
        db.commit()
        return "done", 200
    else:
        drug_id = request.args.get('drug_id')
        query = f'SELECT drug_id, drug_name, class FROM drugs WHERE drug_id="{drug_id}"'
        if not drug_id:
            query = f'SELECT drug_id, drug_name, class FROM drugs'
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
                'drug_id': row[0],
                'drug_name': row[1],
                'class': row[2],
            })
        return jsonify(result)


@app.route('/api/v1/resources/doctor/treatment', methods=['POST', 'GET'])
def api_treatment():
    db, cursor = get_new_cursor()
    if request.method == 'POST':
        req_data = request.get_json()
        print(req_data)

        data = req_data

        data['treatment_date'] = str(date.today())
        data['treat_id'] = int(time.time() * 1000 -
                               (int(time.time() / 100000)) * 100000 * 1000)

        fields = ("treat_id", "patient_id", "doctor_id",
                  "treatment_date", "treatment_report")
        values = tuple([req_data[_] for _ in fields])
        if None in values:
            print('Null value found')
            return "invalud data", 400

        fields_str = ', '.join(fields)

        query = f'INSERT INTO treats ({fields_str}) VALUES {values}'
        print(query)
        try:
            r = cursor.execute(query)
            print(r)
        except Exception as e:
            print(e)
            return "invalid data", 400
        r = db.commit()
        print(r)
        return {'message': 'done', 'treat_id': data['treat_id']}, 200
    else:
        treat_id = request.args.get('treat_id')
        patient_id = request.args.get('patient_id')
        query = ''
        if treat_id:
            query = f'SELECT patient_id, doctor_id, treat_id, treatment_date, treatment_report FROM treats WHERE treat_id="{treat_id}"'
        elif patient_id:
            query = f'SELECT patient_id, doctor_id, treat_id, treatment_date, treatment_report FROM treats WHERE patient_id="{patient_id}"'
        else:
            query = f'SELECT patient_id, doctor_id, treat_id, treatment_date, treatment_report FROM treats'
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
                'doctor_id': row[1],
                'treat_id': row[2],
                'treatment_date': row[3],
                'treatment_report': row[4],
            })
        return jsonify(result)


@app.route('/api/v1/resources/doctor/prescription', methods=['POST', 'GET'])
def api_prescription():
    db, cursor = get_new_cursor()
    if request.method == 'POST':
        req_data = request.get_json()
        print(req_data)

        data = req_data

        drugs = data['drugs']

        for drug_id in drugs:
            insert_data = {
                'drug_id': drug_id,
                'doctor_id': data['doctor_id'],
                'patient_id': data['patient_id'],
                'treat_id': data['treat_id']
            }
            fields = ("drug_id", "patient_id", "doctor_id",
                      "treat_id")
            values = tuple([insert_data[_] for _ in fields])
            if None in values:
                print('Null value found')
                return "invalud data", 400

            fields_str = ', '.join(fields)

            query = f'INSERT INTO prescribed_by ({fields_str}) VALUES {values}'
            print(query)
            try:
                r = cursor.execute(query)
                print(r)
            except Exception as e:
                print(e)
                return "invalid data", 400
        db.commit()
        return "done", 200
    else:
        treat_id = request.args.get('treat_id')
        query = ''
        if treat_id:
            query = f'SELECT drug_id, doctor_id, patient_id, treat_id FROM prescribed_by WHERE treat_id="{treat_id}"'
        else:
            query = f'SELECT drug_id, doctor_id, patient_id, treat_id FROM prescribed_by'

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
                'drug_id': row[0],
                'doctor_id': row[1],
                'patient_id': row[2],
                'treat_id': row[3],
            })
        return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
