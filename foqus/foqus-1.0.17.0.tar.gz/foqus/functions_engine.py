#! /usr/bin/python
# -*- coding:utf-8 -*-
from crontab import CronTab

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from foqus.customers import *
from foqus.commons import count_product, get_count_product_validation, get_payment_details_cms_shopify, get_valid_post,\
    replace_special_caractere, shopify_data_and_train, download
from foqus.payments import p_fwd__stripe_payment
from foqus.request_api import *
from foqus.cloud_configuration import *
from pandas import DataFrame

import getpass
import hashlib
import random
import string
import shutil
import tldextract
import uuid
import vatnumber
import base64

api = APIFoqus()
url_ms = 'https://westeurope.api.cognitive.microsoft.com/customvision/' + os.environ.get('MS_VERSION') +'/Prediction/' \
         + os.environ.get('MS_KEYID') + '/detect/iterations/' + os.environ.get('MS_ITERATION') +'/image'
url_bing = 'https://bingvisualsearchfoqus.cognitiveservices.azure.com/bing/v7.0/images/visualsearch/' \
           '?mkt=' + os.environ.get('MS_MKT') + '&safeSearch=' + os.environ.get('MS_SAFE_SEARCH')

def all_user_projects(customer_name, customer_type, api_project):
    result = db.select_users_projects(customer=customer_name, customer_type=customer_type, api=api_project)
    data = []
    if result:
        for i in range(0, len(result)):
            data.append([result[i][0], result[i][1], result[i][2]])
    return data


def create_project(customer_name, customer_type, api_project, project_name, project_id):
    if api_project == 'similars':
        similars_projects = all_user_projects(customer_name, customer_type, api_project)
        classification_projects = all_user_projects(customer_name, customer_type, 'classification')
        similars_project_path = INPUT_PATH + customer_type + '/' + customer_name + '/images'
        if project_name in similars_projects:
            logger.error("le projet existe , veuillez choisir un autre nom")
            return 0
        elif project_name in classification_projects:
            return 0
        else:
            try:
                os.makedirs(similars_project_path + '/' + str(project_name))
                create_update_project(customer_name, customer_type, str(project_name), api_project, 1,
                                      str(project_name), training_details="{}", counter=0)
                logger.info("similars project was created with success ")
                return 1
            except Exception as e:
                logger.error("similars project was not created %s" % e)
            return 0
    if api_project == 'classification':
        similars_projects = all_user_projects(customer_name, customer_type, api_project)
        classification_projects = all_user_projects(customer_name, customer_type, 'classification')
        trainings_path = TRAININGS_PATH + customer_type + '/' + customer_name + '/classification'
        if project_name in similars_projects:
            logger.error("le projet existe , veuillez choisir un autre nom")
            return 0
        elif project_name in classification_projects:
            return 0
        else:
            try:
                os.makedirs(trainings_path + '/' + str(project_name))
                create_update_project(customer_name, customer_type, str(project_name), api_project, 1,
                                      str(project_name), training_details="{}", counter=0)
                logger.info("classification project was created with success ")
                return 1
            except Exception as e:
                logger.error("classification project was not created %s" % e)
            return 0
    return 0


def get_all_plans_payement(customer_email, type_user_admin):
    type_user_sender = db.verif_permission(customerEmail=customer_email, type_user=type_user_admin)
    msg = "You are not allowed to get_all_plans_payement."
    if (str(type_user_sender) != "Email not found") and (str(type_user_sender) != "Error"):
        if str(type_user_sender) == "admin":
            result = []
            list_plan = db.get_all_plans_payement(table_name="plan")
            for plan in list_plan:
                plan_name = {'plan_name': plan[1]}
                payment_period = {'payment_period': plan[2]}
                total = {'total': float(plan[3])}
                max_image_training = {'max_image_training': plan[4]}
                data = [plan_name, payment_period, total,max_image_training ]
                result.append(data)
            return result
        elif str(type_user_sender) in ["customer", "SN1", "SN2", "SN3"]:
            return msg
        else:
            return msg
    else:
        return "Please check your customer_email."


def number_post_per_clients():
    response = db.select_number_post_per_clients(HISTORY_SEARCH_TABLE)
    result = []
    for res in response:
        name = {'customer_name': res[1]}
        type = {'customer_type': res[2]}
        nb_post = {'number_post': res[0]}
        data = [name, type, nb_post]
        result.append(data)
    return result


def predict_image(image_path, customer_name, customer_type, project_name, similars=None):
    response = api.apiget('get_category', customer_name, customer_type, project_name, image_path)
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    category = json.loads(response)
    image_domaine = (tldextract.extract(image_path)).domain
    if similars is None and category != {'no_category': 0}:
        db.insert_or_update_into_table_history(HISTORY_SEARCH_TABLE, today, customer_name, customer_type,
                                               project_name, image_path, 'classification', json.dumps({}),
                                               category, "", image_domaine, "")

    return category


def get_historic(customer_name, customer_type, project_name, month_num):
    response_historic = []
    days = []
    nmber_requests_by_day = []
    counter_tres_faible = 0
    counter_faible = 0
    counter_moyen = 0
    counter_bon = 0
    counter_excellent = 0

    if month_num is None:
        if project_name is None:
            list_project = db.select_list_project_name(HISTORY_SEARCH_TABLE,  customer_name, customer_type)
        else:
            list_project = [(project_name,)]

        for project in list_project:
            list_response = db.select_historic_project(HISTORY_SEARCH_TABLE, customer_name, customer_type,
                                                       project[0])
            each_search = []

            for response in list_response:
                if response[8] != "{}":
                    cat = (response[8].replace("{", "").replace("}", "").replace('"', "")).split(":")
                else:
                    cat = ["", "0"]

                res = ""
                if "similars" in response[7]:
                    similars = json.loads(response[7])
                    if similars["similars"] == []:
                        continue
                    elif int(similars["similars"][0]['score']) < 30:
                        counter_tres_faible = counter_tres_faible + 1
                        res = str(similars["similars"][0]['score']) + "%" + " : Very low similarity score"
                    elif int(similars["similars"][0]['score']) >= 30 and int(
                            similars["similars"][0]['score']) < 50:
                        counter_faible = counter_faible + 1
                        res = (str(similars["similars"][0]['score']) + "%" + " : low similarity score")
                    elif int(similars["similars"][0]['score']) >= 50 and int(
                            similars["similars"][0]['score']) < 75:
                        counter_moyen = counter_moyen + 1
                        res = (str(similars["similars"][0]['score']) + "%" + " : Medium similarity score")
                    elif int(similars["similars"][0]['score']) >= 75 and int(
                            similars["similars"][0]['score']) < 90:
                        counter_bon = counter_bon + 1
                        res = (str(similars["similars"][0]['score']) + "%" + " : Good similarity score")
                    else:
                        counter_excellent = counter_excellent + 1
                        res = (str(similars["similars"][0]['score']) + "%" + " : Excellent similarity score")

                data = {
                    "date": response[1].strftime("%d-%m-%Y %H:%M:%S"),
                    "url": response[5],
                    "category": {"name": cat[0], "score": float(cat[1].replace(" ", ""))},
                    "country": response[11],
                    "searched_time": response[9],
                    "similars": res
                }

                each_search.append(data)

            response_historic.append({"project": project[0],
                                      "api": "search_similars",
                                      "photos": each_search})
    else:
        requests_date = db.get_date_and_counter_from_historic_table(HISTORY_SEARCH_TABLE, customer_name,
                                                                    customer_type, str(month_num))
        for data in requests_date:
            days.append(str(data[1]))
            nmber_requests_by_day.append(data[0])

        response_list = db.select_all_utilistation_par_mois(HISTORY_SEARCH_TABLE, customer_name, customer_type,
                                                            str(month_num))

        if response_list:
            for j in range(0, len(response_list)):
                data = []
                for i in range(0, len(response_list[j])):

                    if i == 1:
                        data.append(str(response_list[j][i]))

                    elif i == 7:
                        if "similars" in response_list[j][i]:
                            similars = json.loads(response_list[j][i])
                            if int(similars["similars"][0]['score']) < 30:
                                counter_tres_faible = counter_tres_faible + 1
                                data.append(str(similars["similars"][0][
                                                    'score']) + "%" + ":  Very low similarity score")
                            elif int(similars["similars"][0]['score']) >= 30 and int(
                                    similars["similars"][0]['score']) < 50:
                                counter_faible = counter_faible + 1
                                data.append(str(
                                    similars["similars"][0]['score']) + "%" + ":  Low similarity score")
                            elif int(similars["similars"][0]['score']) >= 50 and int(
                                    similars["similars"][0]['score']) < 75:
                                counter_moyen = counter_moyen + 1
                                data.append(str(
                                    similars["similars"][0]['score']) + "%" + ":  Medium similarity score")
                            elif int(similars["similars"][0]['score']) >= 75 and int(
                                    similars["similars"][0]['score']) < 90:
                                counter_bon = counter_bon + 1
                                data.append(
                                    str(similars["similars"][0]['score']) + "%" + ":  Good similarity score")
                            else:
                                counter_excellent = counter_excellent + 1
                                data.append(str(similars["similars"][0][
                                                    'score']) + "%" + ":  Excellent similarity score")
                    elif i == 8:
                        classif = json.loads(response_list[j][i])
                        data.append(classif)
                    else:
                        data.append(response_list[j][i])
                response_historic.append(data)

    return {"response": response_historic,
            "statistic_score": {"tres_faible": counter_tres_faible,
                                "faible": counter_faible,
                                "moyen": counter_moyen,
                                "bon": counter_bon,
                                "excellent": counter_excellent},
            "requests_by_month": {"days": days, "nmber_requests_by_day": nmber_requests_by_day}}

