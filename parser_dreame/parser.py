import os
import logging

from time import sleep
from random import randint

from queue import Queue

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from fake_useragent.fake import UserAgent


class DreameParser:
    def __init__(self):
        self.crawl_queue = Queue()
        self.books_queue = Queue()
        self.ua = {'user-agent': UserAgent().chrome}

        self.pages_cnt_xpath = "//ul[@class='pagination']/li[last()]"
        self.cat_list_xpath = "//li[@class='book clearfix']"
        self.elem_lang_xpath = "//div[@class='stat']/img[@class='stat-lang pull-right']"
        self.elem_book_xpath = "//h3[@class='name']/a"
        self.author_page_xpath = "//a[@class='author-page']"
        self.author_badge_xpath = "//img[@class='next-top-writer']"

        # Selenium setup
        os.environ["WDM_LOG_LEVEL"] = "0"
        options = Options()
        # options.add_argument('--headless')
        options.add_argument(f"user-agent={self.ua}")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--profile-directory=Default")
        options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    @staticmethod
    def url_maker(
            category='-1',
            update_time='0',
            letter='',
            sort_by='0'
    ):
        """
        Make a start URL for crawler (category='-1' is 'All' filter)
        """
        url = f"https://www.dreame.com/search/stack?" \
              f"category={category}" \
              f"&updateTime={update_time}" \
              f"&letter={letter}" \
              f"&sortBy={sort_by}"
        return url

    def page_extract_data(self, url, xpath_cond):
        """
        Crawl URL and get data by xpath_cond
        """
        try:
            self.driver.get(url)
            data = self.driver.find_elements(by=By.XPATH, value=xpath_cond)
            return data

        except Exception as err:
            logging.error('Parser page_extract_data(): ', err, type(err))
            return None

    @staticmethod
    def elem_extract_data(element, xpath_cond):
        """
        Get data from Webelement
        """
        try:
            data = element.find_element(by=By.XPATH, value=xpath_cond)
            return data

        except Exception as err:
            logging.error('Parser elem_extract_data(): ', err, type(err))
            return None

    def get_cat_pages(self, url, pages_cnt):
        """
        Generate cat URLs list and put it to the crawl queue
        """
        cat_urls = list()
        if "pn=" not in url:
            for i in range(1, pages_cnt):
                if "?" in url:
                    cat_urls.append(url + f"&pn={i+1}")
                else:
                    cat_urls.append(url + f"?pn={i+1}")

        for elem in cat_urls:
            self.crawl_queue.put(elem)

        return self.crawl_queue

    def worker(self, start_url):
        self.crawl_queue.put(start_url)

        # Get amount of pagination pages, generate cat pages and add them to queue
        pages_cnt = self.page_extract_data(start_url, self.pages_cnt_xpath)[0]
        if pages_cnt:
            pages_cnt = int(pages_cnt.get_attribute("data-index"))
            self.get_cat_pages(start_url, pages_cnt)

        while not self.crawl_queue.empty():
            url = self.crawl_queue.get()
            print(f'{url} parsing')

            if '/search/' in url:
                # If URL is a catalog page then get books URLs without lang badges
                cat_list = self.page_extract_data(url, self.cat_list_xpath)
                for elem in cat_list:
                    lang = self.elem_extract_data(elem, self.elem_lang_xpath)
                    # If no lang badge found
                    if not lang:
                        book_link = elem.elem_extract_data(elem, self.elem_book_xpath).\
                            get_attribute("href")
                        self.crawl_queue.put(book_link)

            else:
                # Else URL is a book page. Crawl author URL and check badge presence
                author_link = self.page_extract_data(url, self.author_page_xpath)[0]\
                    .get_attribute("href")
                next_top = self.page_extract_data(author_link, self.author_badge_xpath)
                # If is not None
                if next_top is not None:
                    yield author_link, url

            sleep(randint(2, 5))

        self.driver.close()
        self.driver.quit()


if __name__ == "__main__":
    url1 = 'https://www.dreame.com/search/stack'
    url2 = 'https://www.dreame.com/search/stack?category=1&updateTime=0&letter=&kw=&sortBy=0&subTabType='
    url3 = 'https://www.dreame.com/search/stack?category=1&updateTime=0&letter=&kw=&sortBy=0&subTabType=&pn=3'
    parser = DreameParser()
    print([work for work in parser.worker(url1)])
