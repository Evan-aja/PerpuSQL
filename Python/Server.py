from typing import ValuesView
from numpy import mod
import pandas as pd
import pyodbc 
import json
from socket import *

#connect to db
server = 'localhost' 
database = 'PerpuSQL' 
username = 'SA' 
password = 'Gabrielle909' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

serverPort=12000
serverSocket=socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(('',serverPort))

print('Ready to receive')

while True:
    message, clientAddress=serverSocket.recvfrom(2048)
    message=json.loads(message.decode())
    result=pd.read_sql('SELECT 1',cnxn).values
    if(message.get("a")=='1'):
        result=pd.read_sql("EXEC MASTERBUKU @COMMAND='SELECT'",cnxn).values
    elif(message.get("a")=='2'):
        arr=message.get("b")
        sql="EXEC MASTERPINJAM @ID_MAHASISWA=?,@ID_BUKU=?,@COMMAND='ADD'"
        cursor.execute(sql,arr)
        cnxn.commit()
        result=pd.read_sql("EXEC MASTERPINJAM @COMMAND='SELECT'",cnxn)
        result['TANGGAL_PINJAM']=result['TANGGAL_PINJAM'].astype(str)
        result['TANGGAL_KEMBALI']=result['TANGGAL_KEMBALI'].astype(str)
        result=result.values
    elif(message.get("a")=='3'):
        arr=message.get("b")
    elif(message.get("a")=='4'):
        result=pd.read_sql("EXEC MASTERSISWA @COMMAND='SELECT'",cnxn).values
    print(result)
    returns=json.dumps({"a":result.tolist()})
    serverSocket.sendto(returns.encode(),(clientAddress))