def get_client_payment_status(customer_name, customer_type):
    response = db.get_client_payment(customer_name, customer_type)
    return response


def get_apikey_expiration_time(customer_name, customer_type, apikey):
    apikey = db.get_apikey_from_customer_and_customer_type(customer_name, customer_type , apikey)
    api_key = apikey[0]
    response = datetime.datetime.fromtimestamp(get_apikey_expiration(api_key)).strftime("%d-%m-%Y %I:%M:%S")
    return response


def get_details_trainings_for_client(customer_name, customer_type, project_name, api_project):
    response = db.get_training_detalis(STATUS_PROJECT_TABLE, customer_name, customer_type, project_name, api_project)
    status_training = response[2]
    if response[1] == 0:
        date_end_training = ""
        url_training_file = ""
    else:
        try:
            info_last_training = json.loads(response[0])['training'+ str(response[1])]
            date_end_training = info_last_training['date_end_training']
            url_training_file = info_last_training['url_training_file']
        except Exception as e:
            date_end_training = ""
            url_training_file = ""

    result = {'url_training_file': url_training_file,
            'date_end_training': date_end_training,
            'status_training': status_training}
    return result


def get_details_trainings_for_admin(customer_name,customer_type,project_name, api_project):
    response = db.get_training_detalis(STATUS_PROJECT_TABLE, customer_name, customer_type, project_name, api_project)
    if response is not None:
        result={'trainings_details':json.loads(response[0]),
                'number_trainings_by_project': response[1],
                'status_last_training': response[2]}
    else:
        result = {'trainings_details': '',
                  'number_trainings_by_project': 0,
                  'status_last_training': 0}
    return result


def historic_users_management():
    response = db.get__historic_users_management()
    result = []
    for res in response:
        email = {'email': res[0]}
        customer_name = {'customer_name': res[6]}
        customer_type = {'customer_type': res[7]}
        expiration_apikey = {'expiration_apikey': datetime.datetime.fromtimestamp(res[8]).strftime("%d-%m-%Y %I:%M:%S")}
        cnx_counter = {'cnx_counter' : int(res[1])}
        cnx_date = {'cnx_date' : list(res[2].split("+++"))}
        ip_addr = {'ip_address': list(res[3].split("+++"))}
        devices = {'device': list(res[4].split("+++"))}
        city = {'city': list(res[5].split("+++"))}
        data = [email, customer_name, customer_type, expiration_apikey, cnx_counter, cnx_date, ip_addr, devices, city]
        result.append(data)
    return result


def new_similars(customer_name, customer_type, project_name, image, adress_ip, boundingbox):
    try:
        similars = api.apiget('get_similars', customer_name, customer_type, project_name, image, boundingbox)
        response = json.loads(similars)
        if response.get('response', {}).get('similars', []):
            today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            image_domain = (tldextract.extract(image)).domain
            db.insert_or_update_into_table_history(HISTORY_SEARCH_TABLE, today, customer_name, customer_type,
                                                   project_name, image, 'search_similars',
                                                   response.get('response', {'similars': []}),
                                                   response.get('category', {}), adress_ip, image_domain, "")
        return json.dumps(response)
    except Exception as e:
        logger.error('Exception %s' % e)
        return json.dumps({'response': {'similars': []}})


def customer_authentication_api(customerEmail, customerPassword, type_user):
    login = db.login(customerEmail=customerEmail, customerPassword=customerPassword, type_user=type_user)

    is_authenticated = login.split("#$#")[0]
    type_user = login.split("#$#")[1]

    permission = ""
    if str(is_authenticated) == "True":
        permissions = db.get_permission(type_user=type_user)[0]
        for key, value in permissions[1].items():
            if value == 1:
                permission = permission + key+ "|"

    return str(is_authenticated) + "#$#" + permission


def customer_inscription(customer_email, customer_name, customer_type, type_user):
    api_key = str(uuid.uuid4())
    token = str(uuid.uuid4())
    password = ''.join(random.choice(string.ascii_uppercase) for _ in range(8))
    logger.info('Password for client %s is %s' % (customer_email, password))
    hash_password = hashlib.sha512(password.encode('utf-8')).hexdigest()

    add_customer = db.add_customer(customer=customer_name, customerPassword=hash_password, customerEmail=customer_email,
                                   customerJob="", customerPhone="", token=token, aboutUs="", subjectHelp="",
                                   domaine=customer_type, firstName="", lastName="", stafNumber="", apikey=api_key,
                                   expiration_duration_in_hours=100, type=type_user)

    if add_customer:
        db.commit_db_changes()
        # sending email
        customer = db.get_profile(table_name=DATABASE_USERS_MANAGEMENT_TABLE_NAME,
                                  customerEmail=customer_email)
        try:
            full_url = DOMAIN + 'activate/' + urlsafe_base64_encode(force_bytes(customer[0])) \
                       + '/' + customer[12]
        except:
            full_url = DOMAIN + 'activate/' + urlsafe_base64_encode(force_bytes(customer[0])).decode('utf-8') \
                       + '/' + customer[12]
        send_inscription_email(customer_email, full_url, password)
        return api_key
    else:
        return 'The email address is already in use. Please try another email address.'


def get_client_statistics(customer_name, customer_type):
    month_year = str(datetime.date.today())[5:7]+'-'+str(datetime.date.today())[0:4]
    response1 = get_counter_of_last_four_months(customer_name, customer_type)[0]
    response2 = db.get_sum_of_counter_from_country_code(HISTORY_SEARCH_TABLE, customer_name, customer_type)
    response3 = db.get_date_and_counter_from_historic_table(HISTORY_SEARCH_TABLE, customer_name, customer_type,
                                                            month_year)

    response4 = scores_repartition_per_users(customer_name, customer_type)
    number_request_week = number_request_by_week(customer_name, customer_type)
    user_progress_requests = [get_counter_of_last_four_months(customer_name, customer_type)[1],
                              get_counter_of_last_four_months(customer_name, customer_type)[2]]
    requests_four_last_months = []
    for i in range(0, len(response1)):
        requests_four_last_months.append({"month": response1[i][0], "number": response1[i][1]})

    request_by_country = []
    for c in range(0, len(response2)):
        request_by_country.append({"country": response2[c][1], "number": response2[c][0]})

    score_repartition_per_user1 = {"interval": "[10% - 30%]", "number": response4[0]}
    score_repartition_per_user2 = {"interval": "[30% - 50%]", "number": response4[1]}
    score_repartition_per_user3 = {"interval": "[50% - 75%]", "number": response4[2]}
    score_repartition_per_user4 = {"interval": "[75% - 90%]", "number": response4[3]}
    score_repartition_per_user5 = {"interval": "[90% - 100%]", "number": response4[4]}
    score_repartition_per_user = [score_repartition_per_user1, score_repartition_per_user2, score_repartition_per_user3,
                                  score_repartition_per_user4, score_repartition_per_user5]
    daily_request_current_month= []
    for j in range(0, len(response3)):
        daily_request_current_month.append({"date": (response3[j][1]).strftime('%d-%m-%Y'), "number": response3[j][0]})

    nbr_request_total_current_month = []
    request_number_progress = []
    for j in range(0, len(response3)):
        nbr_request_total_current_month.append(response3[j][0])

    customer_plan = db.get_client_payment(customer_name, customer_type)
    if customer_plan[5] == 'FREE':
        number_of_requests_allowed = 1000
    else:
        number_of_requests_allowed = 1000000

    request_total = sum(nbr_request_total_current_month)
    request_number_progress.append({"number_of_requests_used": request_total,
                                    "number_of_requests_allowed": number_of_requests_allowed})

    user_progress_requests_per_period = {}
    progression = []
    user_progress_requests_per_period['user_progress_requests_previous_period'] = user_progress_requests[0]
    user_progress_requests_per_period['user_progress_requests_last_3_month_ago'] = user_progress_requests[1]
    progression.append(user_progress_requests_per_period)

    result = {
        'number_of_requests_for_the_four_last_months': requests_four_last_months,
        'request_repartition': request_by_country,
        'daily_request_for_current_month': daily_request_current_month,
        'scores_repartition_per_users': score_repartition_per_user,
        'number_request_by_week_of_current_month': number_request_week,
        'user_progress_requests_per_period': progression,
        'request_number_progress_for_current_month': request_number_progress

    }
    return result


def all_status_project(customer_name, customer_type):
    result = db.select_status_project_similars(STATUS_PROJECT_TABLE, customer_name, customer_type)
    data=[]
    if result:
        for i in range(0, len(result)):
            data.append([result[i][0], result[i][1]])
    return data


