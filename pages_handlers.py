import requests,json,vinlib,us
from flask import Flask, request, make_response, jsonify
from responses import *
from helpers import *
import datetime

backend_URL="https://robo-agent.uc.r.appspot.com"
# backend_URL="https://af87d329529a.ngrok.io"


def page_zip_code(main_request):
    currentPage=main_request.get('pageInfo').get('currentPage')
    parameters=main_request.get('sessionInfo').get('parameters')
    zip_code = parameters.get('numbers')[0]

    if len(zip_code) == 5:
        return next(mongo_kv(main_request,'01-z',zip_code))
    else:
        return message(['Not valid USA zip code'],page=currentPage)

def page_zip_code_no_match(main_request):
    print(main_request)
    currentPage=main_request.get('pageInfo').get('currentPage')
    parameters=main_request.get('sessionInfo').get('parameters')
    zip_code = parameters.get('numbers')[0]
    if len(zip_code) == 5:
        return next(mongo_kv(main_request,'z',zip_code))
    else:
        return message(['Not valid USA zip code'],page=currentPage)


nist
def page_name_first(main_request):
    currentPage=main_request.get('pageInfo').get('currentPage')
    parameters=main_request.get('sessionInfo').get('parameters')
    name_first= parameters.get('name')[0]['name']
    return next(mongo_kv(main_request,'02-fn',name_first))

def page_name_last(main_request):
    currentPage=main_request.get('pageInfo').get('currentPage')
    parameters=main_request.get('sessionInfo').get('parameters')
    name_last= parameters.get('name')[0]['name']
    return next(mongo_kv(main_request,'03-ln',name_last))

def page_name_middle(main_request):
    currentPage=main_request.get('pageInfo').get('currentPage')
    parameters=main_request.get('sessionInfo').get('parameters')
    name_middle= parameters.get('letter')[0]
    return next(mongo_kv(main_request,'04-mn',name_middle))



def page_born_date(main_request):
    currentPage=main_request.get('pageInfo').get('currentPage')
    parameters=main_request.get('sessionInfo').get('parameters')
    born_date = parameters.get('born-date')[0]
    year = int(born_date["year"])
    born_date_formatted=datetime.date(year=int(born_date["year"]), month=int(born_date["month"]), day=int(born_date["day"]))
    if year > 2005:
        return message('you must be equal or more than 16 years old',page=currentPage)
    else:
        return next(mongo_kv(main_request,'05-bd',born_date_formatted.strftime('%m/%d/%Y')))

def page_street_address(main_request):
    currentPage=main_request.get('pageInfo').get('currentPage')
    parameters=main_request.get('sessionInfo').get('parameters')
    street_address= parameters.get('street-address')[0]
    return next(mongo_kv(main_request,'06-sa',street_address))

# mongodb_saved = parameters.get('mongodb_saved')
# mongodb_saved[""]=
# return next(mongodb_saved)
def page_state(main_request):
    currentPage=main_request.get('pageInfo').get('currentPage')
    parameters=main_request.get('sessionInfo').get('parameters')
    state = parameters.get('state')[0]
    if us.states.lookup(state) != None:
        state=us.states.lookup(state).abbr
        return next(mongo_kv(main_request,'07-st',state))

    else:
        return message('state name not true',page=currentPage)


def page_city(main_request):
    currentPage=main_request.get('pageInfo').get('currentPage')
    parameters=main_request.get('sessionInfo').get('parameters')
    city = parameters.get('city')[0]
    print(city)
    try:
        spoken_state=parameters.get('state')[0]
        spoken_state_abbr=us.states.lookup(spoken_state).abbr
        state_abbr = get_city_opendata(city)['region']

        if state_abbr == spoken_state_abbr:
            return next(mongo_kv(main_request, '08-c', city))
        else:
            return message('city not existed in State',page=currentPage)
    except:
        return message('city not existed in State', currentPage)

def yes_no(main_request):
    return chips(['yes','no'])


def page_vin_question_yes(main_request):
    print('page_vin_question_yes')
    return next(mongo_kv(main_request,'09-vin?',True))

def page_vin_question_no(main_request):
    print('page_vin_question_no')
    return next(mongo_kv(main_request,'09-vin?',False))

def page_vin_number(main_request):
    currentPage=main_request.get('pageInfo').get('currentPage')
    parameters=main_request.get('sessionInfo').get('parameters')
    vin = parameters.get('numbers-letters')[0]
    vin_validate=vinlib.check_vin(vin)
    if vin_validate:
        return next(mongo_kv(main_request,'10-vin',vin))

    else:
        return message('VIN not valid , please enter valid VIN',page=currentPage)


