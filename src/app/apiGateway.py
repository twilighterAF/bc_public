from bestchange_api import BestChange

api = BestChange(load=False)


def get_api():
    return api


def call_api():
    api.load()