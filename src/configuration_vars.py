'''Provides the configuration variables by parsing the configuration file.'''

from configparser import ConfigParser

__author__ = 'Jake Sutton'
__copyright__ = 'Copyright 2020, www.jakegsutton.com'

__license__ = 'MIT'
__email__ = 'jakesutton1249@gmail.com'
__status__ = 'Production'


config = ConfigParser()
config.read('config.ini')

#sql
sql_host = config['sql']['host']
sql_user = config['sql']['user']
sql_password = config['sql']['password']
sql_database = config['sql']['database']

#amcharts
amcharts_password = config['amcharts']['password']
my_chart = config['amcharts']['my_chart']

#twilio
twilio_sid = config['twilio']['account_sid']
twilio_auth = config['twilio']['auth_token']
my_cell = config['twilio']['my_cell']
twilio_cell = config['twilio']['my_twilio']
