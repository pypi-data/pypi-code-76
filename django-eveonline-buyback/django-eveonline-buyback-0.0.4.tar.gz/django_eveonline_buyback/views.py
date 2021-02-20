import re
import logging
import requests
from decimal import Decimal
from django.shortcuts import render
from django.contrib import messages
from django_eveonline_buyback.forms import EveBuyback
from django_eveonline_buyback.models import BuybackSettings
from django.contrib.auth.decorators import login_required


@login_required
def buyback(request):
    total = 0
    general_total = 0
    blue_total = 0

    if request.method == 'POST':
        try:
            form = EveBuyback(request.POST)
            if form.is_valid():
                general_buyback_rate = BuybackSettings.get_instance().general_buyback_rate
                blue_loot_buyback_rate = BuybackSettings.get_instance().blue_loot_buyback_rate
                submission = form.cleaned_data['submission']
                contract_format = is_contract_format(
                    submission.splitlines()[0])
                sorted_items = item_sorter(submission, contract_format)
                general, blue = sorted_items
                try:
                    general_total = get_evepraisal(
                        general, general_buyback_rate)
                except ValueError as err:
                    logging.error(err)
                    messages.error(request, err)
                blue_total = get_bluepraisal(
                    blue, blue_loot_buyback_rate, contract_format)
                total = round((general_total + blue_total), 2)
        except Exception as err:
            logging.error(err)
            raise
    else:
        form = EveBuyback()

    context = {
        'buyback_settings': BuybackSettings.get_instance(),
        'total': total,
        'general_total': general_total,
        'blue_total': blue_total,
        'form': form,
    }

    return render(request, 'django_eveonline_buyback/adminlte/buyback.html', context)


def is_contract_format(first_item):
    try:
        contract_format = re.search(
            r'\b\w+\b[ +|\t+]\b\d+\b[ +|\t+]\b\w+\b', first_item.replace(',', ''))
    except Exception as err:
        logging.error(err)
        raise

    return contract_format


def item_sorter(submission, contract_format):
    blue_buyback = []
    general_buyback = ''

    try:
        for line in submission.splitlines():
            if contract_format:
                item = re.search(r'.*\b\d+\b', line.replace(',', '')).group()
                item_name = re.sub(r'\b\d+\b', '', item).strip()
            else:
                item_name = re.sub(
                    r'\b\d+\b', '', line.replace(',', '')).strip()
            if item_name.lower() in str(get_blue_loot_types()):
                blue_buyback.append(line.replace(',', ''))
            else:
                general_buyback = general_buyback + f'{line}\n'
    except Exception as err:
        logging.error(err)
        raise

    sorted_items = (general_buyback, blue_buyback)

    return sorted_items


def get_evepraisal(submission, rate):
    total = 0

    blue_loot_types = get_blue_loot_types()
    for blue_loot_type in blue_loot_types:
        blue_loot = re.search(rf'{blue_loot_type}', submission.lower())
        if blue_loot:
            raise ValueError('Blue loot items not sorted correctly, your total may be inaccurate. For best results please copy and paste directly from in game. If you believe you have received this message in error please contact your administrator.')

    try:
        if submission != '':
            url = 'https://evepraisal.com/appraisal'
            market = 'jita'
            payload = {
                'User-Agent': 'django-eveonline-buyback/0.0.1 b@bnunez.com',
                'raw_textarea': f'{submission}',
                'market': f'{market}',
            }
            id_request = requests.post(url, params=payload)
            appraisal_id = id_request.headers['X-Appraisal-Id']
            appraisal_url = f'https://evepraisal.com/a/{appraisal_id}.json'
            result = requests.get(appraisal_url).json()
            total = Decimal(result['totals']['buy'])
    except Exception as err:
        logging.error(err)
        raise

    return float(total) * rate


def get_bluepraisal(submission, rate, contract_format):
    total = 0

    try:
        if len(submission) > 0:
            for line in submission:
                if contract_format:
                    item = re.search(r'.*\b\d+\b', line).group()
                    item_name = re.sub(
                        r'\b\d+\b', '', item).strip().replace(' ', '_').lower() + '_price'
                else:
                    item_name = re.sub(
                        r'\b\d+\b', '', line).strip().replace(' ', '_').lower() + '_price'
                item_quantity = re.search(r'\b\d+\b', line)
                if item_quantity:
                    item_quantity = int(item_quantity.group())
                else:
                    item_quantity = 1
                item_price = getattr(BuybackSettings.get_instance(), item_name)
                total += item_price * item_quantity
    except Exception as err:
        logging.error(err)
        raise

    return total * rate


def get_blue_loot_types():
    try:
        blue_loot_types_raw = [
            field.name for field in BuybackSettings.get_instance()._meta.get_fields()[1:5]]
        blue_loot_types = [x.replace('_', ' ').replace(
            'price', '').strip() for x in blue_loot_types_raw]
    except Exception as err:
        logging.error(err)
        raise

    return blue_loot_types
