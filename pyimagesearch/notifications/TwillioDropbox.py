# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 19:31:12 2020

@author: Fidelis
"""

from twilio.rest import Client
from threading import Thread
import dropbox

class TwilioNotifier:
    def __init__(self, conf):
		# store the configuration object
        self.conf = conf

    def send(self,tempimage,msg,ts):
		# start a thread to upload the file and send it
        t = Thread(target=self._send, args=(tempimage,msg,ts))
        t.start()
        t.join()

    def _send(self,tempimage,msg,ts):
        dbx = dropbox.Dropbox(self.conf["dropbox_access_token"])
        print("[SUCCESS] dropbox account linked")
        path = "/{base_path}/{timestamp}.jpg".format(
					   base_path=self.conf["dropbox_base_path"], timestamp=ts)
        dbx.files_upload(open(tempimage.path, "rb").read(), path)
        print("[UPLOAD] file {}.jpg...".format(ts))
        
        #get the temporary link of the files
        
        url = dbx.files_get_temporary_link(path)
        print("[GET URL] file {}.jpg url...".format(ts))
				
		# initialize the twilio client and send the message
        print("[SENDING] file {}.jpg url...".format(ts))
        client = Client(self.conf["twilio_sid"],
			self.conf["twilio_auth"])
        client.messages.create(to=self.conf["twilio_to"], 
			from_=self.conf["twilio_from"], body=msg, media_url=url.link)

		# delete the file from dropbox
        print("[DELETE] file {}.jpg".format(ts))
        dbx.files_delete(path)
		