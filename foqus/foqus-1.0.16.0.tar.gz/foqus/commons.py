from foqus.cloud_configuration import *
from foqus.customers import create_or_update_user_apikey, create_update_project, get_user_apikey, \
    send_email_to_admin, send_payment_email, get_json_ads_number, get_json_ad_photos
from foqus.server_apis import shopify_training
from foqus.payments import create_plan_stripe

from ip2geotools.databases.noncommercial import DbIpCity

if not LOCAL:
    from tensorflow.keras.utils import multi_gpu_model

from currency_converter import CurrencyConverter
from tensorflow.keras import models, layers, optimizers
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image
from math import ceil
from multiprocessing.pool import ThreadPool, TimeoutError

from PIL import Image
from io import BytesIO

import urllib.request
import urllib.parse

import calendar
import datetime
import hashlib
import imghdr
import os
import requests
import time
import uuid
import json

import dask.dataframe as dd
import numpy as np


price_converter = CurrencyConverter()


class MultiTaskPool:
    def __init__(self):
        self.pool = ThreadPool(processes=MAX_ALLOWED_THREADS)
        self.async_results = []
        return

    def push_thread(self, thread, args):
        self.async_results.append(
            self.pool.apply_async(func=thread, args=args))

        return self.get_tasks_count() - 1

    def pop_thread(self, index):
        try:
            response = self.async_results[index].get(timeout=THREAD_RESPONSE_TIMEOUT_IN_SECONDS)
            del self.async_results[index]
            logger.info("Removing thread index: " + str(index))
        except TimeoutError:
            logger.warning("Thread still running! Index: " + str(index))
            response = None
        except:
            response = None
        return response

    def get_tasks_count(self):
        return len(self.async_results)

    def clean_pool(self):
        for i in range(self.get_tasks_count()):
            self.pop_thread(i)


def replace_special_caractere(chaine_to_replace=''):
    '''
    :param chaine_to_replace: str that may contains special caracters
    :return: str with no special caracters (all are replaced)
    '''
    list_caracters = [(['ê', 'ë', 'é', 'è'], 'e'), (['ç'], 'c'), (['ä', 'å', 'ã', 'à'], 'a'),
                      (['í', 'î', 'ì', 'î', 'ï'], 'i'),
                      (['ñ'], 'n'), (['ó', 'ò', 'ô', 'ö', 'õ', 'ø'], 'o'), (['š', 's']), (['ú', 'ù', 'û', 'ü'], 'u'),
                      (['ý', 'ÿ'], 'y'), (['ž'], 'z'), (['œ'], 'oe'), (['æ'], 'ae'),
                      (['*', '#', '~', '&', '´', '^', '|', '[', '(', '{', ';', '?', ':', '=', '+', '²', '%', 'µ', '$',
                        '£', '¨', '!', ']', '}', '@', '/', "'", '"', ',', ';', '§', '<', '>', ')', '_', '-', '.', '°',
                        "’", "́", "̀"], '')]
    buckwalterMod = {
        'ء': 'a', 'ا': 'a', 'إ': 'i',
        'أ': 'a', 'آ': 'a', 'ب': 'b',
        'ة': 't', 'ت': 't', 'ث': 'th',
        'ج': 'j', 'ح': 'H', 'خ': 'kh',
        'د': 'd', 'ذ': 'dh', 'ر': 'r',
        'ز': 'z', 'س': 's', 'ش': 'ch',
        'ص': 's', 'ض': 'dh', 'ط': 't',
        'ظ': 'dh', 'ع': 'a', 'غ': 'gh',
        'ف': 'f', 'ق': 'q', 'ك': 'k',
        'ل': 'l', 'م': 'm', 'ن': 'n',
        'ه': 'h', 'ؤ': 'o', 'و': 'w',
        'ى': 'y', 'ئ': 'i', 'ي': 'y',
    }
    for charcter in chaine_to_replace:
        if charcter in buckwalterMod.keys():
            chaine_to_replace = chaine_to_replace.replace(charcter, buckwalterMod[charcter])
    chaine_to_replace = chaine_to_replace.lower()
    for caracter in chaine_to_replace:
        for list_special in list_caracters:
            if caracter in list_special[0]:
                chaine_to_replace = chaine_to_replace.replace(str(caracter), str(list_special[1]))
    return chaine_to_replace


def update_the_database(db, filename):
    '''
    :param db: the database
    :param filename: the image to move to history (pub no active any more)
    :return: True if everything works fine elsa False
    '''
    try:
        url = db.get_url_from_hash(hash=filename.split("/")[-1])
        db.create_history_table(table_name=filename.split('/')[-3])
        db.create_or_update_history(table_name=filename.split('/')[-3], url=url)
        db.delete_hash(hash=filename.split('/')[-1])
        db.delete_smilitaries(table_name=filename.split('/')[-3], url=url)
        # logger.info("Successfully updated database  ")
        return True
    except Exception as e:
        logger.error("Erreur updating the database ... (%s) " % e)
        return False


