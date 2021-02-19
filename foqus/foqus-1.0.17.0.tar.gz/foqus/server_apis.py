
from flask import jsonify, make_response
from foqus.mqueue import *


import ast
import json
import requests
import time


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        try:
            data = json.loads(result)
            data['log_time'] = (te - ts)
            logger.info('%r  %2.2f s (try)' % (method.__name__, (te - ts)))
        except Exception as e:
            data = {}
            data['data'] = result
            data['log_time'] = (te - ts)
            logger.info('%r  %2.2f s (except)' % (method.__name__, (te - ts)))

        return data
    return timed


def format_to_json_response(response):
    response_dict = "{'Response': 'OK',\n" \
                    " 'Similars': [\n"
    for i in range(len(response)):
        if i == len(response) - 1:
            response_dict += "      '" + str(response[i]) + "'\n"
        else:
            response_dict += "      '" + str(response[i]) + "',\n"
    response_dict += "   ]\n}"

    return ast.literal_eval(response_dict)


def rest_api_request(server, request_type, user_api_key, operation, customer_name, customer_type, customer_universe,
                     project_name, body, customer_email, customer_password, type_user, first_name, last_name,
                     phone_number, job, number_of_staff, plan, cms_if_exist, url_cms, new_email, new_password,
                     new_password_verif, subject_of_email, message_email, month_num, ip, token_cms, boundingbox={}):

    try:
        # REST API tests
        s = requests.Session()
        s.auth = (customer_name, user_api_key)
        s.headers.update({'Content-Type': 'application/json'})
        data = {'user_apikey': user_api_key,
                'operation': operation,
                'customer_name': customer_name,
                'customer_type': customer_type,
                'customer_universe': customer_universe,
                'project_name': project_name,
                'customer_email': customer_email,
                'customer_password': customer_password,
                'type_user': type_user,
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': phone_number,
                'job': job,
                'number_of_staff': number_of_staff,
                'plan': plan,
                'cms_if_exist': cms_if_exist,
                'url_cms': url_cms,
                'new_email': new_email,
                'new_password': new_password,
                'new_password_verif': new_password_verif,
                'subject_of_email': subject_of_email,
                'message_email': message_email,
                'body': body,
                'month_num': month_num,
                'ip': ip,
                'token_cms': token_cms,
                'boundingbox': boundingbox if boundingbox else {}
                }

        url = server + "/api/" + operation
        if request_type.lower() == 'get':
            r = s.get(url=url, data=json.dumps(data))
        elif request_type.lower() == 'post':
            r = s.post(url=url, data=json.dumps(data))
        elif request_type.lower() == 'put':
            r = s.put(url=url, data=json.dumps(data))
        else:
            logger.error("Unsupported request type: " + str(request_type))
            return
        return r
    except:
        logger.error("No connection with the webserver")
        return make_response(jsonify({"response": "Bad request"}), 400)


# @timeit
def get_similars_if_exist(user_apikey, customer_name, customer_type, project_name, body, ip, boundingbox):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'user_apikey': user_apikey,
                                    'operation': 'get_similars_if_exist',
                                    'customer_name': customer_name,
                                    'customer_type': customer_type,
                                    'project_name': project_name,
                                    'ip': ip,
                                    'boundingbox': str(boundingbox) if boundingbox else "{}"
                                    },
                           message_body=body)

    return value.decode('utf-8')


# api_authentication
@timeit
def customer_authentication(customer_email, customer_password, body, type_user):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'customer_email': customer_email,
                                    'type_user': type_user,
                                    'operation': 'client_authentication',
                                    'customer_name': "",
                                    'customer_type': "",
                                    'user_apikey': "",
                                    'customer_password': customer_password},
                           message_body=body)
    value = value.decode('utf-8')
    return value


