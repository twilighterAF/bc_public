import os
import time
import json
from .apiGateway import BestChange


FILEPATH = './info.zip'


def get_update_time(path: str):
    return time.ctime(os.path.getmtime(path))


def get_exchangers_name(rate: dict, api: BestChange) -> str:
    exchange_id = rate['exchange_id']
    exchange_name = api.exchangers().get_by_id(exchange_id)
    return exchange_name


def rate_processor(pairs: dict, limit: int, api: BestChange) -> dict:
    api.load()
    result = {}

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
                        'give_amount': rates['give'],
                        'receive_amount': round(rates['get'], 4),
                        'reserve': round(rates['reserve']),
                        'min_sum': rates['min_sum'],
                        'max_sum': rates['max_sum'],
                        }
        result[i] = rates_dict

    update_time = get_update_time(FILEPATH)
    result['update_time'] = {'update_time': update_time}
    return result


def get_json_report(pairs: dict, limit: int, api: BestChange) -> json:
    rates = rate_processor(pairs, limit, api)
    result = json.dumps(rates, indent=2, ensure_ascii=False)
    return result
