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
    
    email=event['queryStringParameters']['email']
    cursor=connection.cursor()
    cursor.execute("SELECT * from ProfileUsers where Email = %s",(email))
    rows=cursor.fetchall()
    cursor.close()
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