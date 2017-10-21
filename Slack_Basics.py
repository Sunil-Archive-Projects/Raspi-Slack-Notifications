#!/usr/bin/python
# coding: utf-8

# In[3]:


from slackclient import SlackClient #slack client
import os #to check if file exists for auth token
import platform #to get system details
from datetime import datetime #to print timestamp in the messages
import subprocess #
import urllib3 #check internet access
import time #to sleep for particular time at first bootup until
import re #for regex operations

# In[2]:

#create class for RasPi Utility Functions
class RasPi():
    
    def __init__(self):
        self.token = ""
        self.connection_ssid = False
        self.temperature = "0 C"
    
    #read token form slack_token.ini and initialize slack client
    #create token for your app from https://api.slack.com/custom-integrations/legacy-tokens

    def get_auth_token(self,tokenFilePath):
        if not os.path.isfile(tokenFilePath):
            print("File path {} does not exist. Exiting...".format(filepath))
            print("Create a File Named slack_token.ini and paste the Token")
            sys.exit()

        fp = open(tokenFilePath, 'r')  
        token = fp.read()
        fp.close()
        return token.strip()
    
    #send a slack message to a channel
    #api documentation at https://api.slack.com/methods/chat.postMessage#authorship
    def send_slackMessage(self,channel,text,username="Raspi_Bot"):
        sc.api_call("chat.postMessage",channel=channel,text=text,username="Raspi_Bot")

    #to get Temperature of RasPi
    def get_piTemperature(self):
        pi_temperature = subprocess.check_output(['/opt/vc/bin/vcgencmd', 'measure_temp']) 
        pi_temperature = re.sub(r'[\n\r]+', '', pi_temperature.decode("utf-8"))
        return pi_temperature
    
    #get internet connectivity status
    def get_connectivityStatus(self):
        try:
            http = urllib3.PoolManager()
            req = http.request('GET','http://www.google.com') #hit google
            return req.status
        except:
            return False
        
    #get internet conection details
    def get_connectionDetails(self):
        try:
            connection_ssid = subprocess.check_output(['iwgetid', '-r'])
            connection_ssid = re.sub(r'[\n\r]+', '', connection_ssid.decode("utf-8"))
            return connection_ssid
        except Exception as e:
            return str(e)


# In[4]:

#initialize raspi functions class
raspi = RasPi()

#wait until internet connection is established
while raspi.get_connectivityStatus() == False:
    time.sleep(10)

slack_token = raspi.get_auth_token("./slack_token.ini")
sc = SlackClient(slack_token)

#test message
raspi.send_slackMessage(channel = "#general", text = "General Info Text  \nSent from : "+platform.node() + "\nSent at : " + str(datetime.now()) )

raspi.send_slackMessage(channel = "#general", text = raspi.get_piTemperature())

