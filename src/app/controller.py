import os
import time
import json

from bestchange_api import BestChange
from loguru import logger

from . import FILEPATH
from .models import USER_FILTER


def get_update_time(path: str) -> str:
    """Time for view update time on main page"""
    return time.ctime(os.path.getmtime(path))


def get_marked_exchanger() -> str:
    """Marking exchanger in tables"""
    exchanger = USER_FILTER.exchanger
    return exchanger


def get_exchangers_name(rate: dict, api: BestChange) -> str:
    """Dont get it from api by default"""
    exchange_id = rate['exchange_id']
    exchange_name = api.exchangers().get_by_id(exchange_id)
    return exchange_name


def get_all_currencies(api: BestChange) -> list:
    """All currencies for show pair menu on main page"""
    result = []
    if not api.currencies():
        return result
    all_currencies = api.currencies().get()

    for curr in all_currencies.values():
        result.append(curr['name'])
    return result


@logger.catch()
def rate_logger(rates: dict):
    first_rate = None
    if len(rates[0]) > 0:
        first_rate = f'give_name: {rates[0][0]["give_name"]} | receive_name: {rates[0][0]["receive_name"]}' \
                     f' | exchange_name: {rates[0][0]["exchange_name"]} | city: {rates[0][0]["city"]}'
    logger.debug(f'rate processor - {[x for x in rates]}')
    logger.debug(f'first rate - {first_rate}')


@logger.catch()
def rate_processor(pairs: dict, limit: int, filepath: str, api: BestChange) -> dict:
    """
    Iterate through pairs dict and get api call by currencies ids
    Limit sets number for maximum exchangers in tables.
    Get update time from filepath zip archive.
    Filtered by a city if city exist and pair itself allow change city
    """
    result = {}
    headers = {}
    cities = {}
    if not api.rates():
        logger.debug('Dont get api')
        return result

    for i, pair in enumerate(list(pairs.values())):
        rates_dict = {}

        give = api.currencies().search_by_name(pair[0])
        receive = api.currencies().search_by_name(pair[1])
        give_id, _, give_name = give.popitem()[1].values()
        receive_id, _, receive_name = receive.popitem()[1].values()

        city = api.cities().search_by_name(pair[2])
        city_id = list(city.keys())[0] if len(city) == 1 else None
        city_name = list(city.values())[0]['name'] if len(city) == 1 else None
        rates_filter = api.rates().filter(give_id, receive_id)
        count = 0

        if not rates_filter:
            logger.debug('None rates filter')
            result[i] = {}

        for rates in rates_filter:
            iter_conditions = rates['city_id'] == 0, rates['city_id'] == city_id

            if count >= limit:
                break
            else:
                if not city_id or any(iter_conditions):
                    exchange_name = get_exchangers_name(rates, api)
                    rates_dict[count] = {
                            'give_name': give_name,
                            'receive_name': receive_name,
                            'exchange_name': exchange_name,
                            'give_amount': round(rates['give'], 4),
                            'receive_amount': round(rates['get'], 4),
                            'reserve': round(rates['reserve']),
                            'city': city_name,
                            }
                    count += 1
                else:
                    continue
            result[i] = rates_dict
        headers[i] = (give_name, receive_name)
        cities[i] = city_name

    result['city'] = cities
    result['headers'] = headers
    update_time = get_update_time(filepath)
    result['update_time'] = {'update_time': update_time}
    marked_exchanger = get_marked_exchanger()
    result['marked_exchanger'] = {'marked_exchanger': marked_exchanger}
    rate_logger(result)
    return result


def get_json_report(api: BestChange) -> json:
    rates = rate_processor(USER_FILTER.pairs, USER_FILTER.limit, FILEPATH, api)
    result = json.dumps(rates, indent=2, ensure_ascii=False)
    return result


def get_json_currencies(api: BestChange) -> json:
    """Currencies list for the sidebar"""
    all_currencies = get_all_currencies(api)
    result = json.dumps(all_currencies, indent=2, ensure_ascii=False)
    return result


def validate_user_limit(limit: str) -> int:
    result = 10
    if limit.strip().isdigit():
        integer = int(limit)

        if 0 < integer <= 50:
            result = integer
    return result


def validate_exchanger_name(name: str) -> str:
    result = 'no_exchanger'
    if name:
        result = name.strip()
    return result


@logger.catch()
def parse_json_response(response: bytes):
    """Response from sidebar"""
    data = json.loads(response)
    user_pairs = {}
    USER_FILTER.limit = validate_user_limit(data['limit'])
    USER_FILTER.exchanger = validate_exchanger_name(data['exchanger'])
    pairs = data['pairs']

    if len(pairs) > 0:
        for count, pair in enumerate(pairs):
            if len(pair) == 2:
                pair.append('')
            user_pairs[count] = (pair[0], pair[1], pair[2])
    else:
        user_pairs[1] = ('Bitcoin (BTC)', 'Альфа cash-in RUB', '')

    logger.debug(f'USER INPUT | USER_FILTER.limit = {USER_FILTER.limit} | USER_FILTER.exchanger = {USER_FILTER.exchanger} |'
                 f'USER_FILTER.pairs = {user_pairs}')
    USER_FILTER.pairs = user_pairs
    USER_FILTER.json_dump_file()
