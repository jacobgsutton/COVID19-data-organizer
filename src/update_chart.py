'''Updates chart hosted on amcharts.com using selenium and chrome webdriver.'''

from datetime import date, datetime
import os
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

from rw_data import getStateData
from configuration_vars import amcharts_password
from send_console_sms import Log

__author__ = 'Jake Sutton'
__copyright__ = 'Copyright 2020, www.jakegsutton.com'

__license__ = 'MIT'
__email__ = 'jakesutton1249@gmail.com'
__status__ = 'Production'

#Categories of the data (used for console output)
CATS = ['Province_State', 'Country_Region', 'Date', 'Last_Update', 'Lat', 'Long', 'Confirmed', 'Deaths', 
     'Recovered', 'Active', 'FIPS', 'Incident_Rate', 'People_Tested', 'People_Hospitalized', 
     'Mortality_Rate', 'UID', 'ISO3', 'Testing_Rate', 'Hospitalization_Rate']

#Gets the log instance that already exist since log is a singleton
log = Log()

PATH = 'C:/WebDriver/bin/chromedriver_win32/chromedriver83.exe' #Local path
#PATH = os.environ.get('CHROMEDRIVER_PATH')

chrome_options =  webdriver.ChromeOptions()
#chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--disable-gpu') #For windows environment only

driver = webdriver.Chrome(executable_path=PATH, options=chrome_options)

driver.get('https://live.amcharts.com/')

wait = WebDriverWait(driver, 60)


def updateChart(date_): 
    '''Updates Florida COVID19 cumulative cases chart hosted on amcharts.com with selenium.'''
    todays_date_str = date.strftime(date_, '%Y-%m-%d')

    todays_florida_data = getStateData('Florida', todays_date_str)
    last_florida_data_list = getStateData(state='Florida',cap_id=todays_florida_data[19])
   
    florida_confirmed_today = todays_florida_data[6]
    
    if len(last_florida_data_list) != 0:
        florida_confirmed_last = last_florida_data_list[len(last_florida_data_list)-1][6]
    else:
        florida_confirmed_last = 0

    florida_confirmed_difference = florida_confirmed_today - florida_confirmed_last

    try:
        driver.find_element_by_xpath('/html/body/div/section[1]/header/div/div/div/nav/ul[1]/li[2]/a').click()

        driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/main/article/header/form/p[1]/input')))

        driver.find_element_by_xpath('/html/body/div/div/div/main/article/header/form/p[1]/input').send_keys(__email__)
        driver.find_element_by_xpath('/html/body/div/div/div/main/article/header/form/p[2]/input').send_keys(amcharts_password)
        driver.find_element_by_xpath('/html/body/div/div/div/main/article/header/form/p[5]/label/input').click()
        driver.find_element_by_xpath('/html/body/div/div/div/main/article/header/form/p[4]/input[1]').click()

        driver.switch_to.default_content()
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/section[1]/div[1]/div[2]/div/div/div/div[1]/div/table/tbody/tr[1]/td[1]/a')))

        driver.find_element_by_xpath('/html/body/div/section[1]/div[1]/div[2]/div/div/div/div[1]/div/table/tbody/tr[1]/td[1]/a').click()
        
        driver.switch_to.default_content()
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/section[2]/div/div[2]/div[2]/div[2]/div[2]/div[1]/ul[1]/li[1]/a/i')))

        driver.find_element_by_xpath('/html/body/div[1]/section[2]/div/div[2]/div[2]/div[2]/div[2]/div[1]/ul[1]/li[1]/a/i').click() 

        driver.execute_script('var rowCount = $("#am-editor-table").handsontable("countRows"); $("#am-editor-table").handsontable("setDataAtCell", [[rowCount - 1,0,"{0}"],[rowCount-1,1,{1}],[rowCount - 1,2,{2}]]);'
        .format(todays_date_str, florida_confirmed_today, florida_confirmed_difference))

        driver.find_element_by_xpath('/html/body/div[1]/section[2]/header/nav/ul[1]/li[1]/a').click()

        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div[3]/button')))

        driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[3]/button').click()

        time.sleep(5)

        print(log.logIt('Quiting selenium session... id: ' + str(driver.session_id)))
        driver.quit()

        output = ''
        for val, cat in zip(todays_florida_data, CATS):
            output += cat + ': '
            if isinstance(val, datetime):
                output += date.strftime(val, '%m/%d/%Y, %H:%M:%S') 
            elif isinstance(val, date):
                output += date.strftime(val, '%m/%d/%Y')      
            else:
                output += str(val)    
            output += '\n'

        print(log.logIt('All of Florida\'s data from the latest release (yesterday):\n' + output, one_nl=True))
        print(log.logIt('Note: Any values of "None" are categories that had no value in the original dataset. This is likely due to insufficient data verification for that category specifically...'))    
        print(log.logIt('Total cumulative florida cases as of latest release: ' + str(florida_confirmed_today)))
        print(log.logIt('Total cumulative florida cases before latest release: ' + str(florida_confirmed_last) + '\n\nTotal new cases (i.e. the differenece): ' + str(florida_confirmed_difference)))

    except WebDriverException as e:
        print(log.logIt('An error occurred during chart update... '))
        print(log.logIt(e))
        print(log.logIt('It is possible that the database was updated, however, the chart was not...'))
   
