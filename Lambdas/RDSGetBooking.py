
import pymysql
import json

def lambda_handler(event,context):

    endpoint='project-db.cr5lq0ndldt3.us-east-1.rds.amazonaws.com'
    username='admin'
    password=''
    database_name='Project'

    connection=pymysql.connect(host=endpoint,user=username,
    password=password,db=database_name)
    
    id=event['queryStringParameters']['id']
    cursor=connection.cursor()
    cursor.execute("SELECT * from Booking INNER JOIN BUS ON Booking.BID=BUS.BID where BookingID=%s",(id))
    rows=cursor.fetchone()
    cursor.close()
    transactionresponse={}
    transactionresponse['data']=rows
    rows=list(rows)
    print(rows)
    print(rows[4])
    rows[4]=str(rows[4])
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