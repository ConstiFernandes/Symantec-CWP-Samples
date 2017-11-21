#!/usr/bin/env python
#
# Copyright 2017 Symantec Corporation. All rights reserved.
#
#Script to automate deployment of Symantec Cloud Workload Protection Agent on a Virtual Machine. This script can be used in AWS user data field during instance launch
#Refer to CWP REST API at: https://apidocs.symantec.com/home/scwp#_symantec_cloud_workload_protection
#######################################################################################################################################################################

import platform
import os
import requests
import string
import json
import time

#Function to call CWP REST API and download Agent package
def download_agentpkg_from_scwp_server(choiceofpkg):
  token = {}
  mydict = {}

  #CWP REST API endpoint URL for auth function
  url = 'https://scwp.securitycloud.symantec.com/dcs-service/dcscloud/v1/oauth/tokens'
  
  #TODO: Make sure you save your own CWP API keys here
  clientsecret='t6r4m————————srjhc5q'
  clientID='O2ID—————————————i0qsrc3k4p69'
  customerID='SEJ——————8STA8YCxAg'
  domainID='Dqdf—————IITB2w'

  #Add to payload and header your CWP tenant & API keys - client_id, client_secret, x-epmp-customer-id and x-epmp-domain-id
  payload = {'client_id' : clientID, 'client_secret' : clientsecret}
  header = {"Content-type": "application/json" ,'x-epmp-customer-id' : customerID , 'x-epmp-domain-id' : domainID}
  response = requests.post(url, data=json.dumps(payload), headers=header)
  authresult=response.status_code
  token=response.json()
  if (authresult!=200) :
    print "\nAuthentication Failed. Did you replace the API keys in the code with your CWP API Keys? Check clientsecret, clientID, customerID, and domainID\n"
    exit()

  #Extracting auth token
  accesstoken= token['access_token']
  accesstoken = "Bearer " + accesstoken

  #Output agent platform package type passed as a parameter for debugging
  mychoiceofpkg = choiceofpkg
  print "\nDownloading Agent package :-> " +  choiceofpkg + "  to current directory \n"

  #CWP REST API endpoint URL download package function
  urldonwnload = 'https://scwp.securitycloud.symantec.com/dcs-service/dcscloud/v1/agents/packages/download/platform/'
  urldonwnload = urldonwnload + choiceofpkg
  #print urldonwnload

  #Add to payload and header your CWP tenant & API keys - client_id, client_secret, x-epmp-customer-id and x-epmp-domain-id
  headerdownload = {"Authorization": accesstoken ,'x-epmp-customer-id' : customerID , 'x-epmp-domain-id' : domainID}
  response = requests.get(urldonwnload, headers=headerdownload)
  
  #On Windows save file as a .zip and as a .tar.gz on linux
  if (choiceofpkg =='windows') :
      nameofpkg='scwp_agent_' + choiceofpkg + '_package.zip'
  else :
      nameofpkg='scwp_agent_' + choiceofpkg + '_package.tar.gz'
  with open(nameofpkg, "wb") as code:
     #Save downloaded package to local file
     code.write(response.content)
     result=response.status_code
  if (result==200) :
     #Agent download API was successfull
     mydict=response.headers
     filename = mydict['content-disposition']
     #Check if file was doenloaded successfully
     if filename.find(nameofpkg) :
        print "\nAgent package :-> " +  nameofpkg + " downloaded successfully to current directory \n"
  else :
     print "\nDownload agent API failed. Specify correct platform name.\n"
     exit()

if __name__=="__main__":
   #First dump Instance metadata to use as reference
   os.system('curl -s http://169.254.169.254/latest/dynamic/instance-identity/document')
   #Determine OS platform name that is needed as input to CWP download agent REST API function

   #print Current working director for referenxe
   curentdir = os.getcwd()
   print "\nCurrent Working Path = " + os.getcwd()

   #some sample code to detect type of OS platform. CWP API needs platform to be specified in the REST endpoint URL
   osversion = 'undefined'
   osversion = platform.platform()
   print osversion
   choiceofpkg = 'undefined'

   if '.amzn1.' in osversion:
     choiceofpkg = 'amazonlinux'
   elif '-redhat-7' in osversion:
     choiceofpkg = 'rhel7'
   elif '-redhat-6' in osversion:
     choiceofpkg = 'rhel6'
   elif '-centos-7' in osversion:
     choiceofpkg = 'centos7'
   elif '-centos-6' in osversion:
     choiceofpkg = 'centos6'
   elif 'Ubuntu-16' in osversion:
    choiceofpkg = 'ubuntu16'
   elif 'Ubuntu-14' in osversion:
    choiceofpkg = 'ubuntu14'
   elif 'windows' in osversion:
     choiceofpkg = 'windows'

   #You may add additional checks to make sure the agent is installed on supported Kernel versions
   #if osversion in ['Linux-4.9.51-10.52.amzn1.x86_64-x86_64-with-glibc2.2.5', 'Linux-4.9.51-10.52.amzn1.x86_64-x86_64-with-glibc2.2.5']:
   #  choiceofpkg = 'amazonlinux'
   #else:
   #  exit()

   #Make sure the selected Platform is one of the supported list
   print choiceofpkg
   oslist = ['centos6', 'centos7', 'rhel6', 'rhel7', 'ubuntu14', 'ubuntu16', 'amazonlinux', 'windows']
   if choiceofpkg not in  oslist:
    print "\n Invalid OS Platform\n"
    exit()

   download_agentpkg_from_scwp_server(choiceofpkg)

   #Install for Windows. You can add custom code to expand .zip file and run installagent.bat
   if choiceofpkg == 'windows':
    exit()

   #Install for Linux Platforms
   else:
     pkgtocopy="scwp_agent_" + choiceofpkg + "_package.tar.gz"
     package_local = pkgtocopy
     tarcommand = "tar -xvzf " + package_local
     os.system(tarcommand)
     os.system('chmod 700 ./installagent.sh')
     os.system('./installagent.sh')
     os.system('reboot')