def customer_info(data):
    logger.info(data)
    customer_email = data.get('customer_email')

    customer_infos = db.get_profile(DATABASE_USERS_MANAGEMENT_TABLE_NAME, customer_email)
    if customer_infos:
        customer_name = customer_infos[1]
        customer_type = customer_infos[8]
        apikey = customer_infos[13]
        is_active = customer_infos[15]
        if is_active == 0:
            return {"code": 403, "Message": {"response": "Unactivated account"}}
        payment_client = payment_status(customer_name, customer_type)
        if is_user_allowed(apikey) or payment_client.get('choosed_plan', 'FREE') == 'FREE' or \
                        data.get('cms_type', None) == 'shopify':
            if data.get("project_name", None) and data.get("cms_type", None) and data.get("url_cms", None):
                project_name = data.get('project_name')
                access_token = data.get('token', '')
                if (':' in project_name) or ('/' in project_name):
                    return {"code": 405, "Message": {"response": "Not allowed"}}
                cms_type = data.get('cms_type')
                url_cms = data.get('url_cms').split('https://')[1] if 'https://' in data.get('url_cms') else \
                    data.get('url_cms')
                logger.info('===> API_Customer_info_url_data type %s url_cms  %s token %s' % (cms_type, url_cms,
                                                                                              access_token))

                save_data_from_cms(customer_name, customer_type, project_name, cms_type, url_cms, access_token)
                if get_valid_post(customer_name, customer_type):
                    logger.info("max_post_exceeded_cms, 403 client %s type %s email %s"
                                % (customer_name, customer_type, customer_email))
                    return {"code": 403, "Message": {"response": "max post exceeded"}}
                details_training = db.get_training_detalis(STATUS_PROJECT_TABLE, customer_name, customer_type,
                                                           project_name
                                                           , 'similars')
                # Shopify case and wordpress creation of new project
                if details_training is None or details_training[1] == 0:
                    create_update_project(customer_name, customer_type, str(project_name), 'similars', 1,
                                          str(project_name), "", 0)

                if cms_type == 'shopify':
                    payment = payment_client.get('payment', {})
                    payment_validation, apikey = get_payment_details_cms_shopify(customer_name, customer_type,
                                                                                 url_cms, access_token, payment)

                    if (is_user_allowed(apikey) and payment_validation) or  \
                                    payment_client.get('choosed_plan', 'FREE') == 'FREE':

                        # Schedule training every specific time depends on plan
                        details_training = db.get_training_detalis(STATUS_PROJECT_TABLE, customer_name, customer_type,
                                                                   project_name, 'similars')
                        # create cron one time
                        if details_training[1] == 0:
                            date = datetime.datetime.now()
                            if payment_client.get('choosed_plan') == 'FREE':
                                timer = str(date.minute) + " " + str(date.hour) + " * * " + str(date.weekday() + 1) \
                                    if date.weekday() < 7 else str(0)
                            else:
                                timer = str(date.minute) + " " + str(date.hour) + " * * *"

                            path_file = BASE_DIR + 'shopify_crons.py ' + customer_name + ' ' + customer_type + ' ' + \
                                        url_cms + ' ' + apikey + ' ' + project_name
                            command = '/usr/bin/python3 ' + path_file
                            my_cron = CronTab(user=getpass.getuser())
                            job = my_cron.new(command=command)
                            job.setall(timer)
                            my_cron.write()
                            logger.info("Cron_created_shopify at time %s for client %s type %s every %s"
                                        % (str(date), customer_name, customer_type, timer))

                        if count_product(token=access_token, url_shop=url_cms) == 0:
                            logger.info("No_products_found_in_store_shopify, 200 client %s type %s email %s"
                                        % (customer_name, customer_type, customer_email))

                            return {"code": 200, "Message": {'customer_email': customer_email,
                                                             'customer_name': customer_name,
                                                             'customer_type': customer_type,
                                                             'user_api_key': apikey,
                                                             'response': 'No products found in store'}}

                        if not get_count_product_validation(access_token, url_cms,
                                                            payment_client.get('choosed_plan', 'FREE')):
                            logger.info("Not_allowed_max_number_products_exceeded_shopify, "
                                        "405 client %s type %s email %s"
                                        % (customer_name, customer_type, customer_email))
                            return {"code": 405, "Message": {"response": "Not allowed, max number products exceeded"}}

                        if details_training[1] == 0:
                            logger.info('Launching Shopify training')
                            shopify_data_and_train(access_token, url_cms, customer_name, customer_type, apikey,
                                                   project_name)

                    else:
                        logger.info("Unpaid_payment_shopify, 402 client %s type %s email %s"
                                    % (customer_name, customer_type, customer_email))
                        return {"code": 402, "Message": {"response": "Unpaid payment"}}

                logger.info("Everything_is_OK_cms, 200 client %s type %s email %s"
                            % (customer_name, customer_type, customer_email))
                return {"code": 200, "Message": {'customer_email': customer_email,
                                                 'customer_name': customer_name,
                                                 'customer_type': customer_type,
                                                 'user_api_key': apikey}}

            if get_valid_post(customer_name, customer_type):
                logger.info("max post exceeded, 403 client %s type %s email %s"
                            % (customer_name, customer_type, customer_email))

                return {"code": 403, "Message": {"response": "max post exceeded"}}

            logger.info("Everything_is_OK, 200 client %s type %s email %s"
                        % (customer_name, customer_type, customer_email))
            return {"code": 200, "Message": {'customer_email': customer_email,
                                             'customer_name': customer_name,
                                             'customer_type': customer_type,
                                             'user_api_key': apikey}}

        else:
            logger.info("Unpaid_payment, 402 client %s type %s email %s"
                        % (customer_name, customer_type, customer_email))
            return {"code": 402, "Message": {"response": "Unpaid payment"}}

    else:
        logger.info("Client_not_found, 404 client email %s"
                    % customer_email)
        return {"code": 404, "Message": {"response": "Email not found"}}


def save_client_reviews(customer_name, customer_type, project_name, review, url_image):
    response = db.save_client_reviews(customer_name, customer_type, project_name, review,url_image)
    return response

def change_customer_password(customer_password, customer_email, new_password, new_password_verif):
    try:
        profile = db.get_profile(table_name=DATABASE_USERS_MANAGEMENT_TABLE_NAME, customerEmail=customer_email)
        password_old = profile[2]

        customer_password = hashlib.sha512(customer_password.encode('utf-8')).hexdigest()
        hashed_new_password = hashlib.sha512(new_password.encode('utf-8')).hexdigest()

        if customer_password == password_old and new_password == new_password_verif:
            db.set_password(table_name=DATABASE_USERS_MANAGEMENT_TABLE_NAME, customerPasswordN=hashed_new_password,
                            customerEmail=customer_email)
            db.commit_db_changes()
            logger.info('Your password has been successfully updated!')
            return True

        elif customer_password == hashed_new_password and new_password != new_password_verif :
            logger.error('Your new password looks like your current password and the two fields are not identical!')
            return 'Your new password looks like your current password and the two fields are not identical!'

        elif customer_password == hashed_new_password :
            logger.error('Your new password looks like your current password. Please try another one.')
            return 'Your new password looks like your current password. Please try another one.'

        elif customer_password != password_old and new_password != new_password_verif:
            logger.error('Old password incorrect and the two fields are not identical!')
            return 'Old password incorrect and the two fields are not identical!'

        elif customer_password != password_old:
            logger.error('Your old password is incorrect!')
            return 'Your old password is incorrect!'

        elif new_password != new_password_verif:
            logger.error('The two fields are not identical!')
            return 'The two fields are not identical!'

        else:
            logger.error("Error")

    except Exception as e:
        logger.error("Exception in getting customer password from db %s" %e)


def update_profile_customer(customer_email, customer_name, first_name, last_name,
                            phone_number, job, new_email):

    try:
        profile = db.get_profile(table_name=DATABASE_USERS_MANAGEMENT_TABLE_NAME, customerEmail=customer_email)
        id_profile = profile[0]
        old_name = profile[1]
        customer_type = profile[8]

        if new_email == customer_email or new_email== "":
            db.set_profile(table_name=DATABASE_USERS_MANAGEMENT_TABLE_NAME, firstName=first_name, lastName=last_name,
                           customerJob=job, customerPhone=phone_number, customerEmail=customer_email,
                           customer=customer_name, id=str(id_profile))
        else:
            existing_profile = db.get_profile(table_name=DATABASE_USERS_MANAGEMENT_TABLE_NAME, customerEmail=new_email)
            if existing_profile:
                return False
            else:
                db.set_profile(table_name=DATABASE_USERS_MANAGEMENT_TABLE_NAME, firstName=first_name, lastName=last_name,
                           customerJob=job, customerPhone=phone_number, customerEmail=new_email,
                           customer=customer_name, id=str(id_profile))

        db.commit_db_changes()
        if old_name != customer_name:
            db.update_customer_name_payment_table(customer_name, old_name, customer_type)
            db.update_customer_name_history_table(customer_name, old_name, customer_type)
            db.update_customer_name_cms_table(customer_name, old_name, customer_type)
            db.update_customer_name_projects_table(customer_name, old_name, customer_type)
            db.update_customer_review_table(customer_name, old_name, customer_type)
            db.rename_table_client(replace_special_caractere(old_name).replace(' ', ''),
                                   replace_special_caractere(customer_name).replace(' ', ''))
            db.commit_db_changes()

        return True
    except Exception as e:
        logger.error("exception in update_profile_API : %s  " % e)
        return False


def customer_registration(customer_email, customer_type, customer_name, customer_password, first_name, last_name,
                          phone_number, job, number_of_staff, plan, cms_if_exist, url_cms, token_cms):

    uid = str(uuid.uuid4())
    token = str(uuid.uuid4())
    if plan == "FREE":
        expiration = 4380000
    else:
        expiration = 720
    add_customer = db.add_customer(customer=customer_name, customerPassword=customer_password,
                                   customerEmail=customer_email, customerJob=job, customerPhone=phone_number,
                                   token=token, aboutUs="", subjectHelp="", domaine=customer_type,
                                   firstName=first_name, lastName=last_name, stafNumber=number_of_staff, apikey=uid,
                                   expiration_duration_in_hours=expiration, type="customer")
    if add_customer:
        db.commit_db_changes()
        if token_cms:

            db.add_or_update_cms_table(table_name=CMS_TABLE, customer_name=customer_name,
                                       customer_type=customer_type,
                                       project_name="", cms=cms_if_exist, url_shop=url_cms, token=token_cms)
        else:

            db.add_or_update_cms_table(table_name=CMS_TABLE, customer_name=customer_name,
                                       customer_type=customer_type,
                                       project_name="", cms=cms_if_exist, url_shop=url_cms, token='')

        date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

        db.create_payment_client(customer_name, customer_type, date, 'eur', 0)
        db.create_plans_table()
        if plan == "FREE":
            db.update_client_payement(customer_name, customer_type, date, plan, 0, "stripe", 0)
        else:
            db.update_client_payement(customer_name, customer_type, date, plan, 0, "stripe", 99)

        db.add_update_client_parameter(customer_name, customer_type)

        customer = db.get_profile(table_name=DATABASE_USERS_MANAGEMENT_TABLE_NAME,
                                  customerEmail=customer_email)
        try:
            full_url = DOMAIN + 'activate/' + urlsafe_base64_encode(force_bytes(customer[0])) + '/' + customer[12]
        except:
            full_url = DOMAIN + 'activate/' + urlsafe_base64_encode(force_bytes(customer[0])).decode('utf-8') \
                       + '/' + customer[12]
        if cms_if_exist == 'shopify':
            db.activate_profile(token=token)
        else:
            send_email_for_activate_account(customer[9], customer_email, full_url)
        date_inscription = str(datetime.date.today())
        send_email_of_client_inscription(customer_email, date_inscription, "Signup of new client")
        return True
    else:
        return False