# api_authentication
@timeit
def get_api_key_expiration(customer_name, customer_type, user_apikey):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'customer_name': customer_name,
                                    'customer_type': customer_type,
                                    'operation': 'get_apikey_expiration',
                                    'user_apikey': user_apikey},
                           message_body="")
    value = value.decode('utf-8')
    return value


# api_inscription
@timeit
def customer_inscription(customer_email, customer_type, customer_name, body, type_user):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'customer_email': customer_email,
                                    'operation': 'client_inscription',
                                    'customer_name': customer_name,
                                    'customer_type': customer_type,
                                    'type': type_user,
                                    'user_apikey': ""},
                           message_body=body)
    value = value.decode('utf-8')
    return value


# Similarities
def process_customer_stream_from_json(user_apikey, customer_name, customer_type, project_name, body):
    my_queue_json = RabbitMQ(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                             mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD,
                             mqueue_name=MESSAGE_QUEUE_INPUT_NAME,
                             headers={'user_apikey': user_apikey,
                                      'operation': 'process_customer_stream_from_json',
                                      'customer_name': customer_name,
                                      'customer_type': customer_type,
                                      'project_name': project_name
                                      })
    my_queue_json.publish(body)


# Cms process
def process_customer_stream_cms(user_apikey, customer_name, customer_type, project_name, body):
    my_queue_json = RabbitMQ(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                             mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD,
                             mqueue_name=MESSAGE_QUEUE_INPUT_NAME,
                             headers={'user_apikey': user_apikey,
                                      'operation': 'process_customer_stream_cms',
                                      'customer_name': customer_name,
                                      'customer_type': customer_type,
                                      'project_name': project_name
                                      })
    my_queue_json.publish(body)


def shopify_training(user_apikey, customer_name, customer_type, project_name, body):
    my_queue_json = RabbitMQ(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                             mqueue_port=MESSAGE_QUEUE_PORT,
                             mqueue_user=MESSAGE_QUEUE_USER,
                             mqueue_password=MESSAGE_QUEUE_PASSWORD,
                             mqueue_name=MESSAGE_QUEUE_INPUT_NAME,
                             headers={'user_apikey': user_apikey,
                                      'operation': 'shopify_training',
                                      'customer_name': customer_name,
                                      'customer_type': customer_type,
                                      'project_name': project_name,
                                      'url_shop': body
                                      })
    my_queue_json.publish(body)


@timeit
def predict_image(user_apikey, customer_name, customer_type, body, project_name):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'user_apikey': user_apikey,
                                    'operation': 'predict_image',
                                    'customer_name': customer_name,
                                    'project_name': project_name,
                                    'customer_type': customer_type},
                           message_body=body)
    return value


@timeit
def get_historic(user_apikey, customer_name, customer_type, body, project_name, month_num):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'user_apikey': user_apikey,
                                    'operation': 'get_historic',
                                    'customer_name': customer_name,
                                    'customer_type': customer_type,
                                    'project_name': project_name,
                                    'month_num': month_num},
                           message_body=body)
    return value


def process_customer_training_classification(user_apikey, customer_name, customer_type, customer_universe, body,
                                             project_name):
    my_queue_json = RabbitMQ(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                             mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD,
                             mqueue_name=MESSAGE_QUEUE_INPUT_NAME,
                             headers={'user_apikey': user_apikey,
                                      'operation': 'process_customer_training_classification',
                                      'customer_name': customer_name,
                                      'customer_type': customer_type,
                                      'project_name': project_name,
                                      'customer_universe': customer_universe})
    my_queue_json.publish(body)


def get_historic_client(customer_name, customer_type):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'get_historic_client',
                                    'customer_name': customer_name,
                                    'customer_type': customer_type},
                           message_body='')

    return value

@timeit
def get_list_all_clients_with_projects(body):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={
        'operation': 'get_list_all_clients_with_projects'
    },
        message_body=body)
    return value


def get_number_post_per_clients(body):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={
        'operation': 'get_number_post_per_clients'
    },
        message_body=body)
    return value


