import os
import time
import json

from bestchange_api import BestChange

from adminConfig import FILEPATH
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


def rate_processor(pairs: dict, limit: int, filepath: str, api: BestChange) -> dict:
    """
    Iterate through pairs dict and get api call by currencies ids
    Limit sets number for maximum exchangers in tables.
    Get update time from filepath zip archive.
    """
    result = {}
    headers = {}
    if not api.rates():
        return result

    for i, pair in enumerate(list(pairs.values())):
        rates_dict = {}

        give = api.currencies().search_by_name(pair[0])
        receive = api.currencies().search_by_name(pair[1])
        give_id, _, give_name = give.popitem()[1].values()
        receive_id, _, receive_name = receive.popitem()[1].values()

        rates_filter = api.rates().filter(give_id, receive_id)

        for count, rates in enumerate(rates_filter):
            if count >= limit:
                break
            else:
                exchange_name = get_exchangers_name(rates, api)
                rates_dict[count] = {
                        'give_name': give_name,
                        'receive_name': receive_name,
                        'exchange_name': exchange_name,
                        'give_amount': round(rates['give'], 4),
                        'receive_amount': round(rates['get'], 4),
                        'reserve': round(rates['reserve']),
                        'min_sum': rates['min_sum'],
                        'max_sum': rates['max_sum'],
                        }
        result[i] = rates_dict
        headers[i] = (give_name, receive_name)

    result['headers'] = headers
    update_time = get_update_time(filepath)
    result['update_time'] = {'update_time': update_time}
    marked_exchanger = get_marked_exchanger()
    result['marked_exchanger'] = {'marked_exchanger' : marked_exchanger}
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

        if 0 < integer < 50:
            result = integer
    return result


def validate_exchanger_name(name: str) -> str:
    result = 'no_exchanger'
    if name:
        result = name.strip()
    return result


def parse_json_response(response: bytes):
    data = json.loads(response)
    user_pairs = {}
    USER_FILTER.limit = validate_user_limit(data['limit'])
    USER_FILTER.exchanger = validate_exchanger_name(data['exchanger'])
    pairs = data['pairs']

    if len(pairs) > 0:
        for count, pair in enumerate(pairs):
            user_pairs[count] = (pair[0], pair[1])
    else:
        user_pairs[1] = ('Bitcoin (BTC)', 'Альфа cash-in RUB')

    USER_FILTER.pairs = user_pairs
    USER_FILTER.json_dump_file()
