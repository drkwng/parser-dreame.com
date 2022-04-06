
import csv

import os
import logging

from parser_dreame.parser import DreameParser


def csv_writer(filename, mode, data):
    with open(filename, mode, encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        if mode == 0:
            heading = ['AUTHOR_LINK', 'BOOK_SEEN']
            writer.writerow(heading)
        writer.writerow(data)


if __name__ == "__main__":
    path = os.getcwd()

    result_path = path + '\\results\\result.csv'

    logs_file = path + '\\logs\\errors.log'
    logging.basicConfig(level=logging.ERROR, filename=logs_file)

    parser = DreameParser()

    while True:
        start_url = input('Enter a valid start URL: ').strip()
        try:
            if 'http' in start_url:
                for num, work in enumerate(parser.worker(start_url)):
                    print(f'Found data {work} \n'
                          f'Writing to CSV file')
                    csv_writer(result_path, num, work)
                break

            else:
                print('Please enter a valid URL')

        except Exception as err:
            logging.error('main loop error: ', err)
            print(err)
            break

    print(f'Done! Please check results here \n'
          f'{result_path}')
