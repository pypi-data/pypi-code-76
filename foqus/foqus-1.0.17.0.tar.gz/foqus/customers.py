from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from foqus.cloud_configuration import *

import datetime
import uuid
import calendar
import codecs
import smtplib


# Sending emails
def send_payment_email(customer_email):
    first_name = db.get_profile(DATABASE_USERS_MANAGEMENT_TABLE_NAME, customer_email)[9]
    # logger.info("start sending email for informing_client_about_problem_shopify_payment  ...")
    server = smtplib.SMTP(SMTP_HOST, 587)
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    fromaddr = "FOQUS <hello@foqus.ai>"
    toaddr = customer_email
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = 'Mettre à jour votre payement '
    html_file = codecs.open(PATH_EMAIL_PROBLEM_SHOPIFY_PAYMENT, 'r')
    payement_url = DOMAIN + 'payement/'
    html = ((str(html_file.read()).replace("#first_name", first_name)).replace("#payement_url", payement_url))
    part2 = MIMEText(html, 'html')
    msg.attach(part2)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    logger.info("End of sending payment email to client %s" % customer_email)


def send_inscription_email(customer_email, full_url, password=None):
    try:
        server = smtplib.SMTP(SMTP_HOST, 587)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        fromaddr = "FOQUS <contact@trynfit.com>"
        toaddr = customer_email
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = 'Activez votre compte FOQUS'
        html_file = codecs.open(PATH_INSCRIPTION_EMAIL_CUSTOMER, 'r')
        if password:
            html = (str(html_file.read()).replace("#full_url", full_url).replace('#password', password))
        else:
            html = (str(html_file.read()).replace("#full_url", full_url))

        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        logger.info("End of sending inscrition email for client %s" % customer_email)
    except Exception as e:
        logger.info("exception in sending email send_inscription_email ..." + str(e))


def send_email_when_training_started(customer_name, project_name, api, subject):

    customer_profile = db.get_customer_info_from_customer_name(customer_name=customer_name)
    for custmer in customer_profile:
        customer_email = custmer[3]

        try:
            # logger.info("start sending email of starting training ...")
            server = smtplib.SMTP(SMTP_HOST, 587)
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            fromaddr = "FOQUS <hello@foqus.ai>"
            toaddr = customer_email
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = subject
            html_file = codecs.open(PATH_EMAIL_TRAINING_STARTED_CUSTOMER, 'r')
            html = ((str(html_file.read()).replace("#name", (customer_profile[0][9]))).replace("#project_name",
                                                                                               project_name)).replace(
                "#api", api)
            part2 = MIMEText(html, 'html')
            msg.attach(part2)
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            logger.info("End of sending email ")
        except Exception as e:
            logger.info("exception in sending email send_email_when_training_started..." + str(e))


def send_email_to_admin(subject, message):
    '''
       Sending to the admin an email with the error of the server
       :param subject: the subject of the email (Error server)
       :param message: the description of the error and where
       :return:
       '''
    try:
        if not LOCAL:
            # logger.info("start sending email ...")
            server = smtplib.SMTP(SMTP_HOST, 587)
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            fromaddr = "FOQUS <hello@foqus.ai>"
            toaddr = ADMIN_EMAIL
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = subject
            body = message
            msg.attach(MIMEText(body, 'plain'))
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            logger.info("End of sending email to admin ")
    except Exception as e:
        logger.info("exception in sending email to admin send_email_to_admin ..." + str(e))


def send_email(customer_name, project_name, subject):

    customer_profile = db.get_customer_info_from_customer_name(customer_name=customer_name)
    for custmer in customer_profile:
        customer_email = custmer[3]

        try:
            logger.info("start sending email ...")
            server = smtplib.SMTP(SMTP_HOST, 587)
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            fromaddr = "FOQUS <hello@foqus.ai>"
            toaddr = customer_email
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = subject
            html_file = codecs.open(PATH_EMAIL_CUSTOMER, 'r')
            html = (str(html_file.read()).replace("#name", (customer_profile[0][9]))).replace("#project_name",
                                                                                              project_name)
            part2 = MIMEText(html, 'html')
            msg.attach(part2)
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            logger.info("End of sending email ")
        except Exception as e:
            logger.info("exception in sending email send_email..." + str(e))


def send_email_of_client_inscription(customer_email, date_inscription, subject):
    '''
    Sending to the admin an email with the subscribed user
    :param customer_email: the new user email
    :param date_inscription: the date of the user inscription
    :param subject: the subject of the email (New sign up)
    :return:
    '''
    try:
        logger.info("start sending email of client inscription to admin ...")
        server = smtplib.SMTP(SMTP_HOST, 587)
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        fromaddr = "FOQUS <hello@foqus.ai>"
        toaddr = ADMIN_EMAIL
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject
        html_file = codecs.open(PATH_EMAIL_CLIENT_INSCRIPTION, 'r')
        html = ((str(html_file.read()).replace("#email", customer_email))).replace("#date", date_inscription)
        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        logger.info("End of sending email of client inscription to admin ")
    except Exception as e:
        logger.info("exception in sending email of client inscription ..." + str(e))