def page_car_year(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    car_year = parameters.get('year')[0]
    if int (car_year) < 1990:
        return message('only available cars which are produced after 1990',page=currentPage)
    else:
        return next(mongo_kv(main_request, '11-cy', car_year))

def makes_list(main_request):
    car_makes=get_available_makes()
    return chips(car_makes)

def page_car_make(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    car_make = parameters.get('car-make')[0]
    print ('car make is ',car_make)
    car_make=car_make.lower()
    if car_make in get_available_makes():
        return message(text='What is the model of your '+car_make+'?',mongodb_saved=mongo_kv(main_request, '12-cmk', car_make))
    else:
        return message('wrong car make',page=currentPage)


def models_list(main_request):
    parameters = main_request.get('sessionInfo').get('parameters')
    car_year = parameters.get('year')[0]
    car_make = parameters.get('car-make')[0]
    make_models=get_models_make_year(car_make,car_year)
    return chips(make_models)

def page_car_model(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    car_model = parameters.get('car-model')[0]
    car_year = parameters.get('year')[0]
    car_make = parameters.get('car-make')[0]
    car_model=car_model.lower()
    print('car model is ',car_model)
    make_models = get_models_make_year(car_make, car_year)
    if car_model in make_models:
        return next(mongo_kv(main_request, '13-cmo', car_model))
    else:
        return message('wrong car model.',page=currentPage)

def page_car_model_intent_no_match(main_request):
    print(main_request)
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    car_model = parameters.get('car-model')[0]
    car_year = parameters.get('year')[0]
    car_make = parameters.get('car-make')[0]
    print('car model is ',car_model)
    make_models = get_models_make_year(car_make, car_year)
    if car_model in make_models:

        return next()
    else:
        return message('wrong car model.',page=currentPage)


def primary_list(main_request):
    car_primary_list=['Personal','Business','Commercial','Farming']
    return chips(car_primary_list)

def page_car_primary_use(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    car_primary_use=parameters.get('car-primary-use')[0]
    return next(mongo_kv(main_request, '14-cpu', car_primary_use))

def page_car_ride_sharing_question(main_request):
    print('car_ride_sharing_question')
    return chips(['yes','no'])

def page_car_ride_sharing_yes(main_request):
    print('page_car_ride_sharing_yes')
    return next(mongo_kv(main_request, '15-rs', True))

def page_car_ride_sharing_no(main_request):
    print('page_car_ride_sharing_no')
    return next(mongo_kv(main_request, '15-rs', False))


def page_car_miles_work_school(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    car_miles_work_school = parameters.get('numbers-int')[0]
    return next(mongo_kv(main_request, '16-cmws', car_miles_work_school))

def page_car_annual_mileage(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    car_annual_mileage = parameters.get('numbers-int')[0]
    return next(mongo_kv(main_request, '17-cam', car_annual_mileage))


def page_car_own_finance(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    car_own_finance=parameters.get('car-own-finance')[0]
    print(car_own_finance)
    return next(mongo_kv(main_request, '18-cof', car_own_finance))

def page_car_tracking_device_yes(main_request):
    print('car-tracking-device-yes')
    return next(mongo_kv(main_request, '19-ctd', True))

def page_car_tracking_device_no(main_request):
    print('car-tracking-device-no')
    return next(mongo_kv(main_request, '19-ctd', False))

def page_gender(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    gender = parameters.get('gender')[0]
    return next(mongo_list(main_request,'drivers','20-g',gender))

def page_marital_status(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    marital_status = parameters.get('marital-status')[0]
    print(marital_status)
    return next(mongo_list(main_request,'drivers','21-ms',marital_status))

def page_education_level(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    education_level = parameters.get('education-level')[0]
    print(education_level)
    return next(mongo_list(main_request,'drivers','22-el',education_level))


def page_employment_status_employed(main_request):
    print('employed')
    return next(mongo_list(main_request,'drivers','23-es',"Employed"))

def page_employment_status(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    employment_status = parameters.get('employment-status')[0]
    print(employment_status)
    return next(mongo_list(main_request,'drivers','23-es',employment_status))

def page_occupation(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    occupation = parameters.get('occupation')[0]
    print(occupation)
    return next(mongo_list(main_request,'drivers','24-o',occupation))

def page_social_security_number(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    social_security_number = parameters.get('numbers')[0]
    print(social_security_number)
    if len(social_security_number) == 9:
        return next(mongo_list(main_request, 'drivers', '25-ssn', social_security_number))
    else:
        return message('social security number not valid',page=currentPage)

def page_primary_residence(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    primary_residence = parameters.get('primary-residence')[0]
    print(primary_residence)
    return next(mongo_list(main_request,'drivers','26-pr',primary_residence))

def page_residence_status(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    residence_status = parameters.get('residence-status')[0]
    print(residence_status)
    return next(mongo_list(main_request,'drivers','27-res',residence_status))

def page_driver_license_yes(main_request):
    print('driver-license-yes')
    return next(mongo_list(main_request,'drivers','28-dl',True))

def page_driver_license_no(main_request):
    print('driver-license-no')
    return next(mongo_list(main_request,'drivers','28-dl',False))

def page_license_age(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    license_age = parameters.get('numbers-int')[0]
    license_age=int(license_age)
    print(license_age,type(license_age),type(16))

    if license_age >= 16 and license_age <100:
        print('license age is ', license_age)
        return next(mongo_list(main_request, 'drivers', '29-la',license_age))
    else:
        return message('age must be between 16 and 99',page=currentPage)


def page_license_status_yes(main_request):
    print('license-status-yes')
    return next(mongo_list(main_request,'drivers','30-ls?',True))

def page_license_status_no(main_request):
    print('license-status-no')
    return next(mongo_list(main_request,'drivers','30-ls?',False))

def page_driver_accidents_yes(main_request):
    print('driver-accidents-yes')
    return next(mongo_list(main_request,'drivers','31-da',True))

def page_driver_accidents_no(main_request):
    print('driver-accidents-no')
    return next(mongo_list(main_request,'drivers','31-da',False))

def page_incident_description(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    incident_description = parameters.get('incident-description')[0]
    print(incident_description)
    return next(mongo_list(main_request,'drivers','32-ide',incident_description))

def page_incident_date(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    incident_date = parameters.get('incident-date')[0]
    print(incident_date)
    incident_date_formatted=datetime.date(year=int(incident_date["year"]), month=int(incident_date["month"]), day=int(incident_date["day"]))

    if incident_date_formatted <= datetime.date.today():
        return next(mongo_list(main_request, 'drivers', '33-ida',incident_date_formatted.strftime('%m/%d/%Y')))
    else:
        return message('date is not valid, make sure your date before today',page=currentPage)

def page_dui_dwi_yes(main_request):
    print('dui-dwi-yes')
    return next(mongo_list(main_request,'drivers','34-dd',True))

def page_dui_dwi_no(main_request):
    print('dui-dwi-no')
    return next(mongo_list(main_request,'drivers','34-dd',False))


def page_dui_dwi_incident_date(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    dui_dwi_incident_date = parameters.get('dui-dwi-incident-date')[0]
    print(dui_dwi_incident_date)
    dui_dwi_incident_date_formatted=datetime.date(year=int(dui_dwi_incident_date["year"]), month=int(dui_dwi_incident_date["month"]), day=int(dui_dwi_incident_date["day"]))

    if dui_dwi_incident_date_formatted < datetime.date.today():
        return next(mongo_list(main_request, 'drivers', '35-ddd', dui_dwi_incident_date_formatted.strftime('%m/%d/%Y')))
    else:
        return message('date is not valid, make sure your date before today',page=currentPage)

def page_driver_violations(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    driver_violations = parameters.get('driver-violations')[0]
    print(driver_violations)
    return next(mongo_list(main_request,'drivers','37-dv',driver_violations))

def page_driver_violations_yes(main_request):
    print('driver_violations_yes')
    return next(mongo_list(main_request,'drivers','36-dv?',True))

def page_driver_violations_no(main_request):
    print('driver_violations_no')
    return next(mongo_list(main_request,'drivers','36-dv?',False))

def page_add_another_driver_yes(main_request):
    print('add_another_driver_yes')
    mongodb_saved = main_request.get('sessionInfo').get('parameters').get('mongodb_saved')
    mongodb_saved=add_driver(main_request,'drivers')
    main_request ['sessionInfo']['parameters']['mongodb_saved']=mongodb_saved
    print(mongodb_saved)
    return next(mongo_list(main_request,'drivers','38-aad',True))

def page_add_another_driver_no(main_request):
    print('add_another_driver_no')
    return next(mongo_list(main_request,'drivers','38-aad',False))


def page_insurance_last_3_years_yes(main_request):
    print('insurance_last_3_years_yes')
    return next(mongo_kv(main_request,'39-il3y',True))

def page_insurance_last_3_years_no(main_request):
    print('insurance_last_3_years_no')
    return next(mongo_kv(main_request,'39-il3y',False))

def page_body_injury_limits(main_request):
    print(main_request)
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    body_injury_limits = parameters.get('coverage-level')[0]['amount']
    print(body_injury_limits)
    if get_coverage_level(body_injury_limits):
        return next(mongo_kv(main_request, '40-bil', get_coverage_level(body_injury_limits)))
    else:
        return message(text='your coverage level not supported',page=currentPage)

def page_motorist_coverage(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    motorist_coverage = parameters.get('coverage-level')[0]['amount']
    print(motorist_coverage)
    if get_coverage_level(motorist_coverage):
        return next(mongo_kv(main_request, '41-mc', get_coverage_level(motorist_coverage)))
    else:
        return message(text='your coverage level not supported',page=currentPage)

def page_medical_payments_coverage(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    medical_payments_coverage = parameters.get('coverage-level')[0]['amount']
    print(medical_payments_coverage)
    if get_coverage_level(medical_payments_coverage):
        return next(mongo_kv(main_request, '42-mpc', get_coverage_level(medical_payments_coverage)))
    else:
        return message(text='your coverage level not supported',page=currentPage)


def page_email(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    email = parameters.get('email')[0]
    print(email)
    return next(mongo_kv(main_request,'43-e',email))

def page_domain(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    domain = parameters.get('email-domain')[0]
    return next(mongo_kv(main_request,'43-ed',domain))

def page_email_spelling(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    domain = parameters.get('email-domain')[0]

    username = parameters.get('numbers-letters')[0]
    username=username.lower()
    # email_spelling=email_spelling.replace(' at ','@').replace(' ','').replace('dot','.').replace('period','.')
    username=username.replace(' ','').replace('dot','.').replace('period','.')
    email=username+'@'+domain+'.com'
    print(email)
    if check_email(email):
        # print(email_spelling)
        return next(mongo_kv(main_request,'43-e',email))
    else:
        return message('Email is not valid, Can you re-enter valid email?',page=currentPage)

def page_phone_number(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    phone_number = parameters.get('numbers')[0]
    print(phone_number)
    # if len(str(phone_number)) == 10:
    return next(mongo_kv(main_request,'44-pn',phone_number))
    # else:
    #     return message('phone number should be 10 number length',page=currentPage)

def page_autodialed_yes(main_request):
    print('page_autodialed_yes')
    return next(mongo_kv(main_request,'45-ad?',True))

def page_autodialed_no(main_request):
    print('page_autodialed_no')
    return next(mongo_kv(main_request,'45-ad?',False))

def page_license_state(main_request):
    currentPage=main_request.get('pageInfo').get('currentPage')
    parameters=main_request.get('sessionInfo').get('parameters')
    license_state = parameters.get('license-state')[0]
    if us.states.lookup(license_state) != None:
        license_state=us.states.lookup(license_state).abbr
        return next(mongo_kv(main_request, '46-ls', license_state))
    else:
        return message('state name not true',page=currentPage)

def page_license_number(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    license_number = parameters.get('numbers-letters')[0]
    print(license_number)
    return next(mongo_kv(main_request,'47-lnum',license_number))

def page_policy_start(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    policy_start = parameters.get('policy-start')[0]
    print(policy_start)
    policy_start_formatted=datetime.date(year=int(policy_start["year"]), month=int(policy_start["month"]), day=int(policy_start["day"]))

    if policy_start_formatted >= datetime.date.today():
        return next(mongo_kv(main_request, '48-ps', policy_start_formatted.strftime('%m/%d/%Y')))
    else:
        return message('date is not valid, make sure your date after today',page=currentPage)

def page_national_origin(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    national_origin = parameters.get('national-origin')[0]
    print(national_origin)
    return next(mongo_kv(main_request,'49-no',national_origin))

def page_monthly_pay(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    monthly_pay = parameters.get('monthly-pay')[0]
    print(monthly_pay)
    return next(mongo_kv(main_request,'50-mp',monthly_pay))

def page_credit_card_number(main_request):
    currentPage = main_request.get('pageInfo').get('currentPage')
    parameters = main_request.get('sessionInfo').get('parameters')
    credit_card_number = parameters.get('numbers')[0]
    print(credit_card_number)
    if len(str(credit_card_number)) == 16:
        mongodb_saved = mongo_kv(main_request, '51-ccn', credit_card_number)
        # print(mongodb_saved)
        # # response=requests.post(backend_URL+"/db_save",json=mongodb_saved)
        # result=response.json()['results']
        # # print(result)
        # if result == 'True':
        return message('your details are recorded',mongodb_saved=mongodb_saved)
        # else:
        #     return message('there was a problem saving your data please try again',page=currentPage)
    else:
        return message('not valid credit card number',page=currentPage)