def download(url, filename):
    '''
    :param url: url of the file to download
    :param filename: the file name to download to
    :return:
    '''
    # As long as the file is opened in binary mode, both Python 2 and Python 3
    # can write response body to it without decoding.
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent',
                          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/83.0.4103.97 Safari/537.36')

    try:
        res = all(ord(c) < 128 for c in url)
        if res:
            filename, headers = opener.retrieve(url.replace(' ', '+'), filename)
        else:
            url = urllib.parse.urlparse(url)
            url = url.scheme + "://" + url.netloc + urllib.parse.quote(url.path)
            filename, headers = opener.retrieve(url.replace(' ', '+'), filename)
        return filename
    except Exception as e:
        logger.error("Error when downloading/writing download 1 file %s error %s ..." % (filename, e))
    url_extension = image_extension(url)
    real_extension = imghdr.what(filename)
    if real_extension != url_extension:
        file_hash = filename.split('.')[0]
        try:
            res = all(ord(c) < 128 for c in url)
            if res:
                # urllib.request.urlretrieve(url.replace(' ', '+'), )
                opener.retrieve(url.replace(' ', '+'), file_hash + '.' + real_extension)
            else:
                url = urllib.parse.urlparse(url)
                url = url.scheme + "://" + url.netloc + urllib.parse.quote(url.path)
                # urllib.request.urlretrieve(url.replace(' ', '+'), file_hash + '.' + real_extension)
                opener.retrieve(url.replace(' ', '+'), file_hash + '.' + real_extension)
            return file_hash + '.' + real_extension
        except Exception as e:
            logger.error("Error when downloading/writing download 2 file %s error %s ..."
                         % (file_hash + '.' + real_extension, e))
            return None


def can_be_downloaded(url):
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent',
                     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/83.0.4103.97 Safari/537.36')
    try:
        if url.lower().endswith(('.png', '.jpg', '.jpeg')):
            extension = (url.split('/')[-1]).split('.')[-1]
            filename = (url.split('/')[-1]).split('.')[-2] + '.' + extension
        else:
            extension = image_extension(str(url))
            filename = (url.split('/')[-1]) + '.' + extension
        res = all(ord(c) < 128 for c in url)
        if res:
            opener.retrieve(url.replace(' ', '+'), filename)
            os.remove(filename)
            return True
        else:
            url = urllib.parse.urlparse(url)
            url = url.scheme + "://" + url.netloc + urllib.parse.quote(url.path)
            opener.retrieve(url.replace(' ', '+'), filename)
            os.remove(filename)
            return True
    except Exception as e:
        logger.error("Error when downloading/writing_can_be_downloaded function file %s error %s ..." % (url, e))
        return False


def remove(db, filename):
    update_the_database(db, filename)
    try:
        if os.path.exists(filename):
            os.remove(filename)
            return 0
        else:
            # logger.info("File doesn't exist... Nothing to remove")
            return -1
    except:
        logger.error("Error when removing file '" + filename + "'...")
        return -1


def get_file_hash(filename):
    hash_result = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_result.update(chunk)
    return hash_result.hexdigest()


def get_remote_file_hash(url):
    try:
        temporary_file = '/tmp/' + str(uuid.uuid4())
        download(url, temporary_file)
        file_hash = get_file_hash(temporary_file)
        os.remove(temporary_file)
        return file_hash
    except:
        logger.error("Error when trying to calculate REMOTE file hash")
        return None


def image_extension(image_url):
    try:
        r = requests.head(image_url)
        ext = r.headers.get("content-type", "/").split('/')[1]
        return ext if ext in ['jpg', 'jpeg', 'png'] else 'jpeg'
    except:
        return image_url.split('.')[-1]


def resize_and_retrieve(url, filename):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img = img.resize((TARGET_RESOLUTION, TARGET_RESOLUTION))
        img.save(filename)
    except Exception as e:
        logger.error("Error when resizing and downloading file %s error %s ..."
                     % (url, e))


def download_resized_image(url, filename):
    '''
    :param url: url of the file to download
    :param filename: the file name to download to
    :return:
    '''
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent',
                     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/83.0.4103.97 Safari/537.36')
    # As long as the file is opened in binary mode, both Python 2 and Python 3
    # can write response body to it without decoding.
    # logger.info("******** Downloading image..")
    start = time.process_time()
    try:
        res = all(ord(c) < 128 for c in url)
        if res:
            resize_and_retrieve(url.replace(' ', '+'), filename)
        else:
            url = urllib.parse.urlparse(url)
            url = url.scheme + "://" + url.netloc + urllib.parse.quote(url.path)
            resize_and_retrieve(url.replace(' ', '+'), filename)
        # logger.info("*** download time taken" + str(time.process_time() - start))
        return filename
    except Exception as e:
        logger.error("Error when downloading/writing download_resized_image 1 file %s error %s ..." % (filename, e))
    try:
        url_extension = image_extension(url)
        real_extension = imghdr.what(filename)
    except Exception as e:
        # logger.info("Exception file %s " % e)
        return None
    if real_extension != url_extension:
        file_hash = filename.split('.')[0]
        try:
            res = all(ord(c) < 128 for c in url)
            if res:
                # opener.retrieve(url.replace(' ', '+'), file_hash + '.' + real_extension)
                resize_and_retrieve(url.replace(' ', '+'), file_hash + '.' + real_extension)
                # urllib.request.urlretrieve(url.replace(' ', '+'), file_hash + '.' + real_extension)
            else:
                url = urllib.parse.urlparse(url)
                url = url.scheme + "://" + url.netloc + urllib.parse.quote(url.path)
                resize_and_retrieve(url.replace(' ', '+'), file_hash + '.' + real_extension)
            # logger.info("*** download time taken" + str(time.process_time() - start))
            return file_hash + '.' + real_extension
        except Exception as e:
            logger.error("Error when downloading/writing file download_resized_image 2 %s error %s ..."
                         % (file_hash + '.' + real_extension, e))
            return None


