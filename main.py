#
# Made by dkrwng (https://www.fiverr.com/drkwng)
# Telegram: @drkwng_dck
# Email: iamdrkwng@gmail.com
#

import csv
import os
from parser_dreame.parser import DreameParser


def csv_writer(filename, mode, data):
    with open(filename, mode, encoding='utf-8', newline='') as res_file:
        writer = csv.writer(res_file, delimiter=';')
        writer.writerow(data)


if __name__ == "__main__":
    # path = os.getcwd()
    result_path = 'results/result.csv'

    urls_file = input('Enter URLs filename: ').strip()
    with open(urls_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f]

    csv_heading = ['AUTHOR_LINK', 'BOOK_SEEN']
    csv_writer(result_path, 'w', csv_heading)

    parser = DreameParser()

    while True:
        for url in urls:
            if 'http' in url:
                try:
                    for work in parser.worker(url):
                        print(f'Found data {work} \n'
                              f'Writing to CSV file')
                        csv_writer(result_path, 'a', work)

                except Exception as err:
                    print('Main loop exception: ', err, type(err))

        break

    print(f'Done! Please check results here \n'
          f'{result_path}')
