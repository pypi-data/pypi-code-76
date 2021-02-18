#! /usr/bin/python
# -*- coding: utf-8 -*-
from foqus.customers import *
from foqus.pipline_cutomise import Pipeline2
from foqus.request_api import APIFoqus
from six.moves import http_client

from urllib.parse import urlparse
from jsondiff import diff

import imghdr
import mimetypes
import requests
import shutil

import os
import json
import glob

import time
import sys

api = APIFoqus()


def get_category(last_json, num_cat):
    for json_value in last_json.values():
        for index_product in range(len(json_value)):
            if str(index_product) == str(num_cat):
                try:
                    logger.info("The_Category_that_will_have_changes: " + str(json_value[index_product]['Categorie']))
                    return str(json_value[index_product]['Categorie'])
                except Exception as e:
                    return None


def add_category_and_write_to_file(status, last_json_path, last_json, new_category_objects, path_new_file):
    try:
        new_obj = dict()
        for k, v in last_json.items():
            for o in range(len(v)):
                for p in range(len(v[o]['Photos'])):
                    photo = v[o]['Photos'][p]
                    photo["Status"] = 2

                for obj in new_category_objects:
                    if v[o] == obj:
                        v[o] = obj
                        photo['Status'] = status
        new_obj[k] = v
        with open(path_new_file, 'w') as outfile:
            json.dump(new_obj, outfile)
        outfile.close()
        logger.info("----delta: added category and wrote to file")
    except Exception as e:
        logger.error("Error in_diff_files add_category_and_write_to_file %s" %e)


def write_to_file(status, last_json, path_new_file, category_will_have_changes=None, block_image_n=None,
                  new_file=False, deleted_block=None):
    if os.path.isfile(path_new_file):
        logger.info("-----path_new_file: %s" % path_new_file)
        with open(str(path_new_file), 'r') as content_file:
            content = content_file.read()
        json_value = json.loads(content)
    else:
        json_value = []
    logger.info("----delta: creating file...")
    new_obj = {}
    key = ""
    try:
        for key, json_value in last_json.items():
            for index_product in range(len(json_value)):
                for product in range(len(json_value[index_product]['Photos'])):
                    if new_file:
                        photo = json_value[index_product]['Photos'][product]
                        photo["Status"] = 1
                    if not block_image_n and not "Status" in json_value[index_product]['Photos'][product] \
                            and category_will_have_changes:
                        photo = json_value[index_product]['Photos'][product]
                        photo["Status"] = 2
                    if category_will_have_changes \
                            and json_value[index_product]['Categorie'] == category_will_have_changes and \
                                    str(product) == str(block_image_n):
                            photo = json_value[index_product]['Photos'][product]
                            photo["Status"] = status
                    if block_image_n:
                        photo = json_value[index_product]['Photos'][int(block_image_n)]
                        photo["Status"] = status
                    if deleted_block and not category_will_have_changes and not "Status" in json_value[index_product]['Photos'][product]:
                        deleted_block['Status'] = status
                        logger.info(deleted_block)
                        json_value[0]['Photos'].append(deleted_block)
                    elif not "Status" in json_value[index_product]['Photos'][product]:
                        photo = json_value[index_product]['Photos'][product]
                        photo["Status"] = status
        new_obj[key] = json_value
        with open(path_new_file, 'w') as outfile:
            json.dump(new_obj, outfile)
        outfile.close()
        logger.info("-----delta file created")
    except Exception as e:
        logger.error("Erooor in_difff_files write_to_file %s" % e)