def products_related_data(url_images, url_produits, each_picture, url_product, url_mobile_product, product_id, path,
                          customer_name, customer_type, project_name):
    if url_product != '' and url_product in url_produits.keys():
        reference = url_produits[url_product]['images']
        new_reference = reference + " " + each_picture
        url_produits[url_product] = {"product_id": product_id,
                                     "product_url_mobile": url_mobile_product,
                                     "images": new_reference,
                                     "path": path,
                                     "customer_name": customer_name,
                                     "customer_type": customer_type,
                                     "project_name": project_name}
    elif url_product != '':
        url_produits[url_product] = {"product_id": product_id,
                                     "product_url_mobile": url_mobile_product,
                                     "images": each_picture,
                                     "path": path,
                                     "customer_name": customer_name,
                                     "customer_type": customer_type,
                                     "project_name": project_name}
    else:
        url_images.append({"images": each_picture,
                           "path": path,
                           "customer_name": customer_name,
                           "customer_type": customer_type,
                           "project_name": project_name,
                           "product_id": product_id,
                           "product_url_mobile": url_mobile_product})


def download_commit_db_images(url_images, url_produits):
    if url_images:
        for image in url_images:
            try:
                download_or_remove(image.get('images', ''), "", image.get("product_id", ),
                                   image.get("product_url_mobile", ""), image.get("customer_name"),
                                   image.get('customer_type'), image.get('path'), image.get('project_name'))
            except Exception as e:
                logger.error(
                    'Error_url_images_download_commit_db_images_count %s downloading image %s continue' % (e, image))
    else:
        for product in url_produits.keys():
            try:
                download_or_remove(url_produits.get(product, {}).get('images', ''), product,
                                   url_produits.get(product, {}).get("product_id"),
                                   url_produits.get(product, {}).get("product_url_mobile"),
                                   url_produits.get(product, {}).get("customer_name"),
                                   url_produits.get(product, {}).get('customer_type'),
                                   url_produits.get(product, {}).get('path'),
                                   url_produits.get(product, {}).get('project_name'))
            except Exception as e:
                logger.error('Error_url_produits_download_commit_db_images_cont %s downloading image %s continue' %
                             (e, url_produits[product]['images']))
    db.commit_db_changes()


def download_or_remove(urls, each_url_product, product_id, product_url_mobile, customer_name=None, customer_type=None, path_out=None,
                       project_name=None):

    if customer_name is None or customer_type is None or db is None:
        logger.error("Cannot download image: missing parameters")
        return
    if path_out is None:
        path_out = OUTPUT_PATH + customer_type + '/' + customer_name + '/images/' + project_name
    input_s3 = OUTPUT_S3 + customer_type + '/' + customer_name + '/images/' + project_name + '/'
    input_azure = AZURE_OUTPUT_PATH + customer_type + "/" + customer_name + "/images/" + project_name + '/'
    hash_files = ""
    for url in urls.split(' '):
        hash_file = get_remote_file_hash(url)
        extention = image_extension(url)
        filename = hash_file + '.' + extention
        fichier = path_out + '/' + filename
        logger.info("Retrieving image from URL...")

        db.create_client_products_table(replace_special_caractere(customer_name).replace(' ', '_'))

        if os.path.exists(fichier) and os.stat(fichier).st_size != 0:
            logger.info("File exists and not empty... Ignoring download.")
        elif os.path.exists(fichier) and os.stat(fichier).st_size == 0:
            logger.info("File exists but size is 0... Download again!")
            start = time.process_time()
            download_resized_image(url, fichier)
            logger.info("*** download time taken" + str(time.process_time() - start))
        else:
            logger.info("File doesn't exist... Downloading...")
            download_resized_image(url, fichier)
        if fichier.split('/')[-2] == project_name:
            file_azure = input_azure + fichier.split('/')[-1]
        else:
            file_azure = input_azure + fichier.split('/')[-2] + '/' + fichier.split('/')[-1]
        upload_file(file_local_path=fichier, file_upload_s3=input_s3 + fichier.split('/')[-2] + '/',
                    file_upload_azure=file_azure)

        hash_files = hash_files + hash_file + " "
        data_product = db.get_product_details(replace_special_caractere(customer_name).replace(' ', '_'),
                                              each_url_product,
                                              project_name)
        if data_product:
            hash_base = data_product[3]
            urls_references_base = data_product[1].split(' ')
            hash_references_base = data_product[3].split(' ')
            urls_references = urls.split(' ')
            hash_references = hash_files.split(' ')
            # hash_references = list(dict.fromkeys(hash_references))
            for i in range(0, len(urls_references) - 1):
                for j in range(0, len(urls_references_base) - 1):
                    if urls_references[i] == urls_references_base[j]:
                        if hash_references[i] != hash_references_base[j]:
                            # urls_base.replace(urls_references_base[j], urls_references[i])
                            hash_base.replace(hash_references_base[j], hash_references[j])
            # Url image has been changed
            for i in range(0, len(hash_references) - 1):
                for j in range(0, len(hash_references_base) - 1):
                    if hash_references[i] not in hash_references_base:
                        hash_references_base.append(hash_references[i])
                        urls_base = urls + urls_references_base[j] + " "
                    if hash_references[i] == hash_references_base[j]:
                        if urls_references[i] != urls_references_base[j]:
                            urls.replace(urls_references_base[j], urls_references[i])

        if each_url_product == '':
            db.add_or_update_images(table_name=replace_special_caractere(customer_name).replace(' ', '_'),
                                    reference=urls, urlProduit="", product_id=product_id,
                                    hash_code=hash_files, project_name=project_name,
                                    product_mobile_url=product_url_mobile)
        else:
            db.add_or_update_products(table_name=replace_special_caractere(customer_name).replace(' ', '_'),
                                      reference=urls, urlProduit=each_url_product, product_id=product_id,
                                      product_url_mobile=product_url_mobile, hash_code=hash_files,
                                      project_name=project_name, update=data_product)


