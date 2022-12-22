import pymysql
import json
import boto3

def lambda_handler(event,context):

    endpoint='project-db.cr5lq0ndldt3.us-east-1.rds.amazonaws.com'
    username='admin'
    password=''
    database_name='Project'

    connection=pymysql.connect(host=endpoint,user=username,
    password=password,db=database_name)
    
    fname=event['queryStringParameters']['fname']
    lname=event['queryStringParameters']['lname']
    email=event['queryStringParameters']['email']
    reward = 0
    contact=event['queryStringParameters']['contact']
    password=event['queryStringParameters']['password']
    cursor=connection.cursor()
    query = "SELECT * FROM ProfileUsers WHERE Email=%s"
    cursor.execute(query,(email))
    data = cursor.fetchone()
    print(data)
    if(data):
        cursor.close()
        return {
                'statusCode': 200,
                "headers": {"Access-Control-Allow-Origin":"*"},
                'body': json.dumps({
                    'data': 'Error: Email alrady in system.'
                })
            }
    else:
        query = "SELECT MAX(ID) FROM ProfileUsers"
        cursor.execute(query)
        data = cursor.fetchone()
        if data[0] is None:
            id=1
            ins = "INSERT INTO ProfileUsers VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(ins, (fname, lname, id, email, contact, reward, id, password))
            connection.commit()
            cursor.close()
            ses_client = boto3.client("ses", region_name="us-east-1")
            ses_response = ses_client.verify_email_identity(EmailAddress = email)
            return{
                    'statusCode': 200,
                    "headers": {"Access-Control-Allow-Origin":"*"},
                    'body': json.dumps({
                        'data': 'uploaded'
                    })
                }
        else:
            data = data[0]
            id=data+1
            ins = "INSERT INTO ProfileUsers VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(ins, (fname, lname, id, email, contact, reward, id, password))
            connection.commit()
            cursor.close()
            ses_client = boto3.client("ses", region_name="us-east-1")
            ses_response = ses_client.verify_email_identity(EmailAddress = email)
            return{
                    'statusCode': 200,
                    "headers": {"Access-Control-Allow-Origin":"*"},
                    'body': json.dumps({
                        'data': 'uploaded'
                    })
                }