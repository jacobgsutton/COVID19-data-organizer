'''Provides class Log which has fucntionality to log strings and send the log through SMS to my phone using twilio.'''

from twilio.rest import Client

from configuration_vars import twilio_auth, twilio_cell, twilio_sid, my_cell

__author__ = 'Jake Sutton'
__copyright__ = 'Copyright 2020, www.jakegsutton.com'

__license__ = 'MIT'
__email__ = 'jakesutton1249@gmail.com'
__status__ = 'Production'


class Log:
    '''Log is a singleton class used to store a big string i.e. a log and it provides functionality to send the log via SMS to my phone.'''
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.client = Client(twilio_sid, twilio_auth)
        self.log = ''

    def logIt(self, val, one_nl=False):
        '''Adds a string to the log and returns the string passed in.'''  
        self.log += str(val)
        if one_nl:
            self.log += '\n'    
        else:
            self.log += '\n\n'
        return val

    def send(self):
        '''Sends the log to my phone using the twilio API.'''
        sms = self.client.messages.create(to=my_cell, from_=twilio_cell, body=self.log)

