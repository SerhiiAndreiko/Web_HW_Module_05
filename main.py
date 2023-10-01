import logging
import json
import argparse
import asyncio
from request_privat import main_request  
import pathlib

BASE_DIR = pathlib.Path()

async def main(days, currency, cur_1="EUR", cur_2="USD"):
    request = await main_request(currency)

    if request:
        with open(BASE_DIR.joinpath('data.json'), 'r', encoding='utf-8') as f:
            d = json.load(f)

            with open(BASE_DIR.joinpath('cur_list.json'), 'r', encoding='utf-8') as f_cur_list:
                d_cur_list = json.load(f_cur_list)

                if cur_1 in d_cur_list and cur_2 in d_cur_list:
                    result = []

                    for elem in d[:days]:
                        dt = elem.get('date')
                        res_dict = {dt: {}}

                        for rate_elem in elem.get('exchangeRate'):
                            currency = rate_elem.get('currency')

                            if currency == cur_1:
                                res_dict[dt][cur_1] = {
                                    'sale': rate_elem.get('saleRate'),
                                    'purchase': rate_elem.get('purchaseRate')
                                }

                            if currency == cur_2:
                                res_dict[dt][cur_2] = {
                                    'sale': rate_elem.get('saleRate'),
                                    'purchase': rate_elem.get('purchaseRate')
                                }

                        result.append(res_dict)

                    with open(BASE_DIR.joinpath('./cur_exch.json'), 'w', encoding='utf-8') as fd:
                        json.dump(result, fd, ensure_ascii=False, indent=5)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exchange Rate Information")
    parser.add_argument('days', type=int, help="Number of days (up to 10)")
    parser.add_argument('currency', help="Currency code")
    parser.add_argument('cur_1', nargs='?', default="EUR", help="First currency code")
    parser.add_argument('cur_2', nargs='?', default="USD", help="Second currency code")

    args = parser.parse_args()

    if args.days < 1 or args.days > 10:
        print("Кількість днів повинна бути від 1 до 10.")
    else:
        logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")
        asyncio.run(main(args.days, args.currency, args.cur_1, args.cur_2))
