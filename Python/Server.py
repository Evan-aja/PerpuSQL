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

def rotate(arr):
    rt=1
    for i in range(0, rt):    
        first = arr[0]
        for j in range(len(arr)-1):
            arr[j] = arr[j+1]  
        arr[len(arr)-1] = first
    return arr

while True:
    message, clientAddress=serverSocket.recvfrom(16384)
    message=json.loads(message.decode())
    result=pd.read_sql('SELECT 1',cnxn).values
    if(message.get("a")=='1'):
        result=pd.read_sql("EXEC MASTERBUKU @COMMAND='SELECT'",cnxn).values
        
        # result=pd.read_sql("SELECT * FROM BUKU ORDER BY ID_BUKU ASC",cnxn).values
    elif(message.get("a")=='2'):
        arr=message.get("b")
        sql="EXEC MASTERPINJAM @ID_MAHASISWA=?,@ID_BUKU=?,@COMMAND='ADD'"
        
        # sql="INSERT INTO PINJAM(ID_MAHASISWA,ID_BUKU,TANGGAL_PINJAM,TANGGAL_KEMBALI) VALUES(?,?,GETDATE(),DATEADD(DAY,+8,DATEADD(MILLISECOND,-3,DATEADD(DAY,0, DATEDIFF(DAY,0,getdate())))))"
        
        cursor.execute(sql,arr)
        cnxn.commit()
        result=pd.read_sql("EXEC MASTERPINJAM @COMMAND='SELECT'",cnxn)

        # result=pd.read_sql('''SELECT TOP(10) ID_PINJAM,JUDUL,NAMA_DEPAN,TANGGAL_PINJAM,TANGGAL_KEMBALI FROM PINJAM P 
        #                       LEFT JOIN MAHASISWA M ON P.ID_MAHASISWA=M.ID_MAHASISWA 
        #                       LEFT JOIN BUKU B ON P.ID_BUKU=B.ID_BUKU
        #                       ORDER BY ID_PINJAM DESC''',cnxn)
        result['ID_PINJAM']=result['ID_PINJAM'].astype(str)
        result['TANGGAL_PINJAM']=result['TANGGAL_PINJAM'].astype(str)
        result['TANGGAL_KEMBALI']=result['TANGGAL_KEMBALI'].astype(str)
        result=result.values
    elif(message.get("a")=='3'):
        arr=message.get("b")
        print(arr)
        sql="EXEC MASTERSISWA @ID_MAHASISWA=?,@NAMA_DEPAN=?,@NAMA_BELAKANG=?,@JENIS_KELAMIN=?,@COMMAND='UPDATE'"
        
        # sql="UPDATE MAHASISWA SET NAMA_DEPAN=?,NAMA_BELAKANG=?,JENIS_KELAMIN=? WHERE ID_MAHASISWA=?"
        # arr=rotate(arr)

        cursor.execute(sql,arr)
        cnxn.commit()
        result=pd.read_sql("EXEC MASTERSISWA @COMMAND='SELECT'",cnxn).values
        
        # result=pd.read_sql("SELECT * FROM MAHASISWA ORDER BY ID_MAHASISWA ASC",cnxn).values
    elif(message.get("a")=='4'):
        result=pd.read_sql("EXEC MASTERSISWA @COMMAND='SELECT'",cnxn).values
        
        # result=pd.read_sql("SELECT * FROM MAHASISWA ORDER BY ID_MAHASISWA ASC",cnxn).values
    print(result)
    returns=json.dumps({"a":result.tolist()})
    serverSocket.sendto(returns.encode(),(clientAddress))