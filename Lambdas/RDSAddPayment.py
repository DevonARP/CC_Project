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
    ctype=event['queryStringParameters']['ctype']
    card=event['queryStringParameters']['card']
    date=event['queryStringParameters']['date']
    csv=event['queryStringParameters']['csv']
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM ProfileUsers INNER JOIN Payments ON Payments.UID=ProfileUsers.ID WHERE ProfileUsers.Email=%s AND Payments.Card=%s",(email,card))
    rows=cursor.fetchall() 
    if(rows):
        cursor.close()
        return{
            'statusCode': 200,
            "headers": {"Access-Control-Allow-Origin":"*"},
            'body': json.dumps({
                'data':'Card is already registered to your account.'
            })
            }
    else:
        cursor.execute("SELECT * FROM ProfileUsers WHERE ProfileUsers.Email=%s",(email))
        rows=cursor.fetchall() 
        print(rows[0])
        print(rows[0][2])
        query = "SELECT MAX(Payment_ID) FROM Payments"
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        if data[0] is None:
            id=1
            print(id)
            
            ins = "INSERT INTO Payments VALUES(%s, %s, %s, %s, %s, %s)"
            cursor.execute(ins, (ctype,rows[0][2],id,card,date,csv))
            connection.commit()
            cursor.close()
            return{
                    'statusCode': 200,
                    "headers": {"Access-Control-Allow-Origin":"*"},
                    'body': json.dumps({
                        'data':'Successfully added card!'
                    })
                }            
        
        else:
            data=data[0]
            id=data+1
            print(id)
            
            ins = "INSERT INTO Payments VALUES(%s, %s, %s, %s, %s, %s)"
            cursor.execute(ins, (ctype,rows[0][2],id,card,date,csv))
            connection.commit()
            cursor.close()
            return{
                    'statusCode': 200,
                    "headers": {"Access-Control-Allow-Origin":"*"},
                    'body': json.dumps({
                        'data':'Successfully added card!'
                    })
                }