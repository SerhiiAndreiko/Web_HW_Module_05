import asyncio
import logging
import json
import pathlib
import aiohttp
import sys
from datetime import date, timedelta

TODAY = date.today()
BASE_DIR = pathlib.Path()

SLEEP_TIME = 0.5

def get_date_list(days):
    date_list = []
    for d in range(days):
        dt_days = TODAY - timedelta(d)
        dt = f"{dt_days:%d.%m.%Y}"
        date_list.append(dt)
    return date_list

async def request_privat(session, dt):
    url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={dt}'
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            result = await response.json()
            return result
    except (aiohttp.ClientConnectorError, aiohttp.ClientResponseError) as e:
        logging.error(f"Error fetching data for {dt}: {e}")
        return None

async def request_privat_multiple_days(session, date_list):
    results = await asyncio.gather(*[request_privat(session, dt) for dt in date_list])
    return [result for result in results if result is not None]

async def main_request(*argv):
    try:
        days = int(sys.argv[1])
        if days <= 10:
            async with aiohttp.ClientSession() as session:
                dt_list = get_date_list(days)
                results = await request_privat_multiple_days(session, dt_list)

            with open(BASE_DIR.joinpath('./data.json'), 'w', encoding='utf-8') as fd:
                json.dump(results, fd, ensure_ascii=False, indent=5)

        else:
            print('You can use a maximum of 10 days')
    except ValueError:
        logging.error("Invalid input for days.")
        sys.exit(1)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")
    asyncio.run(main_request())

