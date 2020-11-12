'''
This module provides functionality to read/write data to a db. Connects to a ClearDB mysql database hosted on a Heroku server and provides a function designed to send one days worth 
of data to a table called us_covid19_data. It also provides a fuction to get a specific states's data from a specific date from the same table.
'''

from datetime import datetime
from datetime import date

import MySQLdb as sql

from configuration_vars import sql_database, sql_host, sql_password, sql_user
from send_console_sms import Log

__author__ = 'Jake Sutton'
__copyright__ = 'Copyright 2020, www.jakegsutton.com'

__license__ = 'MIT'
__email__ = 'jakesutton1249@gmail.com'
__status__ = 'Production'


#Gets the log instance that already exist since log is a singleton
log = Log()

#data base setup
db = sql.connect(host=sql_host,
                 user=sql_user,
                 passwd=sql_password,
                 db=sql_database)

cur = db.cursor()


def fillNulls(str_):
    '''Helper fuction that looks at the sql command string and fills in nulls where data is missing after a comma.'''
    flag = False
    str_new = str_
    offset = 0
    for i,char in enumerate(str_):
        if char == ',' or char == ')':
            if flag == True:
                str_new = str_new[:i-1+offset] + ' null' + str_new[i+offset:]
                offset += 4
            else:    
                flag = True
        elif char != ' ':
            flag = False
    return str_new

  
def addNewDayData(dict, date_):
    '''Adds one days worth of US COVID19 data to the bulk us_covid19_data table plus a null row to ditinguish between different data additions to the table.'''
    i = 0
    do = 'insert into us_covid19_data '
    print(log.logIt('Updating database...'))
    for state in dict:
        print('Executing insert... Value returned was', cur.execute(do + "(Province_State, Country_Region, Date_, Last_Update, Lat, Long_, Confirmed, Deaths, "
                    "Recovered, Active_, FIPS, Incident_Rate, Total_Test_Results, People_Hospitalized, Case_Fatality_Ratio, UID, ISO3, Testing_Rate, "
                    "Hospitalization_Rate) values" + fillNulls("('{0}', '{1}', '{2}', '{3}', {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, '{16}', {17}, {18});"
                    .format(state,dict[state]['Country_Region'],date.strftime(date_, '%Y-%m-%d'),dict[state]['Last_Update'],dict[state]['Lat'],dict[state]['Long_'],dict[state]['Confirmed'],
                    dict[state]['Deaths'],dict[state]['Recovered'],dict[state]['Active'],dict[state]['FIPS'],dict[state]['Incident_Rate'],dict[state]['Total_Test_Results'],
                    dict[state]['People_Hospitalized'],dict[state]['Case_Fatality_Ratio'],dict[state]['UID'],dict[state]['ISO3'],dict[state]['Testing_Rate'],
                    dict[state]['Hospitalization_Rate']))))
        i += 1
    cur.execute(do + 'values(default,default,default,default,default,default,default,default,default,default,default,default,default,default,default,default,default,default,default,default);')
    log.logIt('Executing insert... x' + str(i))

    
def getStateData(state='Florida', date_='0', cap_id=10000000):
    '''
    Returns a tuple with a certain state's data on a certain date (format: YYYY-MM-DD). This is retrieved from the database. 
    If date is unknown then cap_id can be used to find all the rows before the row with cap_id that has the state in it its contents (cap_id is noninclusive). 
    At that point this fuction would return a list of tuples. If cap_id and date are provided, date is ignored.
    '''
    if date_ != '0' and cap_id == 10000000: 
        try:
            datetime.strptime(date_, '%Y-%m-%d')
            cur.execute("select * from us_covid19_data where Province_State = '{0}' and Date_ = '{1}';".format(state, date_))     
            return cur.fetchall()[0]
        except ValueError:
            print(log.logIt('Incorrect date format... should be YYYY-MM-DD.'))
    cur.execute("select * from us_covid19_data where Province_State = '{0}' and id < {1};".format(state, cap_id))
    return cur.fetchall()

  
def commit():
    '''Commits changes to the database.'''
    print(log.logIt('Commiting changes...'))
    db.commit()

    
def close():
    '''Closes the connection to the datebase.'''
    print(log.logIt('Closing connection...'))
    db.close()
