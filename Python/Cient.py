import sys
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
# clientSocket=socket(AF_INET,SOCK_DGRAM)

#command
while True:
    comm=int(input())
    def switch(comm):
        if(comm==1):
            clientSocket=socket(AF_INET,SOCK_DGRAM)
            sql='1'
            send=json.dumps({"a":sql})
            clientSocket.sendto(send.encode(),(serverName,serverPort))
            message,serverAddress=clientSocket.recvfrom(2048)
            message=json.loads(message.decode())
            message=message.get("a")
            for m in message:
                print(m)
            clientSocket.close()
            return message
        elif(comm==2):
            clientSocket=socket(AF_INET,SOCK_DGRAM)
            sql='2'
            siswa=int(input('masukkan id anda :\t'))
            pilih=switch(1)
            buku=int(input('buku mana yang anda pilih? :\t'))
            arr=[]
            arr.append(siswa)
            for p in range(len(pilih)):
                if(pilih[p][0]==buku):
                    arr.append(pilih[p][0])
            if(len(arr)<2):
                return
            # print(arr)
            send=json.dumps({"a":sql,"b":arr})
            clientSocket.sendto(send.encode(),(serverName,serverPort))
            message,serverAddress=clientSocket.recvfrom(2048)
            message=json.loads(message.decode())
            # print(message)
            le=int(len(message.get("a")))
            print(message.get("a")[le-1])
            clientSocket.close()
        elif(comm==3):
            clientSocket=socket(AF_INET,SOCK_DGRAM)
            sql='4'
            send=json.dumps({"a":sql})
            clientSocket.sendto(send.encode(),(serverName,serverPort))
            message,serverAddress=clientSocket.recvfrom(2048)
            message=json.loads(message.decode())
            message=message.get("a")
            for m in message:
                print(m)
            clientSocket.close()
            
            clientSocket=socket(AF_INET,SOCK_DGRAM)
            while True:
                siswa=int(input('Silahkan masukkan ID anda'))
                arr=[]
                for i in range(len(message)):
                    if(message[i][0]==siswa):
                        arr.append(message[i])
                if(len(arr)<1):
                    print('ID anda salah, mohon memilih kembali')
                    continue
                elif (len(arr)>0):
                    benarkah=False
                    while True:
                        print(arr)
                        benar=input('Apakah data ini benar? (yes/no, default=no)').lower()
                        yes={'yes','y'}
                        no={'no','n',''}
                        if benar in yes:
                            benarkah=True
                            break
                        elif benar in no:
                            benarkah=False
                            break
                        else :
                            sys.stdout.write("Mohon repon dengan 'Yes' atau 'No'")
                            continue
                    if(benarkah==True):
                        break
                    else:
                        continue
            print(arr)

            clientSocket.close()
            


    switch(comm)

#connect to db
# server = 'localhost' 
# database = 'PerpuSQL' 
# username = 'SA' 
# password = 'Gabrielle909' 
# cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
# cursor = cnxn.cursor()