def send_email_for_reset_password(customer_email, full_url, first_name_of_customer, mail_subject):

    server = smtplib.SMTP(SMTP_HOST, 587)
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    try:
        fromaddr = "FOQUS <hello@foqus.ai>"
        msg = MIMEMultipart()
        msg['From'] =fromaddr
        msg['To'] = customer_email
        msg['Subject'] = mail_subject
        html_file = codecs.open(PATH_EMAIL_RESET_PASSWORD,'r')
        html = ((str(html_file.read()).replace("#full_url", full_url)).replace("#first_name", first_name_of_customer))
        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        server.sendmail(fromaddr, customer_email, msg.as_string())
        return True
    except Exception as e:

        logger.error("exception send_email_for_reset_password ......" + str(e))
        return False


def send_email_for_activate_account(first_name, customer_email, full_url):
    '''
    :param first_name: the name of the client
    :param customer_email: the email of the user that just inscripted
    :param full_url: url of activation
    :return:
    '''
    try:
        logger.info("start sending email for account activation ...")
        server = smtplib.SMTP(SMTP_HOST, 587)
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        fromaddr = "FOQUS <hello@foqus.ai>"
        toaddr = customer_email
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = 'Activate your account FOQUS'
        html_file = codecs.open(PATH_EMAIL_ACTIVATE_ACCOUNT, 'r')
        html = ((str(html_file.read()).replace("#full_url", full_url)).replace("#first_name", first_name))
        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        logger.info("End of sending inscription email to client %s" % customer_email)
    except Exception as e:
        logger.info("exception in send_email_for_activate_account ..." + str(e))


def send_email_to_client(customer_name, subject, message):
    '''
    :param customer_name: the customer name that will receive the email
    :param subject: the subject of the email
    :param message: depends on the erros that encountred when processing the shopify traning cron either no products in
    store or the number of products passes the limit of his plan
    :return: No return
    '''
    customer_profile = db.get_customer_info_from_customer_name(customer_name=customer_name)
    for custmer in customer_profile:
        customer_email = custmer[3]
        try:
            logger.info("start sending email of client inscription to admin ...")
            server = smtplib.SMTP(SMTP_HOST, 587)
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            fromaddr = "FOQUS <hello@foqus.ai>"
            toaddr = customer_email
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = subject
            html_file = codecs.open(PATH_EMAIL_TO_CLIENT, 'r')
            html = str(html_file.read()).replace("#message", message)
            part2 = MIMEText(html, 'html')
            msg.attach(part2)
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            logger.info("End of sending email to client  cron shopify")
        except Exception as e:
            logger.info("exception in sending email to client cron shopify ..." + str(e))


def create_or_update_user_apikey(user='anonymous', period_in_hours=72):
    db.update_customer(user, str(uuid.uuid4()), period_in_hours)
    db.commit_db_changes()


def update_customer_apikey(email):
    apikey = db.update_customer_apikey(email=email, apikey=str(uuid.uuid4()))
    return apikey


def specified_project_status(customer_name, customer_type, project_name):
    result = db.get_status_project(table_name=STATUS_PROJECT_TABLE, customer=customer_name,
                                   customer_type=customer_type, api="similars", project=project_name)
    return result


def create_update_project(customer, customer_type, project_to_delete, api, status,name, training_details, counter):
    table_name = STATUS_PROJECT_TABLE
    db.create_status_projects_table(table_name)
    db.insert_or_update_status_projects_table(table_name, customer, customer_type, project_to_delete, api, status,
                                              name, training_details, counter)


def is_apikey_valid(user_apikey):
    try:
        user = db.get_customer_from_apikey(apikey=user_apikey)[0]
    except:
        logger.error("APIKEY not found. Access forbidden for '" + str(user_apikey) + "'")
        return False
    return True


def is_user_allowed(user_apikey):
    try:
        user = db.get_customer_from_apikey(apikey=user_apikey)[0]
    except Exception as e:
        logger.error("exception ...................%s" % e)
        logger.error("APIKEY not found. Access forbidden for '" + str(user_apikey) + "'")
        return False

    expiration = db.get_expiration_from_apikey(apikey=user_apikey)[0]
    if time.time() > expiration:
        logger.info("User '" + user + "' is not allowed because APIKEY has expired. Expiration date: " + time.ctime(
            int(db.get_expiration_from_customer(user)[0])))
        return False
    return True


