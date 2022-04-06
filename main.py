#
# Made by dkrwng (https://www.fiverr.com/drkwng)
# Telegram: @drkwng_dck
# Email: iamdrkwng@gmail.com
#

import csv
import os
from parser_dreame.parser import DreameParser


def csv_writer(filename, mode, data):
    with open(filename, 'w' if mode == 0 else 'a', encoding='utf-8', newline='') as res_file:
        writer = csv.writer(res_file, delimiter=';')
        if mode == 0:
            heading = ['AUTHOR_LINK', 'BOOK_SEEN']
            writer.writerow(heading)
        writer.writerow(data)


if __name__ == "__main__":
    path = os.getcwd()
    result_path = path + '\\results\\result.csv'

    urls_file = input('Enter URLs filename: ').strip()
    with open(urls_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f]

    parser = DreameParser()

    while True:
        for num, url in enumerate(urls):
            if 'http' in url:
                try:
                    for work in parser.worker(url):
                        print(f'Found data {work} \n'
                              f'Writing to CSV file')
                        csv_writer(result_path, num, work)

                except Exception as err:
                    print('Main loop err: ', err, type(err))

        break

    print(f'Done! Please check results here \n'
          f'{result_path}')
