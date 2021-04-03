from flask import Flask, request, make_response, jsonify,render_template,session
from flask_cors import CORS
from flask_pymongo import pymongo
import requests,json,os
from pages_handlers import *

app = Flask(__name__)
app.secret_key='appsecretkey'
CORS(app)



@app.route('/webhook', methods=['POST'])
def webhook():
    main_request = request.get_json(force=True)
    tag=main_request.get('fulfillmentInfo').get('tag')
    # print(main_request)
    if tag == 'zip-code':
        return page_zip_code(main_request)

    if tag == 'zip-code-no-match':
        return page_zip_code_no_match(main_request)

    elif tag == 'name-first':
        return page_name_first(main_request)

    elif tag == 'name-last':
        return page_name_last(main_request)

    elif tag == 'name-middle':
        return page_name_middle(main_request)

    elif tag == 'born-date':
        return page_born_date(main_request)

    elif tag == 'street-address':
        return page_street_address(main_request)

    elif tag == 'state':
        return page_state(main_request)

    elif tag == 'city':
        return page_city(main_request)

    elif tag == 'vin-question':
        return yes_no(main_request)

    elif tag == 'vin-number-yes':
        return page_vin_question_yes(main_request)

    elif tag == 'vin-number-no':
        return page_vin_question_no(main_request)

    elif tag == 'vin-number':
        return page_vin_number(main_request)

    elif tag == 'car-year':
        return page_car_year(main_request)

    elif tag == 'makes-list':
        return makes_list(main_request)

    elif tag == 'car-make':
        return page_car_make(main_request)

    elif tag == 'models-list':
        return models_list(main_request)

    elif tag == 'car-model':
        return page_car_model(main_request)

    elif tag == 'primary-list':
        return primary_list(main_request)

    elif tag == 'car-primary-use':
        return page_car_primary_use(main_request)

    elif tag == 'car-ride-sharing-question':
        return yes_no(main_request)

    elif tag == 'car-ride-sharing-yes':
        return page_car_ride_sharing_yes(main_request)

    elif tag == 'car-ride-sharing-no':
        return page_car_ride_sharing_no(main_request)

    elif tag == 'car-miles-work-school':
        return page_car_miles_work_school(main_request)

    elif tag == 'car-annual-mileage':
        return page_car_annual_mileage(main_request)

    elif tag == 'car-own-finance':
        return page_car_own_finance(main_request)

    elif tag == 'car-tracking-device-yes':
        return page_car_tracking_device_yes(main_request)

    elif tag == 'car-tracking-device-no':
        return page_car_tracking_device_no(main_request)

    elif tag == 'gender':
        return page_gender(main_request)

    elif tag == 'marital-status':
        return page_marital_status(main_request)

    elif tag == 'education-level':
        return page_education_level(main_request)

    elif tag == 'employment-status-employed':
        return page_employment_status_employed(main_request)

    elif tag == 'employment-status':
        return page_employment_status(main_request)

    elif tag == 'occupation':
        return page_occupation(main_request)

    elif tag == 'social-security-number':
        return page_social_security_number(main_request)

    elif tag == 'primary-residence':
        return page_primary_residence(main_request)

    elif tag == 'residence-status':
        return page_residence_status(main_request)

    elif tag == 'driver-license-yes':
        return page_driver_license_yes(main_request)

    elif tag == 'driver-license-no':
        return page_driver_license_no(main_request)

    elif tag == 'license-age':
        return page_license_age(main_request)

    elif tag == 'license-status-yes':
        return page_license_status_yes(main_request)

    elif tag == 'license-status-no':
        return page_license_status_no(main_request)

    elif tag == 'driver-accidents-yes':
        return page_driver_accidents_yes(main_request)

    elif tag == 'driver-accidents-no':
        return page_driver_accidents_no(main_request)

    elif tag == 'incident-description':
        return page_incident_description(main_request)

    elif tag == 'incident-date':
        return page_incident_date(main_request)

    elif tag == 'dui-dwi-yes':
        return page_dui_dwi_yes(main_request)

    elif tag == 'dui-dwi-no':
        return page_dui_dwi_no(main_request)

    elif tag == 'dui-dwi-incident-date':
        return page_dui_dwi_incident_date(main_request)

    elif tag == 'driver-violations':
        return page_driver_violations(main_request)

    elif tag == 'driver-violations-yes':
        return page_driver_violations_yes(main_request)

    elif tag == 'driver-violations-no':
        return page_driver_violations_no(main_request)

    elif tag == 'add-another-driver-yes':
        return page_add_another_driver_yes(main_request)

    elif tag == 'add-another-driver-no':
        return page_add_another_driver_no(main_request)

    elif tag == 'insurance-last-3-years-yes':
        return page_insurance_last_3_years_yes(main_request)

    elif tag == 'insurance-last-3-years-no':
        return page_insurance_last_3_years_no(main_request)

    elif tag == 'body-injury-limits':
        return page_body_injury_limits(main_request)

    elif tag == 'motorist-coverage':
        return page_motorist_coverage(main_request)

    elif tag == 'medical-payments-coverage':
        return page_medical_payments_coverage(main_request)

    elif tag == 'domain':
        return page_domain(main_request)

    elif tag == 'email':
        return page_email(main_request)

    elif tag == 'email-spelling':
        return page_email_spelling(main_request)

    elif tag == 'phone-number':
        return page_phone_number(main_request)

    elif tag == 'autodialed-yes':
        return page_autodialed_yes(main_request)

    elif tag == 'autodialed-no':
        return page_autodialed_no(main_request)

    elif tag == 'license-state':
        return page_license_state(main_request)

    elif tag == 'license-number':
        return page_license_number(main_request)

    elif tag == 'policy-start':
        return page_policy_start(main_request)

    elif tag == 'national-origin':
        return page_national_origin(main_request)

    elif tag == 'monthly-pay':
        return page_monthly_pay(main_request)

    elif tag == 'credit-card-number':
        return page_credit_card_number(main_request)

