import calendar
import datetime as dt
import json
import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import utils
from config import *


class ClearTax:
    def __init__(self):
        self.driver = self.get_driver()

    def get_driver(self, download_dir=DOWNLOAD_DIR):
        """Prepares chrome web driver with auto print as PDF set. 

        Returns:
            [selenium.webdriver.chrome.webdriver.WebDriver] -- Chrome webdriver
        """
        app_state = {
            'recentDestinations': [{
                'id': 'Save as PDF',
                'origin': 'local'
            }],
            'selectedDestinationId': 'Save as PDF',
            'version': 2
        }
        profile = {
            'printing.print_preview_sticky_settings.appState': json.dumps(app_state),
            'savefile.default_directory': download_dir
        }
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', profile)
        chrome_options.add_argument('--kiosk-printing')

        driver = webdriver.Chrome(chrome_options=chrome_options)
        return driver

    def fill_forms(self, start_date, end_date):
        def fill_first_form():
            # 1st Form elements
            # Rent element
            rent_elem = self.driver.find_element_by_name('Rent')
            rent_elem.clear()
            rent_elem.send_keys(MONTHLY_RENT)
            # TODO: Assert here

            # Address element
            addr_elem = self.driver.find_element_by_name('Address')
            addr_elem.clear()
            addr_elem.send_keys(HOUSE_ADDRESS)
            # assert "No results found." not in driver.page_source

            # Submit button
            submit_btn = self.driver.find_element_by_name('submit')
            submit_btn.click()

        def fill_second_form():
            # 2nd Form elements
            name_elem = self.driver.find_element_by_name('Name')
            name_elem.clear()
            name_elem.send_keys(NAME)

            email_elem = self.driver.find_element_by_name('UserEnteredEmail')
            email_elem.clear()
            email_elem.send_keys(EMAIL)

            owner_elem = self.driver.find_element_by_name('HouseOwnerName')
            owner_elem.clear()
            owner_elem.send_keys(OWNER)

            from_date_elem = self.driver.find_element_by_name('StartDate')
            from_date_elem.clear()
            from_date_elem.send_keys(start_date)

            to_date_elem = self.driver.find_element_by_name('EndDate')
            to_date_elem.clear()
            to_date_elem.send_keys(end_date)

        fill_first_form()
        time.sleep(2)
        fill_second_form()

    def print_receipt(self):
        generate_receipt_elem = self.driver.find_element_by_name('Get receipt')
        generate_receipt_elem.click()

        time.sleep(2)  # Replace with check for element existence.

        print_elem = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div/div/div/div[2]/a')
        print_elem.click()

    def download_rent_receipt(self, daterange):
        """Generates and downloads rent receipt for given date range.

        Arguments:
            daterange {tuple} -- Start date and end date
        """
        # Open Cleartax rent receipts page
        self.driver.get(URL)
        assert "FREE Rent Receipts" in self.driver.title

        time.sleep(2)  # TODO: Add custom wait

        # Fill forms
        start_date = f'{daterange[0]:{DATE_FORMAT}}'
        end_date = f'{daterange[1]:{DATE_FORMAT}}'
        self.fill_forms(start_date, end_date)

        # Print and save receipt
        self.print_receipt()

        time.sleep(2)

    def tear_down(self):
        self.driver.close()

    def rename_receipt(self, new_filename):
        filename = 'Create FREE Rent Receipts - Download Rent Receipt Format in PDF.pdf'
        filepath = os.path.join(DOWNLOAD_DIR, filename)
        new_filepath = os.path.join(DOWNLOAD_DIR, f'{new_filename}.pdf')
        new_filename = os.rename(filepath, new_filepath)


if __name__ == '__main__':
    cleartax = ClearTax()
    from_date = dt.date(2018, 4, 1)
    to_date = dt.date(2019, 3, 1)
    for date_range in utils.date_ranges(from_date, to_date):
        month, year = date_range[0].month, date_range[0].year
        filename = 'Rent-{}-{}'.format(calendar.month_name[month], year)
        cleartax.download_rent_receipt(date_range)
        cleartax.rename_receipt(filename)

    cleartax.tear_down()
