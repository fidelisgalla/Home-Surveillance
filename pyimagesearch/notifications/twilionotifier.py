# import the necessary packages
from twilio.rest import Client
import dropbox
import os


class TwilioNotifier: 

    def __init__(self, conf):
        # store the configuration object
        self.conf = conf 

    def upload(self,path):
        #os.chdir('C:\\Users\\admin1\\pic\\') #for the raspberry application, we do not need to do this
        dbx = dropbox.Dropbox(self.conf['dropbox_access_token'])
        files = os.listdir(path)
        dropbox_path = '/'
        for file_name in files:
            with open (os.path.join(path,file_name),'rb') as f:
                dbx.files_upload(f.read(),dropbox_path+file_name,mute=True)
    
    def get_dropbox_url(self):
        dropboxpath='/'
        dbx = dropbox.Dropbox(self.conf['dropbox_access_token'])
        file_paths = [(dbx.files_get_temporary_link(path=os.path.join(dropboxpath,entry.name))).link for entry in dbx.files_list_folder('').entries] 
        return file_paths
    
    def dropbox_delete(self):
        pass
                
    def send_message(self,msg,url):
        account_sid = self.conf["twilio_sid"]
        auth_token = self.conf["twilio_auth"]
        client = Client(account_sid,auth_token)
        message = client.messages.create(body =msg,media_url=self.get_dropbox_url()[1],from_=self.conf['twilio_from'],to =self.conf["twilio_to"])
        return message