@app.route('/messenger')
def messenger():
    return render_template('messenger.html')


@app.route('/db_login', methods=['POST'])
def login():
    cred = request.json
    # print(cred)
    user = cred['username']
    password = cred['password']
    dbname = "robo_agent_db"
    dbstring = "mongodb+srv://" + user + ':' + password + "@cluster0.kmuyv.mongodb.net/" + dbname + "?retryWrites=true&w=majority"
    try:
        client = pymongo.MongoClient(dbstring)
        db = client.get_database(dbname)
        records = db.robo_agent_db_c
        app.config["records"] = records
        # print(get_all_instances())
        return jsonify({'result': 'logged'})
    except :
        return jsonify({'result': 'failed'})

@app.route('/db_get_all')
def get_all_instances():
    try:
        login_check()
        records = app.config["records"]
    except:
        return jsonify({"result": 'not logged'})

    instance_cursor = records.find({})
    instances = []
    for instance in instance_cursor:
        id = instance['_id']
        del instance['_id']
        instance["_id"] = str(id)
        instances.append(instance)
    return jsonify({"result": instances})

@app.route('/db_delete')
def delete_instances():
    try:
        login_check()
        records = app.config["records"]
    except:
        return jsonify({"result": 'not logged'})

    result = records.delete_many({})
    return jsonify({"deleted_count":result.deleted_count})

@app.route('/db_replace', methods=["POST"])
def replace_instance():
    try:
        login_check()
        records = app.config["records"]
    except:
        return jsonify({"result": 'not logged'})
    data = request.json
    # print(data)
    id={"_id":data["_id"]}
    answers_cursor = records.replace_one(id,data,upsert=True)
    result =answers_cursor.raw_result["updatedExisting"]
    return jsonify({"results":result})



@app.route('/db_save', methods=['POST'])
def save_mongodb():
    try:
        login_check()
        records = app.config["records"]
        # print(get_all_instances())
    except:
        return jsonify({"result": 'not logged'})
    instance = request.json
    # print(instance)
    # try:
    records.insert_one(instance)
    return jsonify({'result': 'added'})
    # except:
    #     return jsonify({'result': 'error'})

def login_check(user="patrickjcross",password="Patrick1"):
    try:
        records = app.config["records"]
    except:
        dbname = "robo_agent_db"
        dbstring = "mongodb+srv://" + user + ':' + password + "@cluster0.kmuyv.mongodb.net/" + dbname + "?retryWrites=true&w=majority"
        client = pymongo.MongoClient(dbstring)
        db = client.get_database(dbname)
        records = db.robo_agent_db_c
        # print(records.find({}))
        app.config["records"] = records
        # print(get_all_instances())



if __name__ == '__main__':
    # session['data']={}
    app.run(debug=True,threaded=True)
