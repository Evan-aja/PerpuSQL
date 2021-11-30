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
        sql='1'
        send=json.dumps({"a":sql})
        clientSocket.sendto(send.encode(),(serverName,serverPort))
        message,serverAddress=clientSocket.recvfrom(2048)
        message=json.loads(message.decode())
        message=message.get("a")
        for m in message:
            print(m)
        return message
        clientSocket.close()
    elif(comm==2):
        sql='2'
        siswa=int(input('masukkan id anda :\t'))
        pilih=switch(1)
        buku=int(input('buku mana yang anda pilih? :\t'))
        arr=[]
        for p in range(len(pilih)):
            if(pilih[p][0]==buku):
                arr.append(pilih[p][0])
                arr.append(pilih[p][1])
                arr.append(pilih[p][2])
                arr.append(pilih[p][3])
        if(len(arr)>1):
            print(arr)


        
switch(comm)

#connect to db
# server = 'localhost' 
# database = 'PerpuSQL' 
# username = 'SA' 
# password = 'Gabrielle909' 
# cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
# cursor = cnxn.cursor()