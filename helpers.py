import json,requests,vinlib,_json,csv,random,re

# backend_URL="https://af87d329529a.ngrok.io"
backend_URL="https://robo-agent.uc.r.appspot.com"

def get_city_opendata(city, country='us'):
    tmp = 'https://public.opendatasoft.com/api/records/1.0/search/?dataset=worldcitiespop&q=%s&sort=population&facet=country&refine.country=%s'
    cmd = tmp % (city, country)
    res = requests.get(cmd)
    dct = json.loads(res.content)
    out = dct['records'][0]['fields']
    return out

def get_available_makes():
    make_list=[]
    with open('Year-Make-Model.csv',encoding='latin-1') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[1].lower() in make_list:
                pass
            else:
                make_list.append(row[1].lower())
    return make_list

def search_for_make(make):
    if make.lower() in get_available_makes():
        return True
    else:
        return False

def get_models_make_year(make,year):
    models_list=[]
    with open('Year-Make-Model.csv',encoding='latin-1') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:

            if make.lower() == row[1].lower() and year == row[0]:
                models_list.append(row[2].lower())
    return models_list

def get_models_make(make):
    models_list=[]
    with open('Year-Make-Model.csv',encoding='latin-1') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[2].lower() in models_list:
                pass
            else:
                if make.lower() == row[1].lower():
                    models_list.append(row[2].lower())
    return models_list


def mongo_kv(main_request,key,value):
    mongodb_saved = main_request.get('sessionInfo').get('parameters').get('mongodb_saved')
    if not mongodb_saved:
        mongodb_saved={}
        mongodb_saved["_id"]=random.randint(0,100000000)
        mongodb_saved[key] = value
        p=requests.post(backend_URL+'/db_replace',json=mongodb_saved)
    else:
        mongodb_saved[key] = value
        p=requests.post(backend_URL+'/db_replace',json=mongodb_saved)

    # print('result is ',p.json()["results"])

    return mongodb_saved


def mongo_list(main_request, listname, key, value,newdriver=False):
    mongodb_saved = main_request.get('sessionInfo').get('parameters').get('mongodb_saved')
    try:
        if mongodb_saved[listname]:
            i=len(mongodb_saved[listname])-1
            if mongodb_saved[listname][i] != None:
                mongodb_saved[listname][i][key]= value
                p = requests.post(backend_URL + '/db_replace', json=mongodb_saved)
                # replace mongodb_saved after modified from previous line
    except:
        mongodb_saved[listname]=[]
        mongodb_saved[listname].append({key: value})
        p=requests.post(backend_URL+'/db_replace',json=mongodb_saved)

    # print(len(mongodb_saved[listname]))
    return mongodb_saved


def add_driver(main_request,listname):
    mongodb_saved = main_request.get('sessionInfo').get('parameters').get('mongodb_saved')
    mongodb_saved[listname].append({})
    return mongodb_saved

def get_coverage_level(payment):
    payment=int(payment)
    if payment >= 15000 and payment < 25000 :
        return '$15,000 to $25,000 '

    elif payment >= 25000 and payment < 50000 :
        return '$25,000 to $50,000'

    elif payment >= 50000 and payment < 100000 :
        return '$50,000 to $100,000'

    elif payment >= 100000 and payment <= 300000 :
        return '$100,000 to $300,000 or higher'
    else:
        return False

def check_email(email):
    regex = '^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$'

    if (re.search(regex, email)):
        print("Valid Email")
        return True
    else:
        print("Invalid Email")
        return False