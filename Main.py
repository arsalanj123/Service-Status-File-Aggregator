import os
from shutil import copyfile
import mmap
import time
import datetime
from tzlocal import get_localzone
import pytz

Directory="/mnt/Logs/"
File_Format=".log"
loopfile = ""
DateTime_Now = datetime.datetime.now()
Local_Timezone = pytz.timezone('Asia/Dubai')
Date_Today = (str(DateTime_Now.year)+"-"+str(DateTime_Now.month)+"-"+str(DateTime_Now.day))
Max_Gap = 583400

ServiceStatus_File=Directory+"ServiceStatus_File"

Host_IP='127.0.0.1'
Host_Name = ''
Service_Name = ''
File_Name = ''
Status = ''
Generation_Date = ''
Daily_or_Weekly = ''

#Set variable ip as primary interface IP address
Host_IP = netifaces.ifaddresses(IP_Interface)[netifaces.AF_INET][0]['addr']

for file in os.listdir(Directory):
    if file.endswith(File_Format):
        if file.startswith('Weekly'):
            readfile = os.path.join(Directory, file)
            Creation_Time_numbers = os.path.getctime(readfile)
            Creation_Time = datetime.datetime.utcfromtimestamp(Creation_Time_numbers).strftime('%Y-%m-%d').replace("-0", "-")
            Creation_Time_Detail = datetime.datetime.fromtimestamp(Creation_Time_numbers)
            Gap = (DateTime_Now-Creation_Time_Detail).total_seconds()

            if Gap <= Max_Gap:
                with open(readfile, 'rb', 0) as file, \
                    mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as readfile2:
                        if readfile2.find(b'Synchronization Completed Successfully') != -1:
                            Status = 'Success'
                            Status_File_Handle = open(ServiceStatus_File,"a+")
                            Status_File_Handle.write(Host_Name+","+Host_IP+","+Service_Name+","+File_Name+","+Status+","+Generation_Date+","+Daily_or_Weekly+","+"\n")
                            Status_File_Handle.close()
                            print (str(Status)+" - "+readfile+" - Weekly File - "+str(Creation_Time))
                        elif readfile2.find(b'Synchronization Completed Failed') != -1:
                            status = 'Failed'
                            Status_File_Handle = open(ServiceStatus_File,"a+")
                            Status_File_Handle.write(Host_Name+","+Host_IP+","+Service_Name+","+File_Name+","+Status+","+Generation_Date+","+Daily_or_Weekly+","+"\n")
                            Status_File_Handle.close()
                            print (str(Status)+" - "+readfile+" - Weekly File - "+str(Creation_Time))
                        else:
                            Status_File_Handle = open(ServiceStatus_File,"a+")
                            Status_File_Handle.write(Host_Name+","+Host_IP+","+Service_Name+","+File_Name+","+Status+","+Generation_Date+","+Daily_or_Weekly+","+"\n")
                            Status_File_Handle.close()
                            print ("Status not mentioned"+" - "+readfile+" - Weekly File - "+str(Creation_Time))
            elif Gap > Max_Gap:
                Status_File_Handle = open(ServiceStatus_File,"a+")
                Status_File_Handle.write(Host_Name+","+Host_IP+","+Service_Name+","+File_Name+","+Status+","+Generation_Date+","+Daily_or_Weekly+","+"\n")
                Status_File_Handle.close()
                print("Weekly File - "+readfile+" - not generated - Last file was generated on: "+Creation_Time)
        else:
            readfile = os.path.join(Directory, file)
            Creation_Time_numbers = os.path.getctime(readfile)
            Creation_Time = datetime.datetime.utcfromtimestamp(Creation_Time_numbers).strftime('%Y-%m-%d').replace("-0", "-")
            if Date_Today == Creation_Time:
                with open(readfile, 'rb', 0) as file, \
                    mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as readfile2:
                        if readfile2.find(b'Synchronization Completed Successfully') != -1:
                            Status = 'Success'
                            Status_File_Handle = open(ServiceStatus_File,"a+")
                            Status_File_Handle.write(Host_Name+","+Host_IP+","+Service_Name+","+File_Name+","+Status+","+Generation_Date+","+Daily_or_Weekly+","+"\n")
                            Status_File_Handle.close()
                            print (str(Status)+" - "+readfile+ " - " + str(Creation_Time))
                        elif readfile2.find(b'Synchronization Completed Failed') != -1:
                            status = 'Failed'
                            Status_File_Handle = open(ServiceStatus_File,"a+")
                            Status_File_Handle.write(Host_Name+","+Host_IP+","+Service_Name+","+File_Name+","+Status+","+Generation_Date+","+Daily_or_Weekly+","+"\n")
                            Status_File_Handle.close()
                            print (str(Status)+" - "+readfile+ " - " + str(Creation_Time))
                        else:
                            Status_File_Handle = open(ServiceStatus_File,"a+")
                            Status_File_Handle.write(Host_Name+","+Host_IP+","+Service_Name+","+File_Name+","+Status+","+Generation_Date+","+Daily_or_Weekly+","+"\n")
                            Status_File_Handle.close()
                            print ("Status not mentioned - "+readfile+" - " + str(Creation_Time))
            elif Date_Today != Creation_Time:
                print("File -"+readfile+" - not generated - Last file was generated on: "+Creation_Time)