def contact(first_name, customer_email, subject_of_email, message_email):
    server = smtplib.SMTP(SMTP_HOST, 587)
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    try:

        fromaddr = customer_email
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = ADMIN_EMAIL
        msg['Subject'] = subject_of_email
        html_file = codecs.open(PATH_EMAIL_CONTACT, 'r')
        html = ((str(html_file.read()).replace("#sender_name", first_name)).replace("#message_email", message_email))
        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        server.sendmail(fromaddr, ADMIN_EMAIL, msg.as_string())
        return True
    except Exception as e:
        logger.error("exception ......" + str(e))
        return False


def forget_password(customer_email):
    try:
        user = db.get_profile(table_name=DATABASE_USERS_MANAGEMENT_TABLE_NAME, customerEmail=str(customer_email))
        first_name_of_customer = user[9]
        mail_subject = 'Recuerate your account FOQUS'
        try:
            full_url = DOMAIN + 'reset_password/' + urlsafe_base64_encode(force_bytes(user[0])) \
                       + '/' + user[12]
        except:
            full_url = DOMAIN + 'reset_password/' + urlsafe_base64_encode(force_bytes(user[0])).decode('utf-8') \
                       + '/' + user[12]

        send_email_for_reset_password(customer_email, full_url, first_name_of_customer, mail_subject)
        logger.info('A recovery email has been sent. Thank you to check your mailbox')
        return True
    except :
        logger.error("you are not registred !")
        return False


def get_connected_customer_info(customer_email):
    result = {}
    try:
        customer_info = db.get_profile(table_name=DATABASE_USERS_MANAGEMENT_TABLE_NAME, customerEmail=customer_email)
        result['customer_email'] = customer_email
        result['customer_name'] = customer_info[1]
        result['job'] = customer_info[4]
        result['phone'] = customer_info[5]
        result['customer_type'] = customer_info[8]
        result['first_name'] = customer_info[9]
        result['last_name'] = customer_info[10]
        result['api_key'] = customer_info[13]
    except Exception as e:
        logger.error('email not found for this customer , Please verify your email  %s' %e)
        return False
    return result


def save_payment_info(customer, customer_type, name, address, zipcode, country, city, tva_number):
    db.insert_or_update_payment_info(PAYMENT_INFO, customer, customer_type, name, address, zipcode, country, city, tva_number)
    return True


def payment_details_client(customer_name, customer_type, choosed_plan):

    details_client = db.get_client_adress(PAYMENT_INFO, customer_name, customer_type)
    plan = db.get_plan_form_name(choosed_plan)
    client_payment = db.get_client_payment(customer_name, customer_type)
    price_month = float(plan[3]/12)

    tva_number = details_client[8]
    if vatnumber.check_vat_fr(tva_number):
        price_month_tva = price_month + (price_month * 0.2)
        total = price_month_tva * 11 if client_payment[7] else price_month_tva * 12
    else:
        total = price_month * 11 if client_payment[7] else price_month * 12

    return {"total": round(total, 2), "price_month": price_month, "tva": 1 if vatnumber.check_vat_fr(tva_number) else 0,
            "currency": client_payment[7], "interval": "365", "testing": 0 if client_payment[7] else 1}


def payment_client(customer, customer_type, email,  plan_name, methode_payment, payment_id=None, payer_id=None,
                   stripe_token=None):
    date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    details_client = db.get_client_adress(PAYMENT_INFO, customer, customer_type)
    payment = db.get_client_payment(customer, customer_type)
    plan = db.get_plan_form_name(plan_name)
    price_month = float(plan[3] / 12)
    tva_number = details_client[8]
    if vatnumber.check_vat_fr(tva_number):
        total = price_month + (price_month * 0.2)
        # total = price_month_tva * 11 if payment[7] else price_month_tva * 12
    else:
        # total = price_month * 11 if payment[7] else price_month * 12
        total = price_month
    if methode_payment == 'stripe':

        db.update_client_payement(customer, customer_type, date, plan_name, 1, 'stripe', total)

        logger.info(
            '->STRIPETOKEN<- stripe token %s for client %s ' % (
                stripe_token, email))
        stripe_error = p_fwd__stripe_payment(payment, stripe_token,
                                             float(str(total).replace(',', '.')), customer,
                                             customer_type, plan_name, email)
        from datetime import date
        period_for_client = date(int(datetime.datetime.today().strftime("%Y")),
                                 int(datetime.datetime.today().strftime("%m")),
                                 int(datetime.datetime.today().strftime("%d"))) - \
                            date(int(payment[3].strftime("%Y")), int(payment[3].strftime("%m")),
                                 int(payment[3].strftime("%d")))
        period_in_hours = (30 - int(period_for_client.days)) * 24
        create_or_update_user_apikey(user=customer, period_in_hours=period_in_hours)
        db.update_date_payment(customer, customer_type, datetime.datetime.today().strftime("%Y-%m-%d"))
        if stripe_error:
            logger.error("Errrror in payment the error is %s" % stripe_error)
            return 0
        else:
            return 1
    elif methode_payment == 'paypal':
        db.update_client_payement(customer, customer_type, date, plan_name, 1, 'paypal', total)
        db.update_transction_id(customer, customer_type, payment_id, plan_name, date, 'paypal')
        db.update_customer_id(payment[1], payment[2], payer_id, payment[5], 'paypal')
        from datetime import date
        period_for_client = date(int(datetime.datetime.today().strftime("%Y")),
                                 int(datetime.datetime.today().strftime("%m")),
                                 int(datetime.datetime.today().strftime("%d"))) - \
                            date(int(payment[3].strftime("%Y")), int(payment[3].strftime("%m")),
                                 int(payment[3].strftime("%d")))
        period_in_hours = (365 - int(period_for_client.days)) * 24
        create_or_update_user_apikey(user=customer, period_in_hours=period_in_hours)
        db.update_date_payment(customer, customer_type, datetime.datetime.today().strftime("%Y-%m-%d"))
        return 1


def get_connected_customer_cms_info(customer_name, customer_type, cms):
    result = db.get_cms_details_for_client(CMS_TABLE, customer_name, customer_type, cms)
    if result:
        if result[7]:
            url_confirmation = result[7]
        else:
            url_confirmation = ''
        response = {
            'customer_name': result[1],
            'customer_type': result[2],
            'url_cms': result[5],
            'access_token': result[6],
            'cms_type': result[4],
            'project_name': result[3],
            'url_confirmation': url_confirmation}
    else:
        response = {}
    return response


