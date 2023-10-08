import logging
import json
import pathlib
import asyncio
import sys
from privatbank_request import main_request

BASE_DIR = pathlib.Path()

async def main(days, cur_1, cur_2):
    result = await main_request(days)

    if result == 'Data saved to data.json':
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

                    formatted_result = []

                    for res_dict in result:
                        for date, currencies in res_dict.items():
                            formatted_dict = {
                                date: {
                                    cur: {
                                        'sale': values['sale'],
                                        'purchase': values['purchase']
                                    }
                                    for cur, values in currencies.items()
                                }
                            }
                            formatted_result.append(formatted_dict)

                    current_dir = pathlib.Path.cwd()

                    with open(current_dir.joinpath('cur_exch.json'), 'w', encoding='utf-8') as fd:
                        json.dump(formatted_result, fd, ensure_ascii=False, indent=2)
                        print("Data saved to cur_exch.json")

    else:
        print(result)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 main.py <days> <currency_1> <currency_2>")
        sys.exit(1)

    days = int(sys.argv[1])
    cur_1 = sys.argv[2]
    cur_2 = sys.argv[3]

    if days < 1 or days > 10:
        print("Number of days should be between 1 and 10.")
    else:
        logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")
        asyncio.run(main(days, cur_1, cur_2))
