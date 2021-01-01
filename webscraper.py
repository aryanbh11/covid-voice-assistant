from bs4 import BeautifulSoup
import requests
# lxml


class Scraper:

    def __init__(self):
        self.TOTAL_CASES = {}
        self.TOTAL_DEATHS = {}
        self.RECOVERED = {}
        self.ACTIVE_CASES = {}
        self.CRITICAL_CASES = {}
        self.TESTS_CONDUCTED = {}
        self.countries = []
        self.update_data()

    def get_regions(self):
        return self.countries

    def get_cases(self, region='world'):
        try:
            return self.TOTAL_CASES[region]
        except KeyError:
            return None

    def get_deaths(self, region='world'):
        try:
            return self.TOTAL_DEATHS[region]
        except KeyError:
            return None

    def get_recovered(self, region='world'):
        try:
            return self.RECOVERED[region]
        except KeyError:
            return None

    def get_active_cases(self, region='world'):
        try:
            return self.ACTIVE_CASES[region]
        except KeyError:
            return None

    def get_critical_cases(self, region='world'):
        try:
            return self.CRITICAL_CASES[region]
        except KeyError:
            return None

    def get_tests_conducted(self, region='world'):
        try:
            return self.TESTS_CONDUCTED[region]
        except KeyError:
            return None

    def update_data(self):
        self._reset()
        # Fetching all data from website
        html_text = requests.get('https://www.worldometers.info/coronavirus/#countries').text

        # Setting up beautiful soup
        soup = BeautifulSoup(html_text, 'lxml')
        all_data = []

        # Fetching particular data using BeautifulSoup
        body = soup.find('tbody')
        countries_html = body.find_all('a', class_='mt_a')
        all_data_html = body.find_all('td')

        # List of countries
        for country in countries_html:
            self.countries.append(country.text.lower())

        # Data Cleaning
        i = 0
        while i < len(all_data_html):
            element = all_data_html[i].text.replace('\n', '').lower()
            if element == 'world':
                self.TOTAL_CASES[element] = all_data_html[i + 1].text.replace('\n', '').replace(' ', '').lower()
                self.TOTAL_DEATHS[element] = all_data_html[i + 3].text.replace('\n', '').replace(' ', '').lower()
                self.RECOVERED[element] = all_data_html[i + 5].text.replace('\n', '').replace(' ', '').lower()
                self.ACTIVE_CASES[element] = all_data_html[i + 7].text.replace('\n', '').replace(' ', '').lower()
                self.CRITICAL_CASES[element] = all_data_html[i + 8].text.replace('\n', '').replace(' ', '').lower()
                self.TESTS_CONDUCTED[element] = all_data_html[i + 11].text.replace('\n', '').replace(' ', '').lower()
                i += 11
            if element in self.countries:
                j = 0
                while j < 12:
                    all_data.append(all_data_html[i].text.replace('\n', '').replace(' ', '').lower())
                    i += 1
                    j += 1
            i += 1

        # Data Sorting
        i = 0
        while i < len(all_data) - 11:
            self.TOTAL_CASES[all_data[i]] = all_data[i + 1]
            self.TOTAL_DEATHS[all_data[i]] = all_data[i + 3]
            self.RECOVERED[all_data[i]] = all_data[i + 5]
            self.ACTIVE_CASES[all_data[i]] = all_data[i + 7]
            self.CRITICAL_CASES[all_data[i]] = all_data[i + 8]
            self.TESTS_CONDUCTED[all_data[i]] = all_data[i + 11]
            i += 12

        self.countries.insert(0, 'world')

    def _reset(self):
        self.TOTAL_CASES = {}
        self.TOTAL_DEATHS = {}
        self.RECOVERED = {}
        self.ACTIVE_CASES = {}
        self.CRITICAL_CASES = {}
        self.TESTS_CONDUCTED = {}
        self.countries = []


'''
TESTING:
scraper = Scraper()
print(scraper.get_regions())
print(scraper.get_cases())
print(scraper.get_deaths())
print(scraper.get_recovered())
print(scraper.get_tests_conducted('india'))
'''