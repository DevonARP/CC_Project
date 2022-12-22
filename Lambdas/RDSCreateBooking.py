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
    card=event['queryStringParameters']['card']
    price=event['queryStringParameters']['price']
    id=event['queryStringParameters']['id']
    cursor=connection.cursor()
    query = "SELECT * FROM BookingTransactions WHERE Buyer=%s AND Booking=%s"
    cursor.execute(query,(email,id))
    data = cursor.fetchone()
    print(data)
    if(data):
        cursor.close()
        return {
                'statusCode': 200,
                "headers": {"Access-Control-Allow-Origin":"*"},
                'body': json.dumps({
                    'data': 'Error: Already registered for this trip.'
                })
            }
    else:
        query = "SELECT MAX(BTransactionID) FROM BookingTransactions"
        cursor.execute(query)
        data = cursor.fetchone()
        print(data)
        print(type(data))
        print(len(data))
        if data[0] is None:
            bookid=1
            ins = "INSERT INTO BookingTransactions VALUES(%s, %s, %s, %s, %s)"
            cursor.execute(ins, (bookid, email, id, card, price))
            connection.commit()
            ins = "UPDATE ProfileUsers SET Reward = Reward + 10 WHERE email = %s"
            cursor.execute(ins, (email))
            connection.commit()
            cursor.close()
            try:
                ses_client = boto3.client("ses", region_name="us-east-1")
                ses_client.send_email(Source = 'sk9428@nyu.edu', Destination = {'ToAddresses': [email]}, 
                                    Message = {'Subject': {'Data': 'Bus Booking'}, 
                                                'Body' : { 'Text' : { 'Data' : 'Booked for trip: ' + id}}})
                return{
                        'statusCode': 200,
                        "headers": {"Access-Control-Allow-Origin":"*"},
                        'body': json.dumps({
                            'data': 'uploaded'
                        })}
            except:
                return{
                        'statusCode': 200,
                        "headers": {"Access-Control-Allow-Origin":"*"},
                        'body': json.dumps({
                            'data': 'Booked but please verify email.'
                        })}
        else:
            data = data[0]
            print(data)
            bookid=data+1
            ins = "INSERT INTO BookingTransactions VALUES(%s, %s, %s, %s, %s)"
            cursor.execute(ins, (bookid, email, id, card, price))
            connection.commit()
            ins = "UPDATE ProfileUsers SET Reward = Reward + 10 WHERE email = %s"
            cursor.execute(ins, (email))
            connection.commit()
            cursor.close()
            try:
                ses_client = boto3.client("ses", region_name="us-east-1")
                ses_client.send_email(Source = 'sk9428@nyu.edu', Destination = {'ToAddresses': [email]}, 
                                    Message = {'Subject': {'Data': 'Bus Booking'}, 
                                                'Body' : { 'Text' : { 'Data' : 'Booked for trip: ' + id}}})
                return{
                        'statusCode': 200,
                        "headers": {"Access-Control-Allow-Origin":"*"},
                        'body': json.dumps({
                            'data': 'uploaded'
                        })}
            except:
                return{
                        'statusCode': 200,
                        "headers": {"Access-Control-Allow-Origin":"*"},
                        'body': json.dumps({
                            'data': 'Booked but please verify email.'
                        })}