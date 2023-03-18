import threading
import urllib.request as urllibReq
from domain import get_domain_name
import sys
import logging
import inspect

from spyder.parser import Parser



class SpyderLogger(logging.Filter):
    def filter(self, record):
        # record.extract_line_num = line_num
        return True




class Spyder:
    """
        Cralwer class
        - Mutated Spider - Based on the universial web crawler by Bucky Roberts <https://thenewboston.com/>
    """

    def __init__(self, project_name, base_url, domain_name):
        self._project_name = project_name
        self._base_url = base_url
        self._domain_name = domain_name
        self._queue_file = self._project_name + '/_queue.txt'
        self._crawled_file = self._project_name + '/_crawled.txt'
        self._queue = ""
        self._crawled = ""
        self._crawler_type = 'General'
        self._crawler_purpose = 'Hate'
        self._domain_name = ''
        self._queue_file = ''
        self._crawled_file = ''
        self._queue = set()
        self._crawled = set()

        # ----------------LOGGER CONFIGURATION----------------#
        self.utils_logger = logging.getLogger('spyder-mod.utils')
        self.log_level = 'INFO'

        logger = logging.getLogger('spyder-mod')
        logger.setLevel(self.log_level)
        logger.addFilter(SpyderLogger())

        channel = logging.StreamHandler()
        channel.setLevel(self.log_level)

        formatter = logging.Formatter('%(asctime)s - %(name)-25s - %(filename)-15s - %(funcName)-20s - %(extract_line_num)-5s - %(levelname)-8s - %(message)s')
        channel.setFormatter(formatter)
        logger.addHandler(channel)

        if not self.utils_logger.hasHandlers():
            logger.addHandler(channel)


    def gather_links(self, page_url):
        html_string = ''
        try:
            response = urllibReq.urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html':
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            self.utils_logger.info('Successfully crawled: ' + page_url)
            self.utils_logger.info('Found: ' + str(len(self.find_links(html_string))) + ' links')
            return self.find_links(html_string)
        except Exception as e:
            self.utils_logger.error('Failed to crawl page: ' + page_url)
            self.utils_logger.error(str(e))
            return set()

    def find_links(self, html_string):
        """
            Crawler Link Parsing Helper Functions
         - Based on the universial web crawler by Bucky Roberts <https://thenewboston.com/>
        """
        links = set()
        try:
            start_link = html_string.find('<a href=')
            while start_link != -1:
                start_quote = html_string.find('"', start_link)
                end_quote = html_string.find('"', start_quote + 1)
                url = html_string[start_quote + 1:end_quote]
                if url.find('http') == -1:
                    continue
                links.add(url)
                start_link = html_string.find('<a href=', end_quote)
            return links
        except Exception as e:
            self.utils_logger.error('Failed to parse page: ' + html_string)
            self.utils_logger.error(str(e))
            return set()

    def add_links_to_queue(self, links):
        for url in links:
            if (url in self._queue) or (url in self._crawled):
                continue
            if self._domain_name != get_domain_name(url):
                continue
            self._queue.add(url)

    def update_files(self):
        self.set_to_file(self._queue, self._queue_file)
        self.set_to_file(self._crawled, self._crawled_file)


    def set_to_file(self, links, file):
        try:
            with open(file, 'w') as f:
                for l in sorted(links):
                    f.write(l + '')

        except Exception as e:
            self.utils_logger.error('Failed to write to file: ' + file)
            self.utils_logger.error(str(e))
            return set()




class ChanSpyder(Spyder):
    """
        4Chan | Kiwifarm Cralwer class
        -
    """

    def __init__(self, project_name, base_url, domain_name):
        super().__init__(project_name, base_url, domain_name)
        self._crawler_type = 'Chan'
        self._crawler_purpose = 'Hate'
        self._domain_name = domain_name
        self._queue_file = self._project_name + '/_queue.txt'
        self._crawled_file = self._project_name + '/_crawled.txt'
        self._queue = set()
        self._crawled = set()
        self.crawl_page('First spider', self._base_url)

    def crawl_page(self, thread_name, page_url):
        pass




class ReddSpyder(Spyder):
    """
        Reddit Cralwer class
        -
    """

    def __init__(self, project_name, base_url, domain_name):
        super().__init__(project_name, base_url, domain_name)
        self._crawler_type = 'Reddit'
        self._crawler_purpose = 'Hate'
        self._domain_name = domain_name
        self._queue_file = self._project_name + '/_queue.txt'
        self._crawled_file = self._project_name + '/_crawled.txt'
        self._queue = set()
        self._crawled = set()
        self.crawl_page('First spider', self._base_url)

    def crawl_page(self, thread_name, page_url):
        pass




class TwitSpyder(Spyder):
    """
        Twitter Cralwer class
        -
    """

    def __init__(self, project_name, base_url, domain_name):
        super().__init__(project_name, base_url, domain_name)
        self._crawler_type = 'Twitter'
        self._crawler_purpose = 'Hate'
        self._domain_name = domain_name
        self._queue_file = self._project_name + '/_queue.txt'
        self._crawled_file = self._project_name + '/_crawled.txt'
        self._queue = set()
        self._crawled = set()
        self.crawl_page('First spider', self._base_url)

    def crawl_page(self, thread_name, page_url):
        pass