def delete_project(customer, customer_type, api_project, project_name, project_id):
    name = project_name + "_deleted" + datetime.date.today().strftime("%Y-%m-%d")
    db.update_status_name_deleted_project(name, 0, customer, customer_type, project_name, api_project)
    db.delete_from_table(HISTORY_SEARCH_TABLE, customer, customer_type, project_name)
    if project_name != "" and api_project == "similars":

        input_path_project_to_delete = INPUT_PATH + customer_type + '/' + customer + '/images/' + project_name
        output_path_project_to_delete = OUTPUT_PATH + customer_type + '/' + customer + '/images/' + project_name
        vectors_path_project_to_delete = VECTORS_PATH + customer_type + '/' + customer + '/' + project_name
        streams_path_project_similars_to_delete = STREAMS_PATH + customer_type + '/' + customer + '/similars/' + \
                                                  project_name
        training_path_project_to_delete = TRAININGS_PATH + customer_type + '/' + customer + '/classification/' + \
                                          project_name

        vectors_path_s3 = VECTORS_S3 + customer_type + '/' + customer + '/' + project_name
        output_path_s3 = OUTPUT_S3 + customer_type + '/' + customer + '/images/' + project_name
        input_path_s3 = INPUT_S3 + customer_type + '/' + customer + '/images/' + project_name
        streams_path_3 = STREAMS_S3 + customer_type + '/' + customer + '/similars/' + \
                         project_name
        training_path_s3_to_delete = TRAININGS_S3 + customer_type + '/' + customer + '/classification/' + \
                                     project_name

        vectors_path_azure = AZURE_CUSTOM_DOMAIN_BLOB + AZURE_CONTAINER_NAME + '/' + AZURE_VECTORS_PATH + customer_type + '/' + customer + '/' + project_name
        output_path_azure = AZURE_CUSTOM_DOMAIN_BLOB + AZURE_CONTAINER_NAME + '/' + AZURE_OUTPUT_PATH + customer_type + '/' + customer + '/images/' + project_name
        input_path_azure = AZURE_CUSTOM_DOMAIN_BLOB + AZURE_CONTAINER_NAME + '/' + AZURE_INPUT_PATH + customer_type + '/' + customer + '/images/' + project_name
        streams_path_azure = AZURE_CUSTOM_DOMAIN_BLOB + AZURE_CONTAINER_NAME + '/' + AZURE_STREAMS_PATH + customer_type + '/' + customer + '/similars/' + \
                             project_name
        training_path_azure = AZURE_CUSTOM_DOMAIN_BLOB + AZURE_CONTAINER_NAME + '/' + AZURE_TRAINING_PATH + customer_type + '/' + customer + '/classification/' + \
                              project_name
        input_path_azure_recovery = AZURE_CUSTOM_DOMAIN_BLOB + AZURE_CONTAINER_NAME + '/' + 'recovery_deleted_projects/' + 'input/' + \
                                      customer_type + '/' + customer + '/images/' + project_name
        output_path_azure_recovery = AZURE_CUSTOM_DOMAIN_BLOB + AZURE_CONTAINER_NAME + '/' + 'recovery_deleted_projects/' + 'output/' + \
                                    customer_type + '/' + customer + '/images/' + project_name
        vectors_path_azure_recovery = AZURE_CUSTOM_DOMAIN_BLOB + AZURE_CONTAINER_NAME + '/' + 'recovery_deleted_projects/' + 'vectors/' + \
                                    customer_type + '/' + customer + '/similars/' + project_name
        streams_path_azure_recovery = AZURE_CUSTOM_DOMAIN_BLOB + AZURE_CONTAINER_NAME + '/' + 'recovery_deleted_projects/' + 'streams/' + \
                                    customer_type + '/' + customer + '/delta_files/' + project_name
        training_path_azure_recovery = AZURE_CUSTOM_DOMAIN_BLOB + AZURE_CONTAINER_NAME + '/' + 'recovery_deleted_projects/' + 'trainings/' + \
                                    customer_type + '/' + customer + '/classification/' + project_name

        try:
            if os.path.isdir(input_path_project_to_delete):
                move_directory(source=input_path_azure, new_destination=input_path_azure_recovery,
                               prefix=input_path_s3, directory='deleted_project')
                shutil.rmtree(input_path_project_to_delete)
                logger.info("input path -------- DELETED")
            if os.path.isdir(output_path_project_to_delete):
                move_directory(source=output_path_azure, new_destination=output_path_azure_recovery,
                               prefix=output_path_s3, directory='deleted_project')
                shutil.rmtree(output_path_project_to_delete)
                logger.info("output path -------- DELETED")
            if os.path.isdir(vectors_path_project_to_delete):
                move_directory(source=vectors_path_azure, new_destination=vectors_path_azure_recovery,
                               prefix=vectors_path_s3, directory='deleted_project')

                shutil.rmtree(vectors_path_project_to_delete)
                logger.info("vectors path -------- DELETED")
            if os.path.isdir(streams_path_project_similars_to_delete):
                move_directory(source=streams_path_azure, new_destination=streams_path_azure_recovery,
                               prefix=streams_path_3, directory='deleted_project')
                shutil.rmtree(streams_path_project_similars_to_delete)
                logger.info("streams path similars -------- DELETED")
            if os.path.isdir(training_path_project_to_delete):
                move_directory(source=training_path_azure, new_destination=training_path_azure_recovery,
                               prefix=training_path_s3_to_delete, directory='deleted_project')
                shutil.rmtree(training_path_project_to_delete)
                logger.info("training classification path similars -------- DELETED")
            return 1
        except Exception as e:
            logger.info("Error deleting similars project %s %s " % (project_name, e))
            return 0

    elif project_name != "" and api_project == "classification":

        streams_path_project_classification_to_delete = STREAMS_PATH + customer_type + '/' + customer + \
                                                        '/delta_files/' + project_name
        streams_path_s3_classification_to_delete = STREAMS_S3 + customer_type + '/' + customer + \
                                                   '/classification/' + project_name
        training_path_project_to_delete = TRAININGS_PATH + customer_type + '/' + customer + '/classification/' + \
                                          project_name
        training_path_s3_to_delete = TRAININGS_PATH + customer_type + '/' + customer + '/classification/' + \
                                     project_name

        training_path_azure = AZURE_CUSTOM_DOMAIN_BLOB + AZURE_CONTAINER_NAME + '/' + AZURE_TRAINING_PATH + customer_type + '/' + customer + '/classification/' + \
                              project_name
        streams_path_azure = AZURE_CUSTOM_DOMAIN_BLOB + AZURE_CONTAINER_NAME + '/' + AZURE_STREAMS_PATH + customer_type + '/' + customer + '/similars/' + \
                             project_name
        training_path_azure_recovery = AZURE_CUSTOM_DOMAIN_BLOB + AZURE_CONTAINER_NAME + '/' + 'recovery_deleted_projects/' + 'trainings/' + \
                                       customer_type + '/' + customer + '/classification/' + project_name
        streams_path_azure_recovery = AZURE_CUSTOM_DOMAIN_BLOB + AZURE_CONTAINER_NAME + '/' + 'recovery_deleted_projects/' + 'streams/' + \
                                      customer_type + '/' + customer + '/classification/' + project_name

        try:
            move_directory(source=training_path_azure, new_destination=training_path_azure_recovery, prefix=training_path_s3_to_delete, directory='deleted_project')
            shutil.rmtree(training_path_project_to_delete)
            logger.info("training path -------- DELETED")
            move_directory(source=streams_path_azure, new_destination=streams_path_azure_recovery, prefix=streams_path_s3_classification_to_delete, directory='deleted_project')
            shutil.rmtree(streams_path_project_classification_to_delete)
            logger.info("streams path classification -------- DELETED")
            return 1
        except Exception as e:
            logger.info("Error deleting similars project %s %s " % (project_name, e))
            return 0


# Admin APIs
def can_create_users_api(customerEmail, permission, type_user_admin, type_new_user, email, password, entreprise, nom,
                         prenom, num_tel, domaine):
    type_user_sender = db.verif_permission(customerEmail=customerEmail, type_user=type_user_admin)
    msg = "You are not allowed to create a " + type_new_user + " account"
    if (str(type_user_sender) != "Email not found") and (str(type_user_sender) != "Error"):
        if str(type_user_sender) == "admin":
            resssss = db.get_permission(type_user=type_user_sender)[0]
            for key, value in resssss[1].items():
                if key == permission and value == 1:
                    if type_new_user == "customer":

                        hash_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
                        uid = str(uuid.uuid4())
                        token = str(uuid.uuid4())
                        db.create_users_management_table()
                        test = db.add_customer(customer=entreprise, customerPassword=hash_password,
                                               customerEmail=str(email), customerJob="", customerPhone=num_tel,
                                               token=token, aboutUs="", subjectHelp="", domaine=domaine, firstName=nom,
                                               lastName=prenom, stafNumber="", apikey=uid,
                                               expiration_duration_in_hours=720, type=type_new_user)
                        if test:
                            db.commit_db_changes()

                            customer = db.get_profile(table_name=DATABASE_USERS_MANAGEMENT_TABLE_NAME,
                                                      customerEmail=email)
                            try:
                                full_url = DOMAIN + 'activate/' + urlsafe_base64_encode(
                                    force_bytes(customer[0])) + '/' + customer[12]
                            except:
                                full_url = DOMAIN + 'activate/' + urlsafe_base64_encode(
                                    force_bytes(customer[0])).decode('utf-8') \
                                           + '/' + customer[12]

                            send_inscription_email(email, full_url, password)
                            msg = email + "##" + type_new_user + "##" + entreprise + "##" + domaine
                        else:
                            msg = "Email already in use"
                    elif type_new_user in ["SN1", "SN2", "SN3", "admin"]:
                        hash_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
                        uid = str(uuid.uuid4())
                        token = str(uuid.uuid4())
                        db.create_users_management_table()
                        test = db.add_customer(customer=entreprise, customerPassword=hash_password,
                                               customerEmail=str(email), customerJob="", customerPhone=num_tel,
                                               token=token, aboutUs="", subjectHelp="", domaine=domaine, firstName=nom,
                                               lastName=prenom, stafNumber="", apikey=uid,
                                               expiration_duration_in_hours=720, type=type_new_user)
                        if test:
                            db.commit_db_changes()
                            send_inscription_email(email, "", password)

                            msg = email + "##" + type_new_user + "##" + entreprise + "##" + domaine
                        else:
                            msg = "Email already in use"

            return msg

        elif str(type_user_sender) == "SN2" or str(type_user_sender) == "SN3":
            result_permission = db.get_permission(type_user=type_user_sender)[0]
            for key, value in result_permission[1].items():
                if key == permission and value == 1:
                    if type_new_user == "customer":
                        hash_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
                        uid = str(uuid.uuid4())
                        token = str(uuid.uuid4())
                        db.create_users_management_table()
                        test = db.add_customer(customer=entreprise, customerPassword=hash_password,
                                               customerEmail=str(email), customerJob="", customerPhone=num_tel,
                                               token=token, aboutUs="", subjectHelp="", domaine=domaine, firstName=nom,
                                               lastName=prenom, stafNumber="", apikey=uid,
                                               expiration_duration_in_hours=720, type=type_new_user)
                        if test:
                            db.commit_db_changes()
                            send_inscription_email(email, "", password)
                            msg = email + "##" + type_new_user + "##" + entreprise + "##" + domaine
                        else:
                            msg = "Email already in use"

                    else:
                        msg = "You are not allowed to create a " + type_new_user + " account"
            return msg
        elif type_user_sender == "SN1":
            return msg

        elif type_user_sender == "customer":
            return msg
        else:
            return msg
    else:
        return "Please check your customer_email."