def get_apikey_expiration(user_apikey):
    try:
        user = db.get_customer_from_apikey(apikey=user_apikey)[0]
    except:
        logger.error("APIKEY not found. Access forbidden for '" + user_apikey + "'")
        return False

    expiration = db.get_expiration_from_apikey(apikey=user_apikey)[0]
    return expiration


def get_user_apikey(customer):
    try:
        user_apikey = db.get_apikey_from_customer(customer=customer)[0]
    except:
        logger.error("Customer not found. Access forbidden for '" + customer + "'")
        return None

    expiration = db.get_expiration_from_apikey(apikey=user_apikey)[0]
    if time.time() > expiration:
        logger.error("User '" + customer + "' is not allowed because APIKEY has expired. Expiration date: " +
                     time.ctime(int(db.get_expiration_from_customer(customer)[0])))
        return None
    return user_apikey


def is_customer_registered(customer):
    try:
        db.get_apikey_from_customer(customer=customer)[0]
    except:
        logger.error("Customer '" + customer + "' not found.")
        return False
    return True


def get_json_ads_number(json_input, customer_name, customer_type):
    return len(json_input[customer_name.lower() + '_' + customer_type.lower()])


def get_json_ad_status(json_input, index):
    return json_input[index]['Status']


def get_json_ad_photos(json_input, customer_name, customer_type, index):
    return json_input[customer_name.lower() + '_' + customer_type.lower()][index]['Photos']


def get_json_ad_categorie(json_input, customer_name, customer_type, index):
    return json_input[customer_name.lower() + '_' + customer_type.lower()][index]['Categorie']


def save_data_from_cms(customer_name, customer_type, project_name, cms, url_shop, access_token):
    db.create_cms_table()
    try:
        db.add_or_update_cms_table(table_name=CMS_TABLE, customer_name=customer_name,
                                   customer_type=customer_type, project_name=project_name, cms=cms, url_shop=url_shop,
                                   token=access_token)
    except Exception as e:
        logger.error("Error in saving the data from cms %s for client %s access_token %s, error %s"
                     % (cms, customer_name, access_token, e))


def scores_repartition_per_users(customer, customer_type):
    response_list = db.select_similars_classification_result(HISTORY_SEARCH_TABLE, customer, customer_type)
    nb_person_10_30 = 0
    nb_person_30_50 = 0
    nb_person_50_75 = 0
    nb_person_75_90 = 0
    nb_person_90_100 = 0
    if response_list != []:
        for j in range(0, len(response_list)):
            for i in range(0, len(response_list[j])):
                if i == 7:
                    if "similars" in response_list[j][i]:
                        similars = json.loads(response_list[j][i])
                        if similars['similars'] == []:
                            continue
                        elif int(similars["similars"][0]['score']) < 30:
                            nb_person_10_30 = nb_person_10_30 + response_list[j][9]
                        elif int(similars["similars"][0]['score']) > 30 and int(
                                similars["similars"][0]['score']) < 50:
                            nb_person_30_50 = nb_person_30_50 + response_list[j][9]
                        elif int(similars["similars"][0]['score']) > 50 and int(
                                similars["similars"][0]['score']) < 75:
                            nb_person_50_75 = nb_person_50_75 + response_list[j][9]
                        elif int(similars["similars"][0]['score']) > 75 and int(
                                similars["similars"][0]['score']) < 90:
                            nb_person_75_90 = nb_person_75_90 + response_list[j][9]
                        else:
                            nb_person_90_100 = nb_person_90_100 + response_list[j][9]
    else:
        logger.info("No historic detected")

    nb_person_list = [nb_person_10_30, nb_person_30_50, nb_person_50_75, nb_person_75_90, nb_person_90_100]
    return nb_person_list



