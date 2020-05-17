# import the necessary packages
from twilio.rest import Client
import dropbox
import os


class Notifications: 

    def __init__(self, conf):
        # store the configuration object
        self.conf = conf 
              
    def send_message(self,msg,url):
        account_sid = self.conf["twilio_sid"]
        auth_token = self.conf["twilio_auth"]
        client = Client(account_sid,auth_token)
        message = client.messages.create(body =msg,media_url=url,from_=self.conf['twilio_from'],to =self.conf["twilio_to"])
        return message

        