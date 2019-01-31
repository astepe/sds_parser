from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import csv
from sds_parser.parser import sds_parser, ChemicalData
from tqdm import tqdm
from time import sleep


class SigmaConfigs:

    BASEURL = "https://www.sigmaaldrich.com/catalog/search?term=potassium&interface=All&N=0&mode=match%20partialmax&lang=en&region=US&focus=product"
    SDS_FOLDER = os.getcwd() + '/sigma_aldrich_sds/'
    PROFILE = webdriver.FirefoxProfile('/home/ari/.mozilla/firefox/fqt1kmcn.default-1544991237172')

    def __init__(self):
        self.url = self.BASEURL


def sigma_scraper():

    clear_sds_folder()

    sigma = SigmaConfigs()

    with open('sigma_sds_data.csv', 'w+') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([category.name for category in ChemicalData.CATEGORIES])

        while sigma.url:

            if sigma.url != SigmaConfigs.BASEURL:
                print('scanning next page!')

            scan_page(sigma.url, csv_writer)

            sigma.url = get_next_page_url(sigma.url)


def scan_page(url, csv_writer):

    # open new window
    driver = webdriver.Firefox(SigmaConfigs.PROFILE)
    driver.get(url)
    driver.implicitly_wait(30)

    link_actions = []

    sds_buttons = driver.find_elements_by_class_name('msdsBulletPoint')
    for idx, button in enumerate(sds_buttons):
        link_action = button.get_attribute('href')
        link_actions.append(link_action)
        print(link_action)

    for action in link_actions:
        try:
            driver.execute_script(action)
        except:
            print('Null JS action')
        sleep(5)
        driver.get(url)
        driver.implicitly_wait(30)

        # gather data and write row to csv if file exists
        if len(os.listdir(SigmaConfigs.SDS_FOLDER)) != 0:
            chemical_data = get_data_from_pdf()
            if chemical_data:
                csv_writer.writerow(chemical_data)
            clear_sds_folder()


def clear_sds_folder():

    for file in os.listdir(SigmaConfigs.SDS_FOLDER):
        os.remove(os.path.join(SigmaConfigs.SDS_FOLDER, file))


def get_data_from_pdf():
    old_file_name = SigmaConfigs.SDS_FOLDER + os.listdir(SigmaConfigs.SDS_FOLDER)[0]
    new_file_name = old_file_name.split('.')[0] + '.pdf'
    os.rename(old_file_name, new_file_name)
    chemical_data = sds_parser(new_file_name)
    return chemical_data


def get_next_page_url(url):
    driver = webdriver.Firefox(SigmaConfigs.PROFILE)
    driver.implicitly_wait(30)
    driver.get(url)
    driver.implicitly_wait(30)
    next_page_button = driver.find_element(By.XPATH, '//a[@rel="next"]')
    next_page_url = ''
    if next_page_button:
        next_page_url = SigmaConfigs.BASEURL + next_page_button.get_attribute('href')
    driver.close()
    return next_page_url


def get_num_sds_on_page(url):
    driver = webdriver.Firefox(SigmaConfigs.PROFILE)
    driver.implicitly_wait(30)
    driver.get(url)
    driver.implicitly_wait(30)
    sds_count = len(driver.find_elements_by_class_name('msdsBulletPoint'))
    driver.close()
    return sds_count


if __name__ == '__main__':
    sigma_scraper()