def delta_retrieve_json(customer_name, customer_type, project_name):
    logger.info("============> delta retrieve json started")
    sys.setrecursionlimit(3000)
    start = time.process_time()
    path_json = STREAMS_PATH + customer_type + '/' + customer_name + '/similars/' + project_name
    date = datetime.datetime.today().strftime("%Y-%m-%d:%H-%M")
    path_new_file = STREAMS_PATH + customer_type + '/' + customer_name + '/delta_files/' + project_name + '/'

    if not os.path.isdir(path_new_file):
        try:
            os.makedirs(path_new_file)
        except Exception as e:
            logger.error("Cannot create delta_files directory for customer. "
                         "Please verify permissions ")
            pass

    new_file_status = path_new_file + date + ".json"

    # if there are shopify files take only shopify_file*.json
    if len(glob.glob(path_json + "/shopify_*.json")) > 0:
        paths = sorted(glob.glob(path_json + "/shopify_file_*.json"), key=os.path.getmtime)
    else:
        paths = sorted(glob.glob(path_json + "/*.json"), key=os.path.getmtime)
    if len(paths) > 1:
        last_json_path = paths[-1]
        before_last_json_path = paths[-2]
        logger.info("******** "+before_last_json_path)
        logger.info("******** "+last_json_path)
        last_json = json.load(open(last_json_path))
        before_last_json = json.load(open(before_last_json_path))
    elif len(paths) == 1:
        last_json_path = paths[-1]
        last_json = json.load(open(last_json_path))
        before_last_json = {customer_name + "_" + customer_type: []}
    else:
        last_json = {customer_name + "_" + customer_type: []}
        before_last_json = {customer_name + "_" + customer_type: []}
    try:
        difference = diff(before_last_json, last_json)
    except Exception as e:
        logger.error("Error_diff %s" %e)
        difference = {}

    if before_last_json[customer_name + "_" + customer_type] != [] and difference != {} \
            and difference[customer_name + '_' + customer_type]:
        logger.info("-----delta: comparing to existing file")
        for key_cat, cat in difference[customer_name + '_' + customer_type].items():
            logger.info("======== key_cat and cat:" + str(key_cat) + str(cat))
            category_will_have_changes = get_category(last_json, key_cat)
            if category_will_have_changes:
                for kphotos, photos in cat.get('Photos', {}).items():
                    if str(kphotos) == '$delete':
                        for deleted_position in photos:
                            block_image_n = str(deleted_position)
                            write_to_file(0, last_json, new_file_status, category_will_have_changes, block_image_n)
                    elif str(kphotos) == '$insert':
                        for position_added, block in photos:
                            status = 1
                            block_image_n = str(position_added)
                            write_to_file(status, last_json, new_file_status, category_will_have_changes,
                                                          block_image_n)
                    else:
                        logger.info("Block already donwloaded")
                        write_to_file(2, last_json, new_file_status)
                        continue
            else:
                try:
                    logger.info("-----delta var = cat:")
                    logger.info(cat)
                    for change_type, change in cat.get('Photos', {}).items():
                        if str(change_type) == '$insert':
                            for position_added, block in change:
                                block_image_n = str(position_added)
                                logger.info("added in: " + str(block_image_n))
                                write_to_file(1, last_json, new_file_status, block_image_n=block_image_n)
                        elif str(change_type) == '$delete':
                            for deleted_position in change:
                                block_image_n = str(deleted_position)
                                deleted_block = before_last_json[customer_name + "_" + customer_type][0]['Photos'][int(block_image_n)]
                                logger.info(deleted_block)
                                write_to_file(0, last_json, new_file_status, block_image_n=block_image_n, deleted_block=deleted_block)
                    write_to_file(2, last_json, new_file_status)
                except AttributeError as err:
                    # Only categories have changed not photos inside them
                    logger.error(err)
                except Exception as e:
                    logger.error("Erooor in_difff_files delta_retrieve_json %s" % e)
                    write_to_file(1, last_json, new_file_status)
    elif difference == {} and len(paths) > 1:
        logger.info("-----delta: same file")
        write_to_file(2, last_json, new_file_status)
    else:
        logger.info("-----delta: 1st time, creating json")
        try:
            write_to_file(1, last_json, new_file_status, new_file=True)
        except Exception as e:
            logger.error(e)
        logger.info("------delta: done creating file")
    logger.info("-----Delta retrieve json compare time taken: "+str(time.process_time() - start))
    return new_file_status


def load_json_data(json_path):
    try:
        with open(json_path) as data_file:
            json_input = json.load(data_file)
    except:
        json_data = open(json_path)
        bom_maybe = json_data.read(3)
        if bom_maybe != codecs.BOM_UTF8:
            json_data.seek(0)
        json_input = json.load(json_data)
    return json_input


def checkUrl(url):
    p = urlparse(url)
    conn = http_client.HTTPConnection(p.netloc)
    conn.request('HEAD', p.path)
    resp = conn.getresponse()
    return resp.status < 400