def update_user_apikey(customer_name, customer_type, body):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'update_user_apikey',
                                    'customer_name': customer_name,
                                    'customer_type': customer_type
                                    },
                           message_body=body)
    value = value.decode('utf-8')
    return value


@timeit
def get_specified_project_status(user_apikey, customer_name, customer_type, project_name, body):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'get_specified_project_status',
                                    'customer_name': customer_name,
                                    'customer_type': customer_type,
                                    'project_name': project_name,
                                    'user_apikey': user_apikey
                                    },
                           message_body=body)
    value = value.decode('utf-8')
    return value


# new functions
def get_client_payment_status(customer_name, customer_type):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'get_client_payment_status',
                                    'customer_name': customer_name,
                                    'customer_type': customer_type
                                    },
                           message_body="")

    value = value.decode('utf-8')
    return value

@timeit
def get_payment_status_for_client(user_apikey, customer_name, customer_type):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'get_payment_status_for_client',
                                    'user_apikey': user_apikey,
                                    'customer_name': customer_name,
                                    'customer_type': customer_type
                                    },
                           message_body="")

    value = value.decode('utf-8')
    return value


@timeit
def get_client_statistics(user_apikey, customer_name, customer_type):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'get_client_statistics',
                                    'customer_name': customer_name,
                                    'user_apikey': user_apikey,
                                    'customer_type': customer_type
                                    },
                           message_body="")
    value = value.decode('utf-8')
    return value


def get_statistics_for_admin(customer_name, customer_type):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'get_statistics_for_admin',
                                    'customer_name': customer_name,
                                    'customer_type': customer_type},
                           message_body='')
    value = value.decode('utf-8')
    return value


def all_historic_users_management(body):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'all_historic_users_management'
                                    },
                           message_body=body)
    value = value.decode('utf-8')
    return value


@timeit
def get_details_trainings_for_client(user_apikey, customer_name, customer_type, project_name):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'get_details_trainings_for_client',
                                    'customer_name': customer_name,
                                    'user_apikey': user_apikey,
                                    'customer_type': customer_type,
                                    'project_name': project_name
                                    },
                           message_body="")

    value = value.decode('utf-8')
    return value


def get_details_trainings_for_admin(customer_name, customer_type, project_name):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'get_details_trainings_for_admin',
                                    'customer_name': customer_name,
                                    'customer_type': customer_type,
                                    'project_name': project_name},
                           message_body='')
    value = value.decode('utf-8')
    return value

# api_can_create_users
def can_create_users(customer_email, body, type_user, type_new_user, email, password, entreprise, nom, prenom,
                     num_tel, domaine):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'customer_email': customer_email,
                                    'type_user': type_user,
                                    'type_new_user': type_new_user,
                                    'email': email,
                                    'password': password,
                                    'entreprise': entreprise,
                                    'nom': nom,
                                    'prenom': prenom,
                                    'num_tel': num_tel,
                                    'domaine': domaine,
                                    'operation': 'can_create_users',
                                    'customer_name': "",
                                    'customer_type': "",
                                    'user_apikey': ""},
                           message_body=body)
    value = value.decode('utf-8')
    return value


def can_delete_users(customer_email, body, type_user, email):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'customer_email': customer_email,
                                    'type_user': type_user,
                                    'email': email,
                                    'operation': 'can_delete_users',
                                    'customer_name': "",
                                    'customer_type': "",
                                    'user_apikey': ""},
                           message_body=body)
    value = value.decode('utf-8')
    return value


def can_edit_users(customer_email, body, type_user, email, password, entreprise, nom, prenom, num_tel, domaine):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'customer_email': customer_email,
                                    'type_user': type_user,
                                    'email': email,
                                    'password': password,
                                    'entreprise': entreprise,
                                    'nom': nom,
                                    'prenom': prenom,
                                    'num_tel': num_tel,
                                    'domaine': domaine,
                                    'operation': 'can_edit_users',
                                    'customer_name': "",
                                    'customer_type': "",
                                    'user_apikey': ""},
                           message_body=body)
    value = value.decode('utf-8')
    return value


