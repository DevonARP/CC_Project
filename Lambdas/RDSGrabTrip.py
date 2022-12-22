import pymysql
from datetime import datetime
import json

def lambda_handler(event,context):

    endpoint='project-db.cr5lq0ndldt3.us-east-1.rds.amazonaws.com'
    username='admin'
    password=''
    database_name='Project'

    connection=pymysql.connect(host=endpoint,user=username,
    password=password,db=database_name)
    
    start=event['queryStringParameters']['start']
    end=event['queryStringParameters']['end']
    date=event['queryStringParameters']['date']
    cursor=connection.cursor()
    cursor.execute("SELECT * from Booking INNER JOIN BUS ON Booking.BID=BUS.BID where Start_Location = %s AND End_Location = %s AND Leave_Time >= %s",(start,end,date))
    rows=cursor.fetchall()
    cursor.close()
    print(rows)
    rows=list(rows)
    counter=0
    for i in rows:
        rows[counter]=list(rows[counter])
        print(rows[counter])
        print(rows[counter][4])
        rows[counter][4]=str(i[4])
        counter=counter+1
    transactionresponse={}
    transactionresponse['data']=rows
    print(transactionresponse)
    
    
    
    responseObject={}
    responseObject['statusObject']=200
    responseObject['headers']={}
    responseObject['headers']['Content-Type']='application/json'
    responseObject['body']=json.dumps(transactionresponse)
    print(responseObject)
    
    return{
            'statusCode': 200,
            "headers": {"Access-Control-Allow-Origin":"*"},
            'body': json.dumps({
                'data':transactionresponse
            })
        }