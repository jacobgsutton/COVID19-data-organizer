#!c:/Users/Jake/AppData/Local/Programs/Python/Python38/python.exe

'''Script to control excution of getting data from JHU CSSE, adding all US data to a database, and updating a simple amcharts.com graph for florida COVID19 cases.'''

import datetime
import requests

from rw_data import addNewDayData, commit, close
from update_chart import updateChart

__author__ = 'Jake Sutton'
__copyright__ = 'Copyright 2020, www.jakegsutton.com'

__license__ = 'MIT'
__email__ = 'jakesutton1249@gmail.com'
__status__ = 'Development'


#Dictionary for all states with data from the entire loaded file
us_data_dict = {}


#Get date info needed
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

formated_todays_date = datetime.date.strftime(today, '%m-%d-%Y')
formated_yesterdays_date = datetime.date.strftime(yesterday, '%m-%d-%Y')


#Html request to JHU CSSE COVID-19 git repo
response = None
try:
    print('Getting data...')
    response = requests.get('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/' + formated_todays_date + '.csv')
    response.raise_for_status()
except requests.HTTPError as e:
    print(e, 'Looking for data elsewhere...')
    try:
        response = requests.get('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/' + formated_yesterdays_date + '.csv')
    except requests.exceptions.RequestException as e:
        print('NO DATA FOUND... YESTERDAYS FILE MUST NOT EXIST... FATAL ERROR...')
        raise SystemExit(e)


#Get text from request       
data = response.text


def createProvStateList():
    '''Function to create a list of all the province/states in the data set.'''
    l = []
    for i,d in enumerate(data):
        if i < len(data)-1 and d == '\n':
            l.append(data[i+1 : data.index(',', i)])
    return l


#Grabbing some data and putting it in lists (setup for generating dictionaries)
data_categories = data[0 :  data.index('\n')].split(',')
data_categories_2 = data[data.index(',')+1 :  data.index('\n')].split(',')
province_state_list = createProvStateList()


def generateUSDict():
    '''Generates a dictory with all data from the file.'''
    us_data = []

    for state in province_state_list:
        us_data.append(data[data.index(state)+len(state)+1 : data.index('\n', data.index(state))].split(','))

    for i, key in enumerate(province_state_list):
        us_data_dict[key] = {}
        for cat in data_categories_2:
            for val in us_data[i]:
                us_data_dict[key][cat] = val
                us_data[i].remove(val)
                break


#Calls the fuction to create the main data dictionary
generateUSDict()

#Calls fuction in store_data module to store data that is in us_data_dict in remote sql server
addNewDayData(us_data_dict,today)

#Commits changes to the datebase
commit()

#Calls function that executes selenium commands to add data from server to my amcharts.com Florida COVID19 cases chart 
updateChart(today)

#Closes the database connection
close()

print('Process complete...')