def can_view_users(customer_email, body, type_user):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'customer_email': customer_email,
                                    'type_user': type_user,
                                    'operation': 'can_view_users',
                                    'customer_name': "",
                                    'customer_type': "",
                                    'user_apikey': ""},
                           message_body=body)
    value = value.decode('utf-8')
    return value


def can_view_customers(customer_email, body, type_user):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                                 mqueue_port=MESSAGE_QUEUE_PORT,
                                 mqueue_user=MESSAGE_QUEUE_USER,
                                 mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'customer_email': customer_email,
                                    'type_user': type_user,
                                    'operation': 'can_view_customers',
                                    'customer_name': "",
                                    'customer_type': "",
                                    'user_apikey': ""},
                           message_body=body)
    value = value.decode('utf-8')
    return value


def can_update_apikey(customer_email, type_user, email, body):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'customer_email': customer_email,
                                    'type_user': type_user,
                                    'operation': 'can_update_apikey',
                                    'email': email},
                           message_body=body)
    value = value.decode('utf-8')
    return value


def can_delete_project(customer_email, type_user, customer_name, customer_type, project_name, body):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'customer_email': customer_email,
                                    'type_user': type_user,
                                    'operation': 'can_delete_project',
                                    'project_name': project_name,
                                    'customer_name': customer_name,
                                    'customer_type': customer_type},
                           message_body=body)
    value = value.decode('utf-8')
    return value


def creation_entreprise_package(customer_email, type_user, plan_name, total, max_images_training, body):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'customer_email': customer_email,
                                    'type_user': type_user,
                                    'operation': 'creation_entreprise_package',
                                    'plan_name': plan_name,
                                    'total': total,
                                    'max_images_training': max_images_training},
                           message_body=body)
    value = value.decode('utf-8')
    return value


def get_all_plans_payement(customer_email, type_user, body):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'customer_email': customer_email,
                                    'type_user': type_user,
                                    'operation': 'get_all_plans_payement'},
                           message_body=body)
    value = value.decode('utf-8')
    
    return value


def all_status_projects(customer_name, customer_type, body):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'all_status_projects',
                                    'customer_name': customer_name,
                                    'customer_type': customer_type
                                    },
                           message_body=body)
    value = value.decode('utf-8')
    return value


@timeit
def all_status_project(user_apikey, customer_name, customer_type):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'all_status_project',
                                    'customer_name': customer_name,
                                    'user_apikey': user_apikey,
                                    'customer_type': customer_type},
                           message_body='')
    return value.decode("utf-8")


@timeit
def customer_info(data):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'get_customer_info',
                                    'data': data},
                           message_body='')

    return value.decode("utf-8")


@timeit
def save_client_reviews(user_apikey, customer_name, customer_type, body, project_name, review, url_image):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'user_apikey': user_apikey,
                                    'operation': 'save_client_reviews',
                                    'customer_name': customer_name,
                                    'project_name': project_name,
                                    'customer_type': customer_type,
                                    'review': review,
                                    'url_image': url_image},
                           message_body=body)
    return value.decode('utf-8')


@timeit
def customer_registration(customer_email, customer_type, customer_name, customer_password, first_name, last_name,
                          phone_number, job, number_of_staff, plan, cms_if_exist, url_cms, token_cms):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'customer_email': customer_email,
                                    'operation': 'customer_registration',
                                    'customer_name': customer_name,
                                    'customer_type': customer_type,
                                    'customer_password': customer_password,
                                    'first_name': first_name,
                                    'last_name': last_name,
                                    'phone_number': phone_number,
                                    'job': job,
                                    'number_of_staff': number_of_staff,
                                    'plan': plan,
                                    'cms_if_exist': cms_if_exist,
                                    'url_cms': url_cms,
                                    'token_cms': token_cms
                                    },
                           message_body="")

    value = value.decode('utf-8')
    return value