def get_client_ip(request_client):
    '''

    :param request_client: the request of the view
    :return:
    '''
    x_forwarded_for = request_client.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request_client.META.get('REMOTE_ADDR')
    return ip


def get_client_code_country(adress):
    try:
        response = DbIpCity.get(adress, api_key='free')
        code_country = response.country
        # logger.info(" The code country is %s" % code_country)
    except Exception as e:

        logger.error("Cannot get The code country for address %s" % adress)
        code_country = "FR"
    return code_country


def get_client_country(adress):
    if adress == "":
        country = ""
    elif adress == "127.0.0.1" or "192.168.100" in adress:
        country = "France"
    else:
        response = DbIpCity.get(adress, api_key='free')
        country = response.city
        # logger.info(" The code country is %s" % country)
    return country


def date_gmdate(str_formate, int_timestamp=None):
    if int_timestamp == None:
        return time.strftime(str_formate, time.gmtime())
    else:
        return time.strftime(str_formate, time.gmtime(int_timestamp))


def get_api_version_shopify():
    from datetime import date
    year = date.today().strftime("%Y")
    month = date.today().strftime("%m")
    if month not in ['01', '04', '07', '10']:

        if int(month) > 10:
            api_version = year + '-10'
        elif int(month) > 7:
            api_version = year + '-07'
        elif int(month) > 4:
            api_version = year + '-04'
        else:
            api_version = year + '-01'
    else:
        api_version = year + '-' + month
    return api_version


def get_valid_post(customer, customer_type):
    import calendar
    year = datetime.datetime.today().strftime("%Y")
    month = datetime.datetime.today().strftime("%m")
    # logger.info('counter for client %s for year %s and month %s' % (customer, year, month))
    last_day = calendar.monthrange(int(year), int(month))[1]
    date_start = "%s-%s-01" % (year, month)
    date_fin = "%s-%s-%s" % (year, month, last_day)
    post_counter = db.get_counter_post(customer, customer_type, date_start, date_fin)[0]
    if not post_counter:
        post_counter = 0
    plan_client = db.get_client_payment(customer, customer_type)[5]
    if plan_client[1] == 'FREE':
        max_post = db.max_post(plan_client)[0]
        return max_post < post_counter
    else:
        return False


def max_number_product_exceeded(customer_name, customer_type, body):
        try:
            payment = db.get_client_payment(customer_name, customer_type)
            plan_name = payment[5]
            plan = db.get_plan_form_name(plan_name)
            max_number_training_image = int(plan[4])
            somme = 0
            for category in body.json()[customer_name + '_' + customer_type]:
                somme += len(category['Photos'])
            logger.info("products count %s for file %s client %s type %s" % (somme, body, customer_name, customer_type))
            if somme > max_number_training_image and plan_name == 'FREE':
                return True
            else:
                return False
        except Exception as e:
            logger.error("error in getting products count for client %s with type %s file %s error %s"
                         % (customer_name, customer_type, body, e))
            return False


def get_count_product_validation(token, url_shop, plan):
    api_version = get_api_version_shopify()
    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json"
    }
    count_point = "/admin/api/%s/products/count.json" % api_version

    count_products = requests.get("https://{0}{1}".format(url_shop, count_point), headers=headers)
    if count_products.status_code != 200:
        logger.error("Error in getting info cms client shopify %s  token %s " % (url_shop, token))
        send_email_to_admin("Errror getting cms data cron shopify",
                            "Error_get_count_product_validation in getting info cms client shopify %s  token %s "
                            % (url_shop, token))
    max_images_training = db.get_plan_form_name(plan)[4]
    count_json = json.loads(count_products.text)
    counter = count_json.get('count', 0)
    if (counter > max_images_training or counter == 0) and plan == 'FREE':
        return False
    else:
        return True


