import pandas as pd
import pyodbc 
import json
from socket import *

#init
print('    __  __________    __    ____  __\n   / / / / ____/ /   / /   / __ \/ /\n  / /_/ / __/ / /   / /   / / / / /\n / __  / /___/ /___/ /___/ /_/ /_/\n/_/ /_/_____/_____/_____/\____(_)\n')

print('Apa yang ingan anda lakukan hari ini? (masukkan angka)')
print('1. List Buku\n2. Pinjam Buku\n3. Ubah Profil')

#server
serverName='archlinux'
serverPort=12000
clientSocket=socket(AF_INET,SOCK_DGRAM)

#command
comm=int(input())
def switch(comm):
    if(comm==1):
        # sql="EXEC MASTERBUKU @COMMAND='SELECT'"
        sql='1'
        # df=pd.read_sql(sql,cnxn)
        # print(df)
        clientSocket.sendto(sql.encode(),(serverName,serverPort))
        message,serverAddress=clientSocket.recvfrom(2048)
        message=json.loads(message.decode())
        message=message.get("a")
        for m in message:
            print(m)
        print(message[0][1])
        clientSocket.close()
    # elif(comm==2):
        
switch(comm)

#connect to db
# server = 'localhost' 
# database = 'PerpuSQL' 
# username = 'SA' 
# password = 'Gabrielle909' 
# cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
# cursor = cnxn.cursor()