def can_edit_users_api(customerEmail, permission, type_user_admin, email, password, entreprise, nom, prenom, num_tel,
                       domaine):
    type_user_sender = db.verif_permission(customerEmail=customerEmail, type_user=type_user_admin)
    type_edit_user = db.get_type_user(customerEmail=email)
    msg = "You are not allowed to edit a " + type_edit_user + " account"
    if (str(type_user_sender) != "Email not found") and (str(type_user_sender) != "Error"):
        if type_user_sender == "admin":
            result_permission = db.get_permission(type_user= type_user_sender)[0]
            for key, value in result_permission[1].items():
                if key == permission and value == 1:
                    customer = db.get_profile(table_name=DATABASE_USERS_MANAGEMENT_TABLE_NAME,
                                              customerEmail=email)
                    if type_edit_user == "customer":
                        hash_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
                        test = db.set_all_profile(table_name=DATABASE_USERS_MANAGEMENT_TABLE_NAME,
                                                  firstName=nom, lastName=prenom,
                                                  customerJob="", customerPhone=num_tel, id=str(customer[0]),
                                                  password=hash_password, customer=entreprise, domaine=domaine)

                        if test:
                            try:
                                full_url = DOMAIN + 'activate/' + urlsafe_base64_encode(
                                    force_bytes(customer[0])) \
                                           + '/' + customer[12]
                            except:
                                full_url = DOMAIN + 'activate/' + urlsafe_base64_encode(
                                    force_bytes(customer[0])).decode('utf-8') \
                                           + '/' + customer[12]

                            send_inscription_email(email, full_url, password)
                            msg = email + "##" + type_edit_user + "##" + entreprise + "##" + domaine
                        else:
                            msg = "Email not found"
                    elif type_edit_user in ["SN1", "SN2", "SN3", "admin"]:
                        hash_password = hashlib.sha512(password.encode('utf-8')).hexdigest()

                        test = db.set_all_profile(table_name=DATABASE_USERS_MANAGEMENT_TABLE_NAME,
                                                  firstName=nom, lastName=prenom,
                                                  customerJob="", customerPhone=num_tel, id=str(customer[0]),
                                                  password=hash_password,customer=entreprise, domaine=domaine)

                        if test:
                            send_inscription_email(email, "", password)

                            msg = email + "##" + type_edit_user + "##" + entreprise + "##" + domaine
                        else:
                            msg = "Email not found"
                    elif type_edit_user == "Email not found":
                        msg = "Email not found of user that you want edit informations "
            return msg

        elif type_user_sender == "SN2" or type_user_sender == "SN3":
            result_permission = db.get_permission(type_user=type_user_sender)[0]
            for key, value in result_permission[1].items():
                if key == permission and value == 1:
                    customer = db.get_profile(table_name=DATABASE_USERS_MANAGEMENT_TABLE_NAME,
                                              customerEmail=email)
                    if type_edit_user == "customer":

                        hash_password = hashlib.sha512(password.encode('utf-8')).hexdigest()

                        test = db.set_all_profile(table_name=DATABASE_USERS_MANAGEMENT_TABLE_NAME,
                                                  firstName=nom, lastName=prenom,
                                                  customerJob="", customerPhone=num_tel, id=str(customer[0]),
                                                  password=hash_password,customer=entreprise, domaine=domaine)

                        if test is True:
                            send_inscription_email(email, "", password)

                            msg = email + "##" + type_edit_user + "##" + entreprise + "##" + domaine
                        else:
                            msg = "Email not found"

                    elif type_edit_user == "Email not found":
                        msg = "Email not found of user that you want edit informations "
                    else:
                        msg = "You are not allowed to create a " + type_edit_user + " account"
            return (msg)
        elif str(type_user_sender) == "SN1" :
            return (msg)

        elif  str(type_user_sender) == "customer" :
            return (msg)
        else:
            return (msg)
    else:
        return "Please check your customer_email."


def can_view_users_api(customerEmail, permission, type_user_admin):
    type_user_sender = db.verif_permission(customerEmail=customerEmail, type_user=type_user_admin)

    msg = "You are not allowed to view users "

    if (str(type_user_sender) != "Email not found") and (str(type_user_sender) != "Error"):
        if str(type_user_sender) == "admin":
            result_permission = db.get_permission(type_user=type_user_sender)[0]
            list_users = []
            for key, value in result_permission[1].items():
                if key == permission and value == 1:
                    list_users = db.get_users_for_admin(table_name=DATABASE_USERS_MANAGEMENT_TABLE_NAME)
            result = []
            for user in list_users:
                email = {'email': user[3]}
                type_user = {'type_user': user[21]}
                num_tel = {'num_tel': user[5]}
                apikey = {'apikey': user[13]}
                dat_expiration_apikey = {
                    'date_expiration_apikey': datetime.datetime.fromtimestamp(user[14]).strftime("%d-%m-%Y %I:%M:%S")}
                firstname = {'firstname':user[9]}
                lastname = {'lastname': user[10]}

                data = [email, type_user, num_tel, apikey, dat_expiration_apikey, firstname, lastname]
                result.append(data)
            return result
        elif str(type_user_sender) in ["customer","SN1", "SN2", "SN3"]:
            return msg
        else:
            return msg
    else:
        return "Please check your customer_email."


def can_view_customers_api(customerEmail, permission, type_user_admin):
    type_user_sender = db.verif_permission(customerEmail=customerEmail, type_user=type_user_admin)

    msg = "You are not allowed to view users "

    if (str(type_user_sender) != "Email not found") and (str(type_user_sender) != "Error"):
        if str(type_user_sender)in ["admin","customer","SN1", "SN2", "SN3"]:
            result_permission = db.get_permission(type_user=type_user_sender)[0]
            list_users = []
            for key, value in result_permission[1].items():
                if key == permission and value == 1:
                    list_users = db.get_customers(table_name=DATABASE_USERS_MANAGEMENT_TABLE_NAME)
            result = []
            for user in list_users:
                email = {'email': user[3]}
                type_user = {'type_user': user[21]}
                num_tel = {'num_tel': user[5]}
                apikey = {'apikey': user[13]}
                dat_expiration_apikey = {
                    'date_expiration_apikey': datetime.datetime.fromtimestamp(user[14]).strftime("%d-%m-%Y %I:%M:%S")}
                firstname = {'firstname':user[9]}
                lastname = {'lastname': user[10]}
                customer_name = {'customer_name': user[1]}
                customer_type = {'customer_type': user[8]}
                is_active = {'is_active': user[15]}
                data = [email, customer_name, customer_type, type_user, is_active, num_tel, apikey,
                        dat_expiration_apikey, firstname, lastname]
                result.append(data)
            return result

        else:
            return msg
    else:
        return "Please check your customer_email."


def can_update_apikey_api(customerEmail, permission, type_user_admin, email):
    type_user_sender = db.verif_permission(customerEmail=customerEmail, type_user=type_user_admin)
    info_user = db.get_info_user(customerEmail=email)
    type_user_update_apikey = info_user[0]
    customer_name = info_user[1]
    customer_type = info_user[2]

    msg = "You are not allowed to update apikey for " + type_user_update_apikey + " account"

    if (str(type_user_sender) != "Email not found") and (str(type_user_sender) != "Error"):
        if type_user_update_apikey != "Email not found":
            if str(type_user_sender) == "admin":
                result_permission = db.get_permission(type_user=type_user_sender)[0]
                for key, value in result_permission[1].items():
                    if key == permission and value == 1:
                        if type_user_update_apikey in ["customer","SN1", "SN2", "SN3", "admin"]:
                            create_or_update_user_apikey(user=customer_name, period_in_hours=720)
                            user_apikey = get_user_apikey(customer_name)
                            return customer_name + "##" + customer_type + "##" + user_apikey
            elif str(type_user_sender) == "SN2" or str(type_user_sender) == "SN3":
                resssss = db.get_permission(type_user=type_user_sender)[0]
                for key, value in resssss[1].items():
                    if key == permission and value == 1:
                        if type_user_update_apikey == "customer":
                            create_or_update_user_apikey(user=customer_name, period_in_hours=720)
                            user_apikey = get_user_apikey(customer_name)
                            return customer_name + "##" + customer_type + "##" + user_apikey
            elif str(type_user_sender) == "SN1":
                return msg
            elif str(type_user_sender) == "customer":
                return msg
            else:
                return msg
        else:
            return "The user that you want update apikey does not exist. Please ckeck the email of this user."

    else:
        return "Please check your customer_email."


def can_delete_project_api(customerEmail, permission, type_user_admin,customer_name, customer_type,project_name):
    type_user_sender = db.verif_permission(customerEmail=customerEmail, type_user=type_user_admin)

    msg = "You are not allowed to delete project "

    if (str(type_user_sender) != "Email not found") and (str(type_user_sender) != "Error"):
        if str(type_user_sender) == "admin":
            result_permission = db.get_permission(type_user=type_user_sender)[0]
            for key, value in result_permission[1].items():
                if key == permission and value == 1:
                    test = db.delete_project(table_name=STATUS_PROJECT_TABLE,
                                             customer_name=customer_name, customer_type=customer_type,
                                             project_name=project_name)
                    delete_project(customer_name, customer_type, 'similars', project_name, project_name)
                    # delete_project(customer_name, customer_type, 'classification', project_name, project_name)
                    if test:
                        msg = "Deleting project: " + project_name + " succuessfully..."
                    else:
                        msg = "Deleting project: " + project_name + " failed..."

            return msg
        elif str(type_user_sender) in ["customer", "SN1", "SN2", "SN3"]:
            return msg
        else:
            return msg
    else:
        return "Please check your customer_email."


def creation_entreprise_package(customerEmail, type_user_admin, plan_name, total,max_images_training):
    type_user_sender = db.verif_permission(customerEmail=customerEmail, type_user=type_user_admin)
    msg = "You are not allowed to create entreprise package."
    if (str(type_user_sender) != "Email not found") and (str(type_user_sender) != "Error"):
        if str(type_user_sender) == "admin":

            test = db.add_entreprise_package(table_name="plan", plan_name=plan_name, total=total,
                                             max_images_training= max_images_training )
            if test is True:
                msg = "Creation entreprise package succuessfully..."
            elif test is False:
                msg = "Plan_name already existed."
            else:
                msg = "Creation entreprise package failed..."
            return msg
        elif str(type_user_sender) in ["customer", "SN1", "SN2", "SN3"]:
            return msg
        else:
            return msg
    else:
        return "Please check your customer_email."