def is_url_image(image_url):
    image_formats = ("image/png", "image/jpeg", "image/jpg", "binary/octet-stream")
    r = requests.head(image_url)
    if r.headers["content-type"] not in image_formats:
        mimetype, encoding = mimetypes.guess_type(image_url)
        return mimetype and mimetype.startswith('image')
    else:
        return True


def max_nb_images(path):
    list_nbrs = []
    for j in os.listdir(path):
        for k in os.listdir(str(path) + "/" + str(j)):
            ext = imghdr.what(str(path) + "/" + str(j) + "/" + str(k))
            if (ext == 'png' and k.split(".")[1] in ['jpg', 'jpeg', 'JPG', 'JPEG']) or \
                    (ext in ['jpeg', 'jpg'] and k.split('.')[1] in ['png', 'PNG']) or (ext is None):
                os.remove(str(path) + "/" + str(j) + "/" + str(k))
                logger.info("Deleting_image as it contains png encoding - " + str(path) + "/" + str(j) + "/" + str(k))
        list_nbrs.append(len(os.listdir(str(path) + "/" + str(j))))
    return max(list_nbrs)


def verif_folder_less_twenty(path, nb_classes):
    # Not actually verif less than 20 its just the name
    image_ext = ['.jpg', '.png', '.jpeg', '.JPG', '.PNG', '.JPEG']
    folder_less_20 = []
    # we will check if the number returned by max_nb_images is < batch size in this case it will cause error
    # in training so we take max between it and batch/nb_classes
    max_nb = max(round(BATCH_SIZE / nb_classes), max_nb_images(path))
    if max_nb < 20:
        max_nb = 20
    for j in os.listdir(path):
        x = 0
        for i in os.listdir(str(path) + "/" + str(j)):
            if os.path.splitext(i)[1] in image_ext:
                x = x + 1
        if x == 0 :
            shutil.rmtree(str(path) + "/" + str(j))
            logger.info("Deletin Empty folder : " + str(path) + "/" + str(j))
        elif (x <= 20 or x < max_nb):
            logger.info("WARNING: Folder has less images : " + str(j).split('/')[-1])
            folder_less_20.append(str(j).split('/')[-1])
    return folder_less_20, max_nb


def generate_more_images(training_path, folders, max_nb):
    for id_categorie in folders:
        DIR = str(training_path) + "/" + str(id_categorie)
        nb_images = (len(os.listdir(DIR)))
        p = Pipeline2(source_directory=DIR, output_directory=DIR)
        p.rotate(probability=1, max_left_rotation=5, max_right_rotation=5)
        p.flip_left_right(probability=0.5)
        p.zoom_random(probability=0.5, percentage_area=0.8)
        p.flip_top_bottom(probability=0.5)
        p.sample(max_nb - nb_images)
    logger.info("The images increase is done successfully")


def classification_similars(customer_name, customer_type, project_name):
    api.apipost("classification_similars", customer_name, customer_type, project_name)


def process_customer_stream_from_json(customer_name, customer_type, project_name):
    api.apipost('training_similars', customer_name, customer_type, project_name)


def get_redirect_url(url):
    try:
        image = requests.get(url)
        if image.url == url:
            return is_url_image(url)
        else:
            return is_url_image(image.url)
    except:
        return False


def shopify_training(customer_name, customer_type, url_shop, project):
    api.apipost('shopify_training', customer_name, customer_type, None, None, project, url_shop)


def generate_similarity_vector(customer_name="vector", customer_type='vector', deleted_image={}, project_name=None):
    vector_response = api.apipost('training_similars', customer_name, customer_type, project_name, deleted_image, None)
    response_text = json.loads(vector_response.text)
    response_from_parquet = response_text['response']
    if response_from_parquet == 2:
        return True
    return False


def text_training_retrieve_json(excel_path, customer_name, customer_type, customer_universe, project_name):
    send_email_when_training_started(customer_name, project_name, 'classification', 'Training started')
    if project_name:
        operation = 'training_classification'
    else:
        operation = 'training_text_detection'

    api.apipost(operation, customer_name, customer_type, project_name, excel_path, customer_universe)

