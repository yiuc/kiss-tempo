# kiss-tempo
Keep tempo simple and stupid  
This is a simple program to upload you timesheet to Jira Tempo

## 1. Installation
### install virtualenv
install pip - recommended tool for installing Python packages  
`sudo easy_install pip`  
install virtualenv -a tool to create isolated Python environments  
`sudo pip install virtualenv`  
create you virutal environments, go to the kiss folder
`cd ~Desktop/kiss-temp`  
`virtualenv env`  
install the require packages
`env/bin/pip install -r requirements.txt`

## 2. copy and modify the properties
copy the jira-properties to jira.ini  

## 3. execute the script  
`env/bin/python UploadToTempo.py timesheets.csv`