def shopify_data_and_train(access_token, domain, customer_name, customer_type, user_apikey, project_name):
    logger.info('access_token for client with domain %s is %s' % (domain, access_token))
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }
    api_version = get_api_version_shopify()
    endpoint = "/admin/api/%s/shop.json" % api_version
    response = requests.get("https://{0}{1}".format(domain,
                                                    endpoint), headers=headers)
    if response.status_code == 200:
        data_retreived = json.loads(response.text)
        shop = data_retreived['shop']['domain']
        email = data_retreived['shop']['email']
        data_client = response.text

        if customer_name and customer_type and user_apikey and project_name:
            streams_path_product_json = STREAMS_PATH + customer_type + '/' + customer_name + \
                                        '/similars/' + domain
            json_file = streams_path_product_json + '/shopify_json_file_' + customer_type + '_' + customer_name + \
                        ".json"
            data_file = streams_path_product_json + '/data_client_file_' + customer_type + '_' + customer_name + \
                        ".json"
            if not os.path.exists(streams_path_product_json):
                os.makedirs(streams_path_product_json)
            out = open(json_file, "w")
            out.write('{"' + shop + '":' + data_client + '}')
            out.close()

            if not os.path.exists(streams_path_product_json):
                os.makedirs(streams_path_product_json)
            dat_client = open(data_file, "w")
            dat_client.write(json.dumps(data_retreived))
            dat_client.close()
            # TODO configure it to use AWS or AZURE
            upload_file(file_local_path=data_file,
                        file_upload_s3=STREAMS_S3 + customer_name + '/' + customer_type + '/shopify/',
                        file_upload_azure=AZURE_STREAMS_PATH +customer_name + '/' + customer_type +
                                          '/shopify/data_client_file_' + customer_type + '_' + customer_name + ".json")
            training_details = {}
            create_update_project(customer_name, customer_type, project_name, 'similars', 1, project_name,
                                  json.dumps(training_details), 1)
            create_update_project(customer_name, customer_type, project_name, 'classification', 1,
                                  project_name, json.dumps(training_details), 1)
            shopify_training(user_apikey, customer_name, customer_type, project_name, domain)


def get_payment_details_cms_shopify(customer_name, customer_type, domain, access_token, payment_infos):
    try:
        if payment_infos.get('status', 0) == 0:
            logger.info('access_token for client with domain %s is %s' % (domain, access_token))
            headers = {
                "X-Shopify-Access-Token": access_token,
                "Content-Type": "application/json"
            }
            api_version = get_api_version_shopify()
            endpoint = "/admin/api/%s/recurring_application_charges.json" % api_version
            response = requests.get("https://{0}{1}".format(domain,
                                                            endpoint), headers=headers)
            if response.status_code == 200:
                data_retreived = json.loads(response.text)
                for payment in data_retreived['recurring_application_charges']:
                    if payment.get('status') == "accepted" and str(payment.get("id")) == \
                            payment_infos.get('transction_id', ''):
                        activate_endpoint = "/admin/api/%s/recurring_application_charges/%s/activate.json" \
                                            % (api_version, payment.get('id'))
                        body_activate = {'recurring_application_charges': payment}
                        response_activate = requests.post("https://{0}{1}".format(domain, activate_endpoint),
                                                          json=body_activate, headers=headers)
                        if response_activate.status_code == 200:
                            payment_client = db.get_client_payment(customer_name, customer_type)
                            date = (payment_client[11]).strftime("%Y-%m-%d %H:%M:%S")
                            db.update_client_payement(customer_name, customer_type, date,
                                                      payment.get('name'),
                                                      1, "paypal", float(payment.get("price")) * 11)
                            db.update_transction_id(customer_name, customer_type, str(payment.get("id")),
                                                    payment.get('name'),
                                                    date, 'paypal')
                            create_or_update_user_apikey(user=customer_name, period_in_hours=8040)
                            db.update_url_confirmation(customer_name, customer_type, 'shopify', domain, access_token,
                                                       '')
                            logger.info("Client shopify %s accept the payment and  it is activated %s %s"
                                        % (domain, customer_name, customer_type))
                            return True, get_user_apikey(customer_name)
                        else:
                            return False, get_user_apikey(customer_name)
                    else:
                        return False, get_user_apikey(customer_name)
            return False, get_user_apikey(customer_name)
        else:
            return True, get_user_apikey(customer_name)
    except Exception as e:
        logger.error("Payment shopify error %s" % e)
        return False, get_user_apikey(customer_name)


def count_product(token, url_shop):
    '''
    :param token: shopify token to acess client products listq
    :param url_shop: the url of client shopifu url
    :return: nomber of products of the shopify store
    '''
    api_version = get_api_version_shopify()
    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json"
    }
    count_point = "/admin/api/%s/products/count.json" % api_version
    try:
        count_products = requests.get("https://{0}{1}".format(url_shop, count_point), headers=headers)
        count_json = json.loads(count_products.text)
        counter = int(count_json.get('count', 0))
        return counter
    except:
        return 0


