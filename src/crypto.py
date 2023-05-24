import sys

import ujson
import aiohttp
import json
import asyncio

from logger import log_twice
from utils import *


class Crypto:
    trades_url = 'https://yobit.net/api/3/ActiveOrders/'
    crypto_currency = "eth_usd"

    def __init__(
            self,
            time_trigger: int = 60 * 60,     # which is the time_step before checking the percent of increasing
            percents_trigger: float = 1,     # 1 % of every timestep increasing
            request_data_limit: int = 20     # 20 datalines per request
    ):
        self.check_values(time_trigger, percents_trigger, request_data_limit)

        self._time_trigger = time_trigger
        self._percents_trigger = percents_trigger
        self._request_data_limit = int(request_data_limit)

        # data of the program
        self.last_data: dict | None = None
        self.last_time: float | None = None
        self.step_data: dict | None = None

    def check_values(self, secs: float, percents: float, limit: int) -> bool:
        """Checks whether all arguments are valid."""
        if 10**(-7) < secs < 10**3 and 0 < percents <= 100 and 0 < limit < 100:
            return True
        else:
            log_twice("error", f"Incorrect data is given as {self.__class__.__name__}() arguments")
            self.shutdown()

    def shutdown(self):
        """Shutting down the program after looping or before."""
        if hasattr(self, '_loop'):
            self._loop.close()
        sys.exit()

    async def work(self):
        trading_url = self.trades_url + self.crypto_currency
        self._session = aiohttp.ClientSession(json_serialize=ujson.dumps)
        first_resp = await self.get_response(url_=trading_url)      # first time data is set to avoid condition check
                                                                    # on each interation of main cycle
        self.last_data = self.step_data = json.loads(first_resp)
        self.last_time = nowTime()
        while True:     # main worker cycle that gets data
            resp = await self.get_response(trading_url)
            data = json.loads(resp)[self.crypto_currency]
            # data is iterable with length <= self.request_data_limit
            for trade in data:
                print(trade)
                await asyncio.sleep(1)
                trade_data = trade['timestamp']
                trade_price = trade['price']
                trade_amount = trade['amount']
                total_price = trade_price * trade_amount
                # print(total_price)

            # это здоровый сон для корутины, на пару ms отдает GIL
            await asyncio.sleep(0)

    async def get_response(self, url_: str):
        """Get response from APIon this url_"""
        async with self._session.get(url=url_) as response:
            return await response.text()    # json raises an exception

    def run(self):
        """
        User interface to run the main-working process. Sets loop and futures, then runs them
        """
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        worker = asyncio.ensure_future(self.work(), loop=self._loop)
        worker.add_done_callback(callback)

        try:
            log_twice("info", "Loop is started successfully by user.")
            self._loop.run_forever()

        except KeyboardInterrupt:
            log_twice("info", "Loop is closed successfully by user.")

        except Exception as e:  # any exception
            log_twice("error", str(e))

        finally:
            self.shutdown()

