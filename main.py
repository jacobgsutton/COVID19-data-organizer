#in development

import datetime
import io
import requests

#dictionary for all states with data from the entire loaded file
us_data_dict = {}

#get date info needed
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

formated_todays_date = datetime.date.strftime(today, '%m-%d-%Y')
formated_yesterdays_date = datetime.date.strftime(yesterday, '%m-%d-%Y')

#html request to JHU CSSE COVID-19 git repo
response = None
try:
    response = requests.get('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/' + formated_todays_date + '.csv')
    response.raise_for_status()
except requests.HTTPError as e:
    print(e, 'Looking for data elsewhere...')
    try:
        response = requests.get('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/' + formated_yesterdays_date + '.csv')
    except requests.exceptions.RequestException as e:
        print('NO DATA FOUND... YESTERDAYS FILE MUST NOT EXIST... FATAL ERROR...')
        raise SystemExit(e)

#get text from request       
data = response.text

#function to create a list of all the province/states in the data set
def createProvStateList():
    l = []
    i = 0
    for d in data:
        if i < len(data)-1 and d == '\n':
            l.append(data[i+1 : data.index(',', i)])
        i+=1
    return l

#grabbing some data and putting it in lists (setup for generating dicts)
data_categories = data[0 :  data.index('\n')].split(',')
data_categories_2 = data[data.index(',')+1 :  data.index('\n')].split(',')
province_state_list = createProvStateList()

#generates a dictory with all data from the file
def generateUSDict():
    i = 0
    us_data = []

    for state in province_state_list:
        us_data.append(data[data.index(state)+len(state)+1 : data.index('\n', data.index(state))].split(','))

    for key in province_state_list:
        us_data_dict[key] = {}
        for cat in data_categories_2:
            for val in us_data[i]:
                us_data_dict[key][cat] = val
                us_data[i].remove(val)
                break
        i += 1


#calls the fuction
generateUSDict()

#creates a var for florida dict
florida_data_dict = us_data_dict['Florida']

#testing prints
print(florida_data_dict['Confirmed'], '\n\n')

for state in province_state_list:
    print(state, ':', us_data_dict[state], '\n')