def update_profile(customer_email, customer_name, first_name, last_name,
                   phone_number, job, new_email):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'customer_email': customer_email,
                                    'operation': 'update_profile',
                                    'customer_name': customer_name,
                                    'first_name': first_name,
                                    'last_name': last_name,
                                    'phone_number': phone_number,
                                    'job': job,
                                    'new_email': new_email},
                           message_body="")

    value = value.decode('utf-8')
    return value


def change_password(customer_email, customer_password, new_password, new_password_verif):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'customer_password': customer_password,
                                    'operation': 'change_password',
                                    'new_password': new_password,
                                    'new_password_verif': new_password_verif,

                                    'customer_email': customer_email
                                    },
                           message_body="")

    value = value.decode('utf-8')
    return value


def forget_password(customer_email):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'forget_password',
                                    'customer_email': customer_email
                                    },
                           message_body="")

    value = value.decode('utf-8')
    return value


def contact(first_name, customer_email, subject_of_email, message_email):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'contact',
                                    'first_name': first_name,
                                    'customer_email': customer_email,
                                    'subject_of_email': subject_of_email,
                                    'message_email': message_email
                                    },
                           message_body="")

    value = value.decode('utf-8')
    return value


@timeit
def get_connected_customer_info(customer_email):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'get_connected_customer_info',
                                    'customer_email': customer_email},
                           message_body='')

    return value.decode("utf-8")


@timeit
def get_connected_customer_cms_info(customer_name, customer_type, cms):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'get_connected_customer_cms_info',
                                    'customer_name': customer_name,
                                    'customer_type': customer_type,
                                    'cms': cms},
                           message_body='')
    return value.decode("utf-8")


def delete_user_data(customer_name, customer_type):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'customer_name': customer_name,
                                    'customer_type': customer_type,
                                    'operation': 'delete_user_data'},
                           message_body="")
    value = value.decode('utf-8')
    return value


def delete_user_data_from_email(customer_email):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'customer_email': customer_email,
                                    'operation': 'delete_user_data_from_email'},
                           message_body="")
    value = value.decode('utf-8')
    return value

@timeit
def all_user_projects(customer_name, customer_type, api):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'all_user_projects',
                                    'customer_name': customer_name,
                                    'customer_type': customer_type,
                                    'body': api},
                           message_body='')

    return value.decode("utf-8")


@timeit
def manage_project(customer_name, customer_type, api, project_name, project_id, operation):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': operation,
                                    'customer_name': customer_name,
                                    'customer_type': customer_type,
                                    'project_name': project_name,
                                    'project_id': project_id,
                                    'body': api},
                           message_body='')

    return value.decode("utf-8")

@timeit
def payment_client(customer_name, customer_type, user_apikey, email,  plan_name, methode_payment, operation, payment_id,
                   payer_id, stripe_token):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    headers = {'operation': operation,
               'customer_name': customer_name,
               'customer_type': customer_type,
               'customer_email': email,
               'user_apikey': user_apikey,
               'plan_name': plan_name,
               'methode_payment': methode_payment,
               'payment_id': payment_id,
               'payer_id': payer_id,
               'stripe_token': stripe_token}
    value = rpc_queue.call(headers=headers,
                           message_body='')
    return value.decode("utf-8")

@timeit
def payment_shopify(customer_name, customer_type, user_apikey, email,  plan_name, url_cms, token_cms, operation):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    headers = {'operation': operation,
               'customer_name': customer_name,
               'customer_type': customer_type,
               'customer_email': email,
               'user_apikey': user_apikey,
               'plan_name': plan_name,
               'url_cms': url_cms,
               'token_cms': token_cms}
    value = rpc_queue.call(headers=headers,
                           message_body='')
    return value.decode("utf-8")


