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
        results=pd.read_sql("EXEC MASTERBUKU @COMMAND='SELECT'",cnxn)
        result=results.values
    print(result)
    returns=json.dumps({"a":result.tolist()})
    serverSocket.sendto(returns.encode(),(clientAddress))