def get_counter_of_last_four_months(customer, customer_type):
    today = datetime.date.today()
    first = today.replace(day=1)
    curr_month = str(today)[5:7]
    curr_month_year = str(today)[5:7]+'-'+str(today)[0:4]
    lastMonth = (first - datetime.timedelta(days=1)).strftime("%m")
    lastMonth_year = (first - datetime.timedelta(days=1)).strftime("%m-%Y")
    first_day_of_last_month = (first - datetime.timedelta(days=1)).replace(day=1)
    last_lastMonth = (first_day_of_last_month - datetime.timedelta(days=1)).strftime("%m")
    last_lastMonth_year = (first_day_of_last_month - datetime.timedelta(days=1)).strftime("%m-%Y")
    first_day_four_month_ago = (
        first_day_of_last_month - datetime.timedelta(days=1) - datetime.timedelta(days=1)).replace(day=1)
    fourth_month_ago = (first_day_four_month_ago - datetime.timedelta(days=1)).strftime("%m")
    fourth_month_ago_year = (first_day_four_month_ago - datetime.timedelta(days=1)).strftime("%m-%Y")
    last_four_last_months = [curr_month,lastMonth, last_lastMonth, fourth_month_ago]
    lastfour_months_year = [curr_month_year,lastMonth_year, last_lastMonth_year, fourth_month_ago_year]

    request_number = []

    for month in lastfour_months_year:
        value = db.select_utilistation_par_mois(HISTORY_SEARCH_TABLE, customer, customer_type, month)

        if value:
            request_number.append(value)
        else:
            request_number.append(0)
    nbr_requests_by_month = []
    for j in range(0, len(request_number)):
        nbr_requests_by_month.append((last_four_last_months[j], request_number[j]))


    #====================utilisation_per_periode

    last_date_in_last_month = first - datetime.timedelta(days=1)
    if str(calendar.monthrange(int(today.strftime("%Y")), int(today.strftime("%m")))[1]) == today.strftime("%d"):
        last_month_day = calendar.monthrange(int(last_date_in_last_month.strftime("%Y")), int(last_date_in_last_month.strftime("%m")))[1]
        try:
            if int(today.strftime("%m")) - 1 == 2:
                current_day_in_the_last_month = today.replace(day=28, month=int(last_date_in_last_month.strftime("%m")))
            else:
                current_day_in_the_last_month = today.replace(day=last_month_day).replace(
                    month=int(last_date_in_last_month.strftime("%m")))

        except Exception as e:
            current_day_in_the_last_month = today.replace(month=int(last_date_in_last_month.strftime("%m"))).replace(day=last_month_day)
    else:
        if int(today.strftime("%m")) - 1 == 2:
            current_day_in_the_last_month = today.replace(day=28, month=int(last_date_in_last_month.strftime("%m")))
        else:
            current_day_in_the_last_month = today.replace(month=int(last_date_in_last_month.strftime("%m")))

    utilisation_per_period = db.get_similars_request_period(HISTORY_SEARCH_TABLE, customer, customer_type, str(first),
                                                            str(today))
    utilisation_per_last_period = db.get_similars_request_period(HISTORY_SEARCH_TABLE, customer, customer_type,
                                                                 str(first_day_of_last_month),
                                                                 str(current_day_in_the_last_month))
    if not utilisation_per_period:
        user_progress_requests = 0
    elif utilisation_per_last_period:
        user_progress_requests = ((utilisation_per_period - utilisation_per_last_period) / utilisation_per_period) * 100
    else:
        user_progress_requests = 100

    user_progress_requests_3_month = db.select_utilistation_par_mois(HISTORY_SEARCH_TABLE, customer, customer_type,
                                                                     last_lastMonth_year)
    user_progress_requests_4_month = db.select_utilistation_par_mois(HISTORY_SEARCH_TABLE, customer, customer_type,
                                                                     fourth_month_ago_year)

    if not user_progress_requests_3_month:
        progress_month_3_ago = 0
    else:
        if user_progress_requests_4_month is not None:
            progress_month_3_ago = ((user_progress_requests_3_month - user_progress_requests_4_month) / user_progress_requests_3_month) * 100
        else:
            progress_month_3_ago = (user_progress_requests_3_month / user_progress_requests_3_month) * 100

    return nbr_requests_by_month, user_progress_requests, progress_month_3_ago


def user_exist(user_apikey, customer, customer_type):
    result = db.get_customer_name_and_type(apikey=user_apikey, customer=customer, customer_type=customer_type)
    if result:
        return True
    else:
        return False


def project_exist(customer_name, customer_type, api, project):
    result = db.get_project_and_status(customer=customer_name, customer_type=customer_type, api=api, project=project)
    return result


def number_request_by_week(customer, customer_type):
    today = datetime.date.today()

    current_year = str(today)[0:4]
    num_post_week = db.get_date_counter(HISTORY_SEARCH_TABLE, customer, customer_type, current_year)
    week_list_and_value = {}
    keys=[]
    values=[]
    for t in num_post_week:
        num_week =(t[1].isocalendar()[1])
        if (num_week) in week_list_and_value.keys():
            week_list_and_value[num_week] += t[0]
        else:
            week_list_and_value[num_week] = t[0]

    for key, value in sorted(week_list_and_value.items()):
        keys.append(key)
        values.append(value)

    nbr_request_by_week=[]
    for j in range(0, len(keys)):
        nbr_request_by_week.append({'week': str(keys[j]), 'number': values[j]})

    return nbr_request_by_week


def get_photos(json_input, customer_name, customer_type):
    photos = []
    try:
        for i in range(get_json_ads_number(json_input, customer_name, customer_type)):
            photos = photos + get_json_ad_photos(json_input, customer_name, customer_type, i)
    except Exception as e:
        logger.error(e)
    return photos