# TO BE MODIFIED TO MATCH THE LATEST ONE AND TO BE IMPORTED EVERYWHERE NEEDED IN BACKEND
def fine_tune(IMG_HEIGHT, IMG_WIDTH, NUM_CLASSES):

    vgg_conv = VGG16(weights='imagenet', include_top=False, input_shape=(IMG_HEIGHT, IMG_WIDTH, 3))

    for layer in vgg_conv.layers[:-4]:
        layer.trainable = False

    model = models.Sequential()

    model.add(vgg_conv)
    model.add(layers.Flatten())
    model.add(layers.Dense(1024, activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(NUM_CLASSES, activation='sigmoid'))

    # model.summary()
    if not LOCAL:
        parallel_model = multi_gpu_model(model, gpus=2)
    else:
        parallel_model = model

    parallel_model.compile(loss='categorical_crossentropy',
                           optimizer=optimizers.RMSprop(lr=1e-4),
                           metrics=['accuracy'])
    return parallel_model, model


def verification_of_images(customer_name, customer_type, project_name):
    path = OUTPUT_PATH + customer_type + '/' + customer_name + '/images/' + project_name + '/'
    directories = next(os.walk(path))[1]
    if 'train' in directories:
        path = os.path.join(path, 'train')
    if len(directories) == 0:
        filelist = os.listdir(path)
        for file_obj in filelist:
            ext = imghdr.what(path + file_obj)
            if (ext != file_obj.split(".")[1]) or (ext is None):
                os.remove(path + file_obj)
                # logger.info("Deleting_image %s as it contains %s encoding - %s "
                #             % (file_obj, ext, file_obj.split('.')))
    else:
        for j in next(os.walk(path))[1]:
            filelist = os.listdir(path + j + "/")

            for file_obj in filelist:
                ext = imghdr.what(path + j + "/" + file_obj)
                if (ext != file_obj.split(".")[1]) or (ext is None):
                    os.remove(path + j + "/" + file_obj)
                    # logger.info("Deleting_image %s as it contains %s encoding - %s "
                    #             % (file_obj, ext, file_obj.split('.')[1]))


def load_vectors_from_local(vectors, users):
    '''
    :param vectors: dict with vectors names and values initialised to empty dict
    :param users: list of all users in database
    :return: json with all vectors with values
    '''
    for user in users:
        vector_path = VECTORS_PATH + str(user[8]) + '/' + str(user[1]) + '/'
        try:
            projects = os.listdir(vector_path)
            for project in projects:
                    vectors_project = os.listdir(vector_path + project)
                    status = db.get_status_project(STATUS_PROJECT_TABLE, user[1], user[8], 'similars', project)
                    if status and status[0] == 2:
                        for vector in vectors_project:
                            try:
                                vector_name = vector.split('.parquet')[0]
                                if vector_name not in vectors.keys():
                                    # logger.info(
                                    #     'Vector to load  =====> %s' % (vector))
                                    vector_data = dd.read_parquet(vector_path + project + '/' + vector,
                                                                  engine='pyarrow')

                                    vectors[vector_name] = vector_data
                                    if vector_data is not None:
                                        vectors[vector_name] = vector_data
                                        # logger.info('Vector %s  loaded successfully for client %s '
                                        #                     % (vector_name, str(user[1])))
                                    # else:
                                    #     logger.info(
                                    #                 'Vector %s not loaded for client %s vector is None'
                                    #                 % (vector_name, str(user[1])))
                            except Exception as e:
                                logger.warning("Vector not loaded %s error %s" %(vector, e))
                    else:
                        # logger.info('Status Project not 2 %s %s' % (project, status))
                        continue
        except Exception as e:
            logger.warning("Can't get the parquet file for client %s with domaine %s error %s"
                           % (str(user[1]), str(user[8]), e))
    # logger.info("Vectors keys : %s" % vectors.keys())
    return vectors


def befor_month(number):
    if number == "01":
        return "12"
    elif number == "02":
        return "01"
    elif number == "03":
        return "02"
    elif number == "04":
        return "03"
    elif number == "05":
        return "04"
    elif number == "06":
        return "05"
    elif number == "07":
        return "06"
    elif number == "08":
        return "07"
    elif number == "09":
        return "08"
    elif number == "10":
        return "09"
    elif number == "11":
        return "10"
    elif number == "12":
        return "11"


def week_of_month(dt):
    first_day = dt.replace(day=1)
    dom = dt.day
    adjusted_dom = dom + first_day.weekday()
    return int(ceil(adjusted_dom/7.0))


def create_table_plan_and_plan():
    try:
        db.create_plans_table()
        db.add_new_plan('FREE', 1000, 0, 365, 100)
        db.add_new_plan('STANDARD', 10000, 1188, 365, 5000)
        db.add_new_plan('PRO', 10000, 1188, 365, 5000)
        db.add_new_plan('PREMIUM', 50000, 3588, 365, 20000)
        db.add_new_plan('PLATINUM', 100000, 5988, 365, 50000)
        create_plan_stripe('STANDARD', 1188, 'eur')
        create_plan_stripe('PREMIUM', 3289, 'eur')
        create_plan_stripe('PLATINUM', 5489, 'eur')
    except Exception as e:
        logger.warning("------------ %s " % e)


def shopify_payment_billing(customer_name, customer_type, customer_email, url_cms, token_cms, plan):

    headers = {
        "X-Shopify-Access-Token": token_cms,
        "Content-Type": "application/json"
    }
    # Delete active payment
    api_version = get_api_version_shopify()
    previous_payment = False
    try:
        payment_client = db.get_client_payment(customer_name, customer_type)
        if payment_client != ():
            previous_payment = True
            payment_endpoint = "/admin/api/%s/recurring_application_charges/%s.json" % (api_version, payment_client[6])
            get_payment_shopify_status = requests.get("https://{0}{1}".format(url_cms, payment_endpoint),
                                                      headers=headers)
            if get_payment_shopify_status.status_code == 200:
                response_status = json.loads(get_payment_shopify_status.text)
                if response_status.get('recurring_application_charge', {}).get('status', '') == 'active':
                    delete_endpoint = "/admin/api/%s/recurring_application_charges/%s.json" \
                                      % (api_version, payment_client[6])
                    response_delete = requests.delete("https://{0}{1}".format(url_cms, delete_endpoint),
                                                      headers=headers)
                    # if response_delete.status_code == 200:
                        # logger.info("========>payment deleted %s " % payment_client[6])
        else:
            previous_payment = False
    except Exception as e:
        logger.error("Exception deleting old payment %s for client %s %s " % (e, customer_name, customer_type))

    price = 99.0

    price_dollar = round(price_converter.convert(price, 'EUR', 'USD'))
    endpoint = "/admin/api/%s/recurring_application_charges.json" % api_version
    json_post = {
        "recurring_application_charge": {
            "name": plan,
            "price": price_dollar,
            "return_url": "https://foqus-shopify.azurewebsites.net/index"
        }}

    if LOCAL:
        json_post['recurring_application_charge']['test'] = 'true'
        json_post['recurring_application_charge']['trial_days'] = 1000
    if not previous_payment:
        json_post['recurring_application_charge']['trial_days'] = 0
        total = price
    else:
        total = price
    # logger.info('===========> json to post %s total to pay %s' % (json.dumps(json_post), total))
    charge_shopify_api = requests.post("https://{0}{1}".format(url_cms, endpoint), headers=headers, json=json_post)
    if charge_shopify_api.status_code == 201:
        response = json.loads(charge_shopify_api.text)
        transaction_id = response.get('recurring_application_charge', {}).get('id', None)
        url_confirmation = response.get('recurring_application_charge', {}).get('confirmation_url', '')
        # logger.info("====>recurring_application_charge_signup_url_confirmation %s " % transaction_id)
        date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        db.update_client_payement(customer_name, customer_type, date, plan, 1, 'paypal', total)
        db.update_transction_id(customer_name, customer_type, str(transaction_id), plan, date, 'paypal')
        db.update_url_confirmation(customer_name, customer_type, 'shopify', url_cms, token_cms, url_confirmation)
        create_or_update_user_apikey(user=customer_name, period_in_hours=30)
        return url_confirmation
    else:
        try:
            send_payment_email(customer_email)
        except Exception as e:
            logger.error("exception in sending email shopify_payment_billing..." + str(e))
        return ''


def get_url_confirmation_expiration(customer, customer_type, customer_email):

    try:
        payment_client = db.get_client_payment(customer, customer_type)

        if payment_client[8] == 1:
            return None
        cms_details = db.get_cms_details_for_client('cms_client_table', customer, customer_type, 'shopify')
        headers = {
            "X-Shopify-Access-Token": cms_details[6],
            "Content-Type": "application/json"
        }
        api_version = get_api_version_shopify()
        endpoint = "/admin/api/%s/recurring_application_charges/%s.json" % (api_version, payment_client[6])

        response = requests.get("https://{0}{1}".format(cms_details[5], endpoint), headers=headers)
        payment_status = json.loads(response.text)
        if payment_status.get("recurring_application_charge", {}).get("status", "expired") == "expired":
            url_confirmation = shopify_payment_billing(customer, customer_type, customer_email, cms_details[5], cms_details[6], payment_client[5])
        elif payment_status.get("recurring_application_charge", {}).get("status", "expired") == "accepted":

            activate_endpoint = "/admin/api/%s/recurring_application_charges/%s/activate.json" \
                                % (api_version, payment_status.get("recurring_application_charge", {}).get('id'))
            response_activate = requests.post("https://{0}{1}".format(cms_details[5], activate_endpoint),
                                              json=payment_status, headers=headers)
            if response_activate.status_code == 200:
                payment_client = db.get_client_payment(customer, customer_type)
                date = (payment_client[11]).strftime("%Y-%m-%d %H:%M:%S")
                db.update_client_payement(customer, customer_type, date,
                                          payment_status.get("recurring_application_charge", {}).get('name'),
                                          1, "paypal", float(payment_status.get("recurring_application_charge", {}).get("price")) * 11)
                db.update_transction_id(customer, customer_type, str(payment_status.get("recurring_application_charge", {}).get("id")),
                                        payment_status.get("recurring_application_charge", {}).get('name'),
                                        date, 'paypal')
                create_or_update_user_apikey(user=customer, period_in_hours=8040)
                db.update_url_confirmation(customer, customer_type, 'shopify', cms_details[5], cms_details[6],
                                           '')
                # logger.info("Client shopify %s accept the payment and  it is activated %s %s"
                #             % (cms_details[5], customer, customer_type))

            return None
        else:
            return None
        if url_confirmation == '':
            return None
    except Exception as e:
        logger.error("Error getting url confirmation for customer %s with type %s %s" % (customer, customer_type, e))
        return None
    return url_confirmation


def calculate_images_file(json_input, customer_name, customer_type):
    photos = 0
    categorie = False
    for i in range(get_json_ads_number(json_input, customer_name, customer_type)):
        if 'Categorie' in json_input[customer_name.lower() + '_' + customer_type.lower()][i].keys():
            categorie = True
        else:
            categorie = False
        photos = photos + len(get_json_ad_photos(json_input, customer_name, customer_type, i))
    logger.info('===================> %s' % photos)
    return categorie, photos


# def upload_parquet(parquet_local):
def image_treatement_to_vector(model, image_path, hash_image):
    features = None
    try:
        img = Image.open(image_path)
        img = img.resize((TARGET_RESOLUTION, TARGET_RESOLUTION), Image.ANTIALIAS)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        features = model.predict(x)  # Prediction des features
        features = features[0].reshape(-1)
    except Exception as e:
        logger.warning("Errooor_when_claculating_trying_with_RGB %s" %e)
        try:
            img = Image.open(image_path)
            rgb_im = img.convert('RGB')
            image_name = hash_image
            emplacement_to_save = hash_image
            image_name = image_name.replace('png', 'jpg')
            rgb_im.save(emplacement_to_save + image_name)

            upload_file(file_local_path=emplacement_to_save + image_name,
                        file_upload_s3=OUTPUT_S3 + emplacement_to_save.split('output/')[1],
                        file_upload_azure=AZURE_OUTPUT_PATH + emplacement_to_save.split('output/')[1] + image_name)
            os.remove(emplacement_to_save + hash_image)

            new_image = emplacement_to_save + image_name
            img = Image.open(new_image)
            img = img.resize((TARGET_RESOLUTION, TARGET_RESOLUTION), Image.ANTIALIAS)
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            features = model.predict(x)  # Prediction des features
            features = features[0].reshape(-1)
        except Exception as e:
            logger.error("ignoring_the_image %s cannot calculate vector %s" % (hash_image, e))
    return features.tolist()


def add_layer_to_vgg(customer_name, customer_type):
    parameters = db.get_training_parameters(customer_name, customer_type, "similars")
    # logger.info('--------------------------------------------------------')
    include_top = parameters.get('vectors').get('include_top', False)
    classes = parameters.get('vectors').get('classes_numbers', 1000)
    # logger.info('--------------------------------------------------------')
    try:
        if include_top:
            logger.info("====> Loading model with include_top True and classes %s" % classes)
            model = VGG16(include_top=True, weights="imagenet", input_tensor=None,
                          input_shape=None, pooling=None, classes=classes)
        else:
            logger.info("====> Loading model with include_top Flase")
            model = VGG16(weights='imagenet', include_top=False)
    except Exception as e:
        logger.error("Model not loaded error is %s ==> loading with include_top False " % e)
        model = VGG16(weights='imagenet', include_top=False)
    return model


def get_images_from_db(images, customer_name, project_name):
    response_scores = []
    for i in images:
        url_image = db.get_url_from_hash_client_table(replace_special_caractere(customer_name).replace(' ', '_'),
                                                      project_name, i['image'].split('/')[-1])
        if url_image is None:
            url_image = db.get_url_from_hash_client_table(
                replace_special_caractere(customer_name).replace(' ', '_')
                , project_name, i['image'].split('/')[-1].replace('jpeg', 'png').replace('jpg', 'png'))
            if url_image is None:
                logger.error("Hash table corrupted! Can't get url for hash file " + i['image'].split('/')[-1])
                continue
        index_hash = url_image[3].split(' ').index(i['image'].split('/')[-1])
        value_image = {'url_image': url_image[1].split(' ')[index_hash],
                       'score': int(round(i['score'], 2) * 10 * 10),
                       'url_produit': url_image[2] if url_image[2] else '',
                       'idproduit': url_image[5] if url_image[5] else '',
                       'mobile_url_produit': url_image[6] if url_image[6] else ''}

        response_scores.append(value_image)
    return response_scores


def get_images_from_db_vptree(images, customer_name, project_name):
    response_scores = []
    for i in images:
        url_image = db.get_url_from_hash_client_table(replace_special_caractere(customer_name).replace(' ', '_'),
                                                      project_name, i['image'].split('/')[-1])
        if url_image is None:
            continue
        for image in url_image[3].split(' '):
            if i['image'] in image:
                index_hash = url_image[3].split(' ').index(image)
                value_image = {'url_image': url_image[1].split(' ')[index_hash],
                               'score': int(round(i['score'], 2) * 10 * 10) if i['score'] < 1 else int(round(i['score'], 2) * 10 ),
                               'url_produit': url_image[2] if url_image[2] else '',
                               'idproduit': url_image[5] if url_image[5] else '',
                               'mobile_url_produit': url_image[6] if url_image[6] else ''}

                response_scores.append(value_image)
    return response_scores