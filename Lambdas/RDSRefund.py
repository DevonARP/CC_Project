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

    email=event['queryStringParameters']['email']
    id=event['queryStringParameters']['id']
    cursor=connection.cursor()
    query = "DELETE FROM BookingTransactions WHERE Buyer=%s AND BTransactionID=%s"
    cursor.execute(query,(email,id))
    connection.commit()
    ins = "UPDATE ProfileUsers SET Reward = Reward - 10 WHERE email = %s"
    cursor.execute(ins, (email))
    connection.commit()
    cursor.close()
    try:
        ses_client = boto3.client("ses", region_name="us-east-1")
        ses_client.send_email(Source = 'sk9428@nyu.edu', Destination = {'ToAddresses': [email]}, 
                            Message = {'Subject': {'Data': 'Bus Booking'}, 
                                        'Body' : { 'Text' : { 'Data' : 'Refunded for trip: ' + id}}})
        return {
                'statusCode': 200,
                "headers": {"Access-Control-Allow-Origin":"*"},
                'body': json.dumps({
                    'data': 'deleted'
                })
            }
    except:
        return {
                'statusCode': 200,
                "headers": {"Access-Control-Allow-Origin":"*"},
                'body': json.dumps({
                    'data': 'Deleted but please verify email.'
                })
            }
        