@timeit
def payment_info_client(customer_name, customer_type, user_apikey, name,  address, zipcode, country, city, tva_number,
                                 operation):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    headers = {'operation': operation,
               'customer_name': customer_name,
               'customer_type': customer_type,
               'name': name,
               'user_apikey': user_apikey,
               'address': address,
               'zipcode': zipcode,
               'country': country,
               'city': city,
               'tva_number': tva_number}
    value = rpc_queue.call(headers=headers,
                           message_body='')
    return value.decode("utf-8")

@timeit
def payment_details_client(customer_name, customer_type, user_apikey, choosed_plan, operation):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    headers = {'operation': operation,
               'customer_name': customer_name,
               'customer_type': customer_type,
               'choosed_plan': choosed_plan,
               'user_apikey': user_apikey}
    value = rpc_queue.call(headers=headers,
                           message_body='')
    return value.decode("utf-8")


def get_client_training_parameters(customer_name, customer_type, training_type):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'customer_name': customer_name,
                                    'customer_type': customer_type,
                                    'training_type': training_type,
                                    'operation': 'training_parameters_client'},
                           message_body="")
    value = value.decode('utf-8')
    return value


def update_client_training_parameters(customer_name, customer_type, training_type, parameters):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'customer_name': customer_name,
                                    'customer_type': customer_type,
                                    'training_type': training_type,
                                    'parameters': parameters,
                                    'operation': 'update_training_parameters_client'},
                           message_body="")
    value = value.decode('utf-8')
    return value


def all_historic_users_management_customer(body, customer_name=None, customer_type=None):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'all_historic_users_management_customer',
                                    'customer_name': customer_name if customer_name else None,
                                    'customer_type': customer_type if customer_type else None,
                                    },
                           message_body=body)
    value = value.decode('utf-8')
    return value

@timeit
def customer_data(data):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'get_customer',
                                    'data': data},
                           message_body='')

    return value.decode("utf-8")


@timeit
def update_customer_apikey(customer_email, user_apikey):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'update_customer_apikey',
                                    'customer_email': customer_email,
                                    "user_apikey" :  user_apikey},
                           message_body='')

    return value.decode("utf-8")

def get_plan_details(plan_name):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'get_plan_details',
                                    'plan_name': plan_name},
                           message_body='')
    value = value.decode('utf-8')
    return value


def update_plan_admin(plan_name, images_products, max_post, total):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS,
                          mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER,
                          mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'update_plan_admin',
                                    'plan_name': plan_name,
                                    'images_product': images_products,
                                    'max_post': max_post,
                                    'total': total},
                           message_body='')
    value = value.decode('utf-8')
    return value


def detect_objects_image(user_apikey, customer_name, customer_type, project_name, body, ip):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'user_apikey': user_apikey,
                                    'operation': 'detect_objects_image',
                                    'customer_name': customer_name,
                                    'customer_type': customer_type,
                                    'project_name': project_name,
                                    'ip': ip
                                    },
                           message_body=body)
    value = value.decode('utf-8')
    list_value = value.replace('[', '').replace(']', '').split('}}, ')
    list_bound_box = []
    for probability in list_value:
        probability = probability if probability.endswith('}}') else probability + "}}"
        probability = json.loads(probability.replace("'", '"'))
        list_bound_box.append(probability)

    return list_bound_box

@timeit
def get_customer_cms_infos(customer_name, customer_type, project_name):
    rpc_queue = RpcClient(mqueue_address=MESSAGE_QUEUE_ADDRESS, mqueue_port=MESSAGE_QUEUE_PORT,
                          mqueue_user=MESSAGE_QUEUE_USER, mqueue_password=MESSAGE_QUEUE_PASSWORD)
    value = rpc_queue.call(headers={'operation': 'get_customer_cms_info',
                                    'customer_name': customer_name,
                                    'customer_type': customer_type,
                                    'project_name': project_name},
                           message_body='')
    return value.decode("utf-8")