def delete_user_data(customer_name, customer_type):
    tables_to_delete_from = [CMS_TABLE, STATUS_PROJECT_TABLE,
                             PAYMENT_TABLE, REVIEW_TABLE, HISTORY_SEARCH_TABLE, PAYMENT_INFO]
    if db.get_customer_info_from_customer_name(customer_name):
        if db.delete_from_users_management(customer_name, customer_type):
            logger.info("Deleting_user %s with type %s from table %s"
                        % (customer_name, customer_type, DATABASE_USERS_MANAGEMENT_TABLE_NAME))
        detection_error_projects = db.select_from_status_project(customer_name, customer_type)[0] \
            if db.select_from_status_project(customer_name, customer_type) != [] \
            else db.select_from_status_project(customer_name, customer_type)
        for detection_table in detection_error_projects :
            logger.info('Deleting_detection_error_table %s' % detection_table)
            db.drop_table("predict_"+customer_type+"_"+customer_name+"_"+str(detection_table.lower()))
        for table in tables_to_delete_from:
            if db.delete_from_table(table, customer_name, customer_type):
                logger.info("Deleting_user %s with type %s from table %s" % (customer_name, customer_type, table))
            else:
                logger.info("Deleting_user %s with type %s from table %s failed" %
                            (customer_name, customer_type, table))
        db.drop_table(replace_special_caractere(customer_name).replace(' ', '_'))
        logger.info("Drop_user_table_for_similars %s" % customer_name)
        try:
            move_directory(source=AZURE_INPUT_PATH + customer_type + '/' + customer_name + '/images/',
                           new_destination="deletedUser/" + AZURE_INPUT_PATH + customer_type + '/' + customer_name +
                                           '/images/',
                           prefix=INPUT_S3 + customer_type + '/' + customer_name + '/images/',
                           directory='deleted_user')
            logger.info('Archiving input directory for client %s %s' % (customer_name, customer_type))
            move_directory(source=AZURE_OUTPUT_PATH + customer_type + '/' + customer_name + '/images/',
                           new_destination="deletedUser/" + AZURE_OUTPUT_PATH + customer_type + '/' + customer_name +
                                           '/images/',
                           prefix=OUTPUT_S3 + customer_type + '/' + customer_name + '/images/',
                           directory='deleted_user')
            logger.info('Archiving output directory for client %s %s' %(customer_name, customer_type))
            move_directory(source=AZURE_VECTORS_PATH + customer_type + '/' + customer_name,
                           new_destination="deletedUser/" + AZURE_OUTPUT_PATH + customer_type + '/' + customer_name,
                           prefix=OUTPUT_S3 + customer_type + '/' + customer_name,
                           directory='deleted_user')
            logger.info('Archiving vectors directory for client %s %s' % (customer_name, customer_type))
            move_directory(source=AZURE_TRAINING_PATH + customer_type + '/' + customer_name,
                           new_destination="deletedUser/" + AZURE_TRAINING_PATH + customer_type + '/' + customer_name,
                           prefix=TRAININGS_S3 + customer_type + '/' + customer_name,
                           directory='deleted_user')
            logger.info('Archiving training directory for client %s %s' % (customer_name, customer_type))
        except Exception as e:
            logger.warning('Deleting error %s' %e)

        return True
    else:
        return False


def delete_user_data_from_email(customer_email):
    logger.info("Starting_deleting_user_data %s " % customer_email)
    customer_name = db.get_customer_name_from_customer_email(customer_email)
    if customer_name:
        list_users = db.get_customer_info_from_customer_name(customer_name=customer_name[0])
        if list_users and len(list_users) > 1:
            if db.get_customer_info_from_customer_name(customer_name[0]):
                if db.delete_from_users_management_from_email(customer_email):
                    logger.info("Deleting_user %s with email %s from table %s"
                                % (customer_name[0], customer_email, DATABASE_USERS_MANAGEMENT_TABLE_NAME))
                    return True
        if list_users and len(list_users) == 1:
            customer_type = db.get_customer_type_from_customer_email(customer_email)
            if customer_type:
                logger.info("Delete_all_data_for_user %s with type %s" %(customer_name[0], customer_type[0]))
                return delete_user_data(customer_name[0], customer_type[0])

    else:
        return False

def can_delete_users_api(customerEmail, permission, type_user_admin, email):

    type_user_sender = db.verif_permission(customerEmail=customerEmail, type_user=type_user_admin)
    type_del_user = db.get_type_user(customerEmail=email)

    msg = "You are not allowed to delete a " + type_del_user + " account"
    if type_user_sender:
            if str(type_user_sender) == "admin":
                result_permission = db.get_permission(type_user=type_user_sender)[0][1]
                if result_permission[permission] == 1:
                    try:
                        delete_user_data_from_email(email)
                        msg = "Deleting user: " + email + " succuessfully..."
                    except Exception as e:
                        msg = "Deleting user: " + email + " failed..."
                else:
                    msg = "You are not allowed to delete a " + type_del_user + " account"
                return msg

            elif type_user_sender in ["SN2", "SN3"]:
                result_permission = db.get_permission(type_user=type_user_sender)[0][1]
                if result_permission[permission] == 1:
                    try:
                        delete_user_data_from_email(email)
                        msg = "Deleting user: " + email + " succuessfully..."
                    except Exception as e:
                        msg = "Deleting user: " + email + " failed..."
                else:
                    msg = "You are not allowed to delete a " + type_del_user + " account"
                return msg
            else:
                return msg
    else:
        return "The user that you want deleted does not exist."


def list_all_clients_with_projects():
    result = []
    response = db.select_list_all_clients_with_projects(STATUS_PROJECT_TABLE)
    try:
        df = DataFrame(response.groupby(['customer_name', 'customer_type']))
        for i in range(0, len(df)):
            customer_nametype = str(df[0][i])
            values = df[1][i]
            list_index = list(values.index)
            client_info = {'customer_name': customer_nametype.split("', '")[0].replace("('", ""),
                           'customer_type': customer_nametype.split("', '")[1].replace("')", "")}
            response = []
            for j in list_index:
                response.append({'project': values.get('project')[j], 'api': values.get('api')[j],
                                 'status': values.get('status')[j], 'name': values.get('name')[j]})
            client_info = {'customer_name': customer_nametype.split("', '")[0].replace("('", ""),
                           'customer_type': customer_nametype.split("', '")[1].replace("')", ""),
                           'projects': response}
            result.append(client_info)
    except Exception as e:
        logger.error("Error in getting user with projects %s" % e)
    return result


def get_client_statistics_admin(customer_name, customer_type):

    response1 = get_counter_of_last_four_months(customer_name, customer_type)[0]
    response2 = db.get_sum_of_counter_from_country_code(HISTORY_SEARCH_TABLE, customer_name, customer_type)
    response3 = db.get_date_and_counter_from_historic_table(HISTORY_SEARCH_TABLE, customer_name, customer_type,
                                                            str(datetime.date.today())[5:7])
    response4 = scores_repartition_per_users(customer_name, customer_type)
    response5 = db.get_reviews(customer_name, customer_type)
    requests_four_last_months = []

    reviews = []
    values = []
    keys_reviews = [1, 2, 3, 4, 5]
    total_reviews = 0
    for review in response5:
        total_reviews = total_reviews + review[1]
        values.append(review[0])
    for review in response5:
        reviews.append({"etoile": review[0], "percentage": round((review[1]/total_reviews)*100, 2)})
    for key in list(set(keys_reviews) - set(values)):
        reviews.append({"etoile": key, "percentage": 0.0})

    for i in range(0, len(response1)):
        try:
            requests_four_last_months.append({"month": response1[i][0], "number": response1[i][1]})
        except:
            requests_four_last_months.append({"month": 0, "number": 0})

    request_by_country = []
    for c in range(0, len(response2)):
        request_by_country.append({"country": response2[c][1], "number": response2[c][0]})

    score_repartition_per_user1 = {"interval": "[10% - 30%]", "number": response4[0]}
    score_repartition_per_user2 = {"interval": "[30% - 50%]", "number": response4[1]}
    score_repartition_per_user3 = {"interval": "[50% - 75%]", "number": response4[2]}
    score_repartition_per_user4 = {"interval": "[75% - 90%]", "number": response4[3]}
    score_repartition_per_user5 = {"interval": "[90% - 100%]", "number": response4[4]}
    score_repartition_per_user = [score_repartition_per_user1, score_repartition_per_user2, score_repartition_per_user3,
                                  score_repartition_per_user4, score_repartition_per_user5]
    daily_request_current_month = []
    for j in range(0, len(response3)):
        daily_request_current_month.append({"date": (response3[j][1]).strftime('%d-%m-%Y'), "number": response3[j][0]})

    result = {
        'number_of_requests_for_the_four_last_months': requests_four_last_months,
        'request_repartition':request_by_country,
        'daily_request_for_current_month': daily_request_current_month,
        'scores_repartition_per_users': score_repartition_per_user,
        'reviews': reviews
    }
    return result


def update_training_parameters(customer_name, customer_type, training_type, parameters):
    if training_type == 'similars':
        db.add_update_client_parameter(customer_name, customer_type, similars=parameters)
    elif training_type == 'classification':
        db.add_update_client_parameter(customer_name, customer_type, classification=parameters)
    else:
        return 0
    return 1


def training_parameters(customer_name, customer_type, training_type):
    training_param = db.get_training_parameters(customer_name, customer_type, training_type)
    return training_param


def historic_users_management_customer(customer_name=None, customer_type=None):
    response = db.get__historic_users_management(customer_name, customer_type)
    data_login = {}
    for res in response:
        data_login['email'] = res[0]
        data_login['customer_name'] = res[6]
        data_login['customer_type'] = res[7]
        data_login['expiration_apikey'] = datetime.datetime.fromtimestamp(res[8]).strftime("%d-%m-%Y %I:%M:%S")
        data_login['cnx_counter'] = int(res[1]) if res[1] else []
        data_login['cnx_date'] = list(res[2].split("+++")) if res[2] else []
        data_login['ip_address'] = list(res[3].split("+++")) if res[3] else []
        data_login['device'] = list(res[4].split("+++")) if res[4] else []
        data_login['city'] = list(res[5].split("+++")) if res[5] else []
    return data_login


def payment_status(customer_name, customer_type):
    try:
        pay_result = get_client_payment_status(customer_name, customer_type)
        address = db.get_client_adress(PAYMENT_INFO, customer_name, customer_type)
        if address:
            client_address = address[4] + " " + address[7] + ', ' + address[5] + " " + address[6]
        else:
            client_address = ""

        plan_details = db.get_plan_form_name(pay_result[5])
        if pay_result:
            response = {
                'choosed_plan': pay_result[5],
                'plan_details': {
                    'max_post': plan_details[5],
                    'image_products': plan_details[4],
                    'total_payment': float(plan_details[3])},
                'payment': {
                    'total': round(float(pay_result[9]), 2),
                    'payment_date': datetime.datetime.timestamp(pay_result[11]),
                    'payment_methode': pay_result[4],
                    'currency': pay_result[7],
                    'status': pay_result[8],
                    'transction_id': pay_result[6] if pay_result[6] else "",
                    'payment_address': client_address
                }
            }
        else:
            response = {
                'choosed_plan': '',
                'plan_details': {
                    'max_post': plan_details[5],
                    'image_products': plan_details[4],
                    'total_payment': float(plan_details[3])},
                'payment': {
                    'total': 0.00,
                    'payment_date': '',
                    'payment_methode': '',
                    'currency': 'eur',
                    'status': 0,
                    'transction_id': '',
                    'payment_address': client_address
                }
            }
        return response
    except Exception as e:

        return {}






def get_url_site_for_client(db, customer_name, customer_type):
    try:
        db.cursor.execute("SELECT url_shop FROM " + CMS_TABLE + " WHERE customer_name = %s AND customer_type = %s",
                      (customer_name, customer_type,))
        result = db.cursor.fetchone()
        return result[0] if result else ''

    except Exception as e:
        logger.error("Exception getting url shop for client %s type %s"  %(customer_name, customer_type))
        db.connector.rollback()


def get_as_base64(url):
    return base64.b64encode(requests.get(url).content).decode('utf-8')


def tooctet_stream(file):
    with open(file, 'rb') as in_file:
        return base64.b64encode(in_file.read())


def getting_similars_from_site(top, bottom, left, right, url_image, url_site):

    try:
        data_to_send = "--boundary_1234-abcd\r\nContent-Disposition: form-data; " \
                       "name=\"knowledgeRequest\"\r\n\r\n{\r\n    \"imageInfo\" : " \
                       "{\"url\" : \"" + url_image + "\",\"cropArea\": {\r\n\"top\": " + \
                       str(top) \
                       + ",\r\n\"bottom\": " + str(bottom) + \
                       ",\r\n\"left\": " + str(left) \
                       + ",\r\n\"right\": " + str(right) \
                       + "\r\n}},\r\n\"knowledgeRequest\" : {\"filters\" : {\"site\" : \"" + url_site \
                       + "\"}}\r\n}\r\n\r\n--boundary_1234-abcd--"

        bing_headers = {"Content-Type": "multipart/form-data",
                        "Ocp-Apim-Subscription-Key": os.environ.get('OSP_SUBSCRIPTION_KEY')}
        res = requests.post(url=url_bing,
                            data=data_to_send,
                            headers=bing_headers)
        return json.loads(res.text)
    except Exception as e:
        logger.error("Error getting_similars %s" %e)
        return {}


def image_extension(image_url):
    try:
        r = requests.head(image_url)
        return r.headers.get("content-type", "/").split('/')[1]
    except:
        if '.' in image_url.split['/'][-1]:
            return image_url.split('/')[-1].split('.')[-1]
        else:
            return 'jpeg'


def get_classification_custom_vision(customer_name, customer_type, project_name, url_image):
    headers = {
        "Prediction-Key": os.environ.get('MS_PREDICT_KEY'),
        "Content-Type": "application/octet-stream"
    }
    testing_directory_for_client = STREAMS_PATH + customer_type + '/' + customer_name + '/' + project_name + \
                                   '/testingsimilars/'
    if not os.path.isdir(testing_directory_for_client):
        try:
            os.makedirs(testing_directory_for_client)
        except Exception as e:
            logger.error("Cannot create streams directory for customer. Please verify permissions")
            pass
    hash_file =str(uuid.uuid4())
    extention = image_extension(url_image)
    file_name = hash_file + '.' + extention
    filename = download(url_image, testing_directory_for_client + file_name)
    # upload_file(filename, file_upload_s3=customer_type + '/' + customer_name + '/similars/' + project_name + '/ms_api/',
    #             file_upload_azure=AZURE_STREAMS_PATH + customer_type + '/'
    #                               + customer_name + '/similars/' + project_name +
    #                               "/ms_api/" + file_name )
    with open(filename, 'rb') as f:
        data = f.read()
    res = requests.post(url=url_ms,
                        data=data,
                        headers=headers)
    data = json.loads(res.text)
    return data.get('predictions')


def getting_similars(customer_name, customer_type, project_name, url_image, choosedbox, url_site, ip):

    category = choosedbox.get('tagName', "")
    score = choosedbox.get('probability', 0.0)
    top = float(choosedbox.get('boundingBox', {}).get('top', 0.0))
    bottom = float(choosedbox.get('boundingBox', {}).get('top', 0.0) + choosedbox.get('boundingBox', {}).get('height', 1.0))
    left = float(choosedbox.get('boundingBox', {}).get('letf', 0.0))
    right = float(choosedbox.get('boundingBox', {}).get('left', 0.0) + choosedbox.get('boundingBox', {}).get('width', 1.0))

    last_values = getting_similars_from_site(top, bottom, left, right, url_image, url_site)
    list_tags = last_values.get('tags', {})
    similars = []
    try:
        for action in list_tags:
            if 'actions' in action.keys():
                for action_type in action.get('actions'):
                    if action_type.get('actionType', '') == 'VisualSearch':
                        for value in action_type.get('data', {}).get('value', []):
                            try:
                                similars.append({'url_image': value.get('contentUrl').replace("'",""),
                                                 'url_produit': value.get('hostPageUrl').replace("'",""),
                                                 'score': 100})
                            except:
                                continue
        if category == '':
            category_to_save = {}
        else:
            category_to_save = {category: round(score, 2) * 10 * 10}

        db.insert_or_update_into_table_history(HISTORY_SEARCH_TABLE, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                               customer_name, customer_type, project_name, url_image, 'search_similars',
                                               {"similars": similars}, category_to_save,
                                               ip, (tldextract.extract(url_image)).domain, '')

    except Exception as e:
        logger.error("Exception getting_similars ms %s" % e)
    similars_dict = {"similars": similars}

    result = {"response": similars_dict}
    return result


def customer_details(data):
    logger.info(data)
    apikey = data.get('user_apikey')
    customer_info = db.get_profile_from_apikey(apikey)
    if customer_info:
        customer_name = customer_info[1]
        customer_type = customer_info[8]
        customer_email = customer_info[3]
        is_active = customer_info[15]
        if is_active == 0:
            return {"code": 403, "Message": {"response": "Unactivated account"}}
        payment_client = payment_status(customer_name, customer_type)
        if is_user_allowed(apikey) or payment_client.get('choosed_plan', 'FREE') == 'FREE':
            logger.info("Everything_is_OK, 200 client %s type %s email %s"
                        % (customer_name, customer_type, customer_email))
            return {"code": 200, "Message": {'customer_email': customer_email,
                                             'customer_name': customer_name,
                                             'customer_type': customer_type,
                                             'user_api_key': apikey}}
        else:
            logger.info("Unpaid_payment, 402 client %s type %s email %s"
                        % (customer_name, customer_type, customer_email))
            return {"code": 402, "Message": {"response": "Unpaid payment"}}

    else:
        logger.info("Client_not_found, 404 client email %s"
                    % apikey)
        return {"code": 404, "Message": {"response": "User not found"}}


def get_plan_details(plan_name):
    plan = db.get_plan_form_name(plan_name)
    try:
        response = {'plan_name': plan_name, 'total': float(plan[3]), 'max_post': plan[5], "images_product": plan[4]}
    except:
        response = {}
    return response


def update_plan_admin(plan_name, images_product, max_post, total):
    plan = db.update_plan(plan_name, images_product, max_post, total)
    return plan


def update_client_payment(customer_name, customer_type, plan_name, status):
    date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    plan = db.get_plan_form_name(plan_name)
    db.update_client_payement(customer_name, customer_type, date, plan_name, status, 'stripe', plan[3])
    return True


def get_cms_details_for_customer(customer_name, customer_type, project_name):
    result = db.get_cms_details_for_customer(CMS_TABLE, customer_name, customer_type, project_name)
    if result:
        if result[7]:
            url_confirmation = result[7]
        else:
            url_confirmation = ''
        response = {
            'customer_name': result[1],
            'customer_type': result[2],
            'url_cms': result[5],
            'access_token': result[6],
            'cms_type': result[4],
            'project_name': result[3],
            'url_confirmation': url_confirmation}
    else:
        response = {}
    return response