
import csv

import os

from parser_dreame.parser import DreameParser


def csv_writer(filename, mode, data):

    with open(filename, 'w' if mode == 0 else 'a', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        if mode == 0:
            heading = ['AUTHOR_LINK', 'BOOK_SEEN']
            writer.writerow(heading)
        writer.writerow(data)


if __name__ == "__main__":
    path = os.getcwd()
    result_path = path + '\\results\\result.csv'

    parser = DreameParser()

    while True:
        start_url = input('Enter a valid start URL: ').strip()
        if 'http' in start_url:
            for num, work in enumerate(parser.worker(start_url)):
                print(f'Found data {work} \n'
                      f'Writing to CSV file')
                csv_writer(result_path, num, work)
            break

        else:
            print('Please enter a valid URL')

    print(f'Done! Please check results here \n'
          f'{result_path}')
