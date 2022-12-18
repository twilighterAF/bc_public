import time
import datetime
import threading

from bestchange_api import BestChange
from loguru import logger


class API:

    def __init__(self, api_instance: BestChange):
        self._api = api_instance
        self._timestamp = datetime.datetime.now()
        self._call_status = False
        self._TIMELIMIT = 5

    def get_call_status(self) -> bool:
        return self._call_status

    def set_call_status(self, status: bool):
        """
        Status change prevents api overload.
        True while has at least 1 client sending requests.
        If time last request greater than TIMELIMIT - set to false
        """

        self._call_status = status

    def call_api(self):
        self._api.load()

    def get_api(self) -> BestChange:
        return self._api

    def get_timestamp(self) -> datetime:
        return self._timestamp

    def set_timestamp(self, timestamp: datetime):
        self._timestamp = timestamp

    @logger.catch()
    def _api_loop(self):
        while self.get_call_status():
            timestamp = datetime.datetime.today().minute - self.get_timestamp().minute
            self.call_api()
            logger.debug(f'Api call {self.get_api()}')
            time.sleep(1)
            if timestamp >= self._TIMELIMIT:
                self.set_call_status(False)

    @logger.catch()
    def start_api_loop(self):
        """Call this method"""
        if not self.get_call_status():
            try:
                self.set_call_status(True)
                threading.Thread(target=self._api_loop, name='api_loop', daemon=True).start()

            except Exception:
                self.set_call_status(False)
                raise InterruptedError


API_BEST_CHANGE = API(BestChange(load=False, cache_seconds=35))
