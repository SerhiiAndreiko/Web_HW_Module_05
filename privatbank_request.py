import aiohttp
import logging
import asyncio
import json
import pathlib
from datetime import date, timedelta

TODAY = date.today()
BASE_DIR = pathlib.Path()

async def get_privatbank_data(session, dt):
    url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={dt:%d.%m.%Y}'

    try:
        async with session.get(url) as response:
            response.raise_for_status()
            result = await response.json()
            return result
    except aiohttp.ClientError as e:
        logging.error(f"Error connecting to PrivatBank API: {e}")
        return None

async def request_privat(date_list):
    async with aiohttp.ClientSession() as session:
        tasks = [get_privatbank_data(session, dt) for dt in date_list]
        results = await asyncio.gather(*tasks)
        return results

async def main_request(days):
    try:
        dt_list = [TODAY - timedelta(d) for d in range(days)]
        results = await request_privat(dt_list)

        if results:
            with open(BASE_DIR.joinpath('./data.json'), 'w', encoding='utf-8') as fd:
                json.dump(results, fd, ensure_ascii=False, indent=5)

            return 'Data saved to data.json'
        else:
            return 'Failed to retrieve data from PrivatBank API'

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return 'An error occurred while processing the request'
