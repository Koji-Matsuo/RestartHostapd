#If wifi conection is disconected,
#this profram conect wifi used by restarting hostapd.
#If you want to use this service,
#please open the linux terminal and write this comand "sudo python RestartHostapd.py".

import os
import time
import datetime

#Max line number of logfile .
maxRow = 2880

#Writes the contents specified in the argument to 'RestartHostapdLog'.
def writeLog(log):
    os.system('echo \'' + log + '\' | sudo tee -a ./log/RestartHostapdLog\n')
#This method make backup log and remove the original log.  
def makeBackupLog(originalLog,afterlog):
    os.system('cp ./log/'+originalLog+' ./log/'+afterlog)
    os.system('rm ./log/'+originalLog)    

#It keeps running unless you stop the process.    
while True:
    
    #Assigns an initial value to a variable 
    dt_now = datetime.datetime.now()
    rowNum = sum([1 for _ in open('./log/RestartHostapdLog')])
    syslog = open('/var/log/syslog','r')    
    datalist = syslog.readlines()
    sucsess = str(datalist[0])[4:15].replace(':','').replace(' ','')
    fail = str(datalist[0])[4:15].replace(':','').replace(' ','')
    
    #Write start time to log.
    writeLog('['+str(dt_now)+'] Confirming the wifi conection --->')
    #If line number of log file over max line numver, it makes back up log and removing original log.
    if rowNum >= maxRow:
        makeBackupLog('RestartHostapdLog','RestartHostapdLog_'+str(dt_now.strftime('%Y.%m.%dT%H:%M:%S')))        
    
    #Searching place of stoping hostapd.service and assigns its problem value.
    for data in datalist:
        if 'hostapd.service: Succeeded' in data :
            sucsess = str(data)[4:15].replace(':','').replace(' ','')
        if 'hostapd' in data  and 'disassociated' in data:
            fail = str(data)[4:15].replace(':','').replace(' ','')
    syslog.close()
    
    #If wifi conection is disconected, restart hostapd service.
    if int(sucsess) < int(fail) :
        os.system('./restartHostapd.sh')
        writeLog('['+str(dt_now)+'] The hostapd is restarted by this program.')
    else :
        writeLog('['+str(dt_now)+'] Conection is right.')
    # Wait 60 seconds.
    time.sleep(60)
    