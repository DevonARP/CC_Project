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
    first=event['queryStringParameters']['first']
    last=event['queryStringParameters']['last']
    email2=event['queryStringParameters']['email2']
    contact=event['queryStringParameters']['contact']
    password=event['queryStringParameters']['password']
    cursor=connection.cursor()
    if(email2):
        cursor.execute("SELECT * FROM ProfileUsers WHERE Email=%s",(email2))
        rows=cursor.fetchall()
        if(rows):
            cursor.close()
            return{
                    'statusCode': 200,
                    "headers": {"Access-Control-Allow-Origin":"*"},
                    'body': json.dumps({
                        'data':'The Email you wanted to change to is in use by another account and we cannot change your information becasue of it.'
                    })
                }
    if(first):
        cursor.execute("UPDATE ProfileUsers SET fName=%s WHERE Email=%s",(first,email))
        connection.commit()
    if(last):
        cursor.execute("UPDATE ProfileUsers SET lName=%s WHERE Email=%s",(last,email))
        connection.commit()
    if(contact):
        cursor.execute("UPDATE ProfileUsers SET Contact=%s WHERE Email=%s",(contact,email))
        connection.commit()
    if(password):
        cursor.execute("UPDATE ProfileUsers SET Password=%s WHERE Email=%s",(password,email))
        connection.commit()
    if(email2):
        cursor.execute("UPDATE ProfileUsers SET Email=%s WHERE Email=%s",(email2,email))
        connection.commit()
        cursor.execute("UPDATE BookingTransactions SET Buyer=%s WHERE Buyer=%s",(email2,email))
        connection.commit()

    cursor.close()
    return{
            'statusCode': 200,
            "headers": {"Access-Control-Allow-Origin":"*"},
            'body': json.dumps({
                'data':'Successfully updated your information! We reccomend signing out and back in.'
            })
        }