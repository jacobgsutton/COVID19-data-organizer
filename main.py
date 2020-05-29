import datetime
import io
import requests

#dictionary for florida's data specifically
florida_data_dict = {}

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

#grabbing some data and putting it in lists
data_categories = data[0 :  data.index('\n')].split(',')
florida_data = data[data.index('Florida') : data.index('\n', data.index('Florida'))].split(',')

#set up florida dict
for key in data_categories:
    for val in florida_data:
        florida_data_dict[key] = val
        florida_data.remove(val)
        break


#testing prints
print(florida_data_dict)
print(florida_data_dict['Confirmed'])