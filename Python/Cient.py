import sys
import pandas as pd
import pyodbc 
import json
from socket import *

def recvv(socket):
    data = b''
    while True:
        part=socket.recv(2048)
        data+=part
        if len(part)<2048:
            break
    return data
def gender(choice):
    switch = {
        1:'Laki-Laki',
        2:'Perempuan',
        3:'NonBiner'
    }
    return switch.get(choice,'no')
def genderchooser():
    tmp=str
    while True:
        choice=int(input('\nPilih Gender anda :\n1. Laki-laki\n2. Perempuan\n3. NonBiner\n'))
        tmp=gender(choice)
        if tmp=='no':
            print('Pilih 1-3')
            continue
        else:
            break
    return tmp

#init
print('    __  __________    __    ____  __\n   / / / / ____/ /   / /   / __ \/ /\n  / /_/ / __/ / /   / /   / / / / /\n / __  / /___/ /___/ /___/ /_/ /_/\n/_/ /_/_____/_____/_____/\____(_)\n')


#server
serverName='archlinux'
serverPort=12000

#command
while True:
    print('\nApa yang ingan anda lakukan hari ini? (masukkan angka)')
    print('1. List Buku\n2. Pinjam Buku\n3. Ubah Profil\n4. Keluar')
    comm=int(input())
    def switch(comm):
        if(comm==1):
            clientSocket=socket(AF_INET,SOCK_DGRAM)
            sql='1'
            send=json.dumps({"a":sql})
            clientSocket.sendto(send.encode(),(serverName,serverPort))
            message=recvv(clientSocket)
            message=json.loads(message.decode())
            message=message.get("a")
            print('\n%3s%20s%15s%20s'%('ID','Judul','Genre','Penulis'))
            for m in range(len(message)):
                print('%3d%20s%15s%20s'%(message[m][0],message[m][1],message[m][2],message[m][3]))
            clientSocket.close()
            return message
        elif(comm==2):
            clientSocket=socket(AF_INET,SOCK_DGRAM)
            sql='4'
            send=json.dumps({"a":sql})
            clientSocket.sendto(send.encode(),(serverName,serverPort))
            message=recvv(clientSocket)
            message=json.loads(message.decode())
            message=message.get("a")
            clientSocket.close()
            clientSocket=socket(AF_INET,SOCK_DGRAM)
            sql='2'
            siswa=int(input('masukkan id anda : '))
            pilih=switch(1)
            buku=int(input('buku mana yang anda pilih? : '))
            arr=[]
            if(siswa<=len(message)):
                arr.append(siswa)
            for p in range(len(pilih)):
                if(pilih[p][0]==buku):
                    arr.append(pilih[p][0])
            if(len(arr)<2):
                return
            send=json.dumps({"a":sql,"b":arr})
            clientSocket.sendto(send.encode(),(serverName,serverPort))
            message=recvv(clientSocket)
            message=json.loads(message.decode())
            print('\n%s%20s%15s%30s%30s'%('ID','Judul','Peminjam','Tanggal Pinjam','Tanggal Kembali'))
            me=message.get("a")
            print('%s%20s%15s%30s%30s'%(me[0][0],me[0][1],me[0][2],me[0][3],me[0][4]))
            clientSocket.close()
        elif(comm==3):
            clientSocket=socket(AF_INET,SOCK_DGRAM)
            sql='4'
            send=json.dumps({"a":sql})
            clientSocket.sendto(send.encode(),(serverName,serverPort))
            message=recvv(clientSocket)
            message=json.loads(message.decode())
            message=message.get("a")
            print('\n%3s%15s%15s%10s'%('ID','Firstname','Lastname','Gender'))
            for m in range(len(message)):
                print('%3d%15s%15s%10s'%(message[m][0],message[m][1],message[m][2],message[m][3]))
            clientSocket.close()
            
            clientSocket=socket(AF_INET,SOCK_DGRAM)
            while True:
                siswa=int(input('Silahkan masukkan ID anda : '))
                arr=[]
                for i in range(len(message)):
                    if(message[i][0]==siswa):
                        arr.append(message[i][0])
                        arr.append(message[i][1])
                        arr.append(message[i][2])
                        arr.append(message[i][3])
                if(len(arr)<1):
                    print('ID anda salah, mohon memilih kembali')
                    continue
                elif (len(arr)>0):
                    benarkah=False
                    while True:
                        print('\n%3s%15s%15s%10s'%('ID','Firstname','Lastname','Gender'))
                        print('%3d%15s%15s%10s'%(arr[0],arr[1],arr[2],arr[3]))
                        benar=input('Apakah data ini benar? (yes/no, default=no)').lower()
                        yes={'yes','y','ya'}
                        no={'no','n','tidak',''}
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
            while True:
                print('\nApa yang ingin anda ubah?\n\n%3s%15s%15s%10s\n%3d%15s%15s%10s'%('ID','Firstname','Lastname','Gender',arr[0],arr[1],arr[2],arr[3]))
                print('1. Nama Depan\n2. Nama Belakang\n3. Jenis Kelamin\n4. Selesai')
                ubah=int(input())
                if(ubah==1):
                    print('Nama Depan : ',arr[1])
                    arr[1]=input('Masukkan Nama depan baru : ')
                elif(ubah==2):
                    print('Nama Depan : ',arr[2])
                    arr[2]=input('Masukkan Nama belakang baru : ')
                elif(ubah==3):
                    print("Jenis Kelamin : ",arr[3])
                    arr[3]=genderchooser()
                elif(ubah==4):
                    benarkah=False
                    while True:
                        print('\n%3s%15s%15s%10s'%('ID','Firstname','Lastname','Gender'))
                        print('%3d%15s%15s%10s'%(arr[0],arr[1],arr[2],arr[3]))
                        benar=input('Apakah data ini benar? (yes/no, default=no)').lower()
                        yes={'yes','y','ya'}
                        no={'no','n','tidak',''}
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
            sql='3'
            send=json.dumps({"a":sql,"b":arr})
            clientSocket.sendto(send.encode(),(serverName,serverPort))
            message=recvv(clientSocket)
            message=json.loads(message.decode())
            message=message.get("a")
            print('\n%3s%20s%15s%20s'%('ID','Judul','Genre','Penulis'))
            for m in range(len(message)):
                print('%3d%20s%15s%20s'%(message[m][0],message[m][1],message[m][2],message[m][3]))
            clientSocket.close()
        elif(comm==4):
            print('Terima Kasih')
    switch(comm)
    if(comm==4):
        break