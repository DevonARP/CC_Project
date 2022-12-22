import pymysql
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
    query = "SELECT * FROM ProfileUsers INNER JOIN Payments on ProfileUsers.ID = Payments.UID WHERE ProfileUsers.Email=%s"
    cursor.execute(query,(email))
    data = cursor.fetchall()
    cursor.close()
    print(data)
    if(data):
        rows=list(data)
        counter=0
        for i in rows:
            rows[counter]=list(rows[counter])
            print(rows[counter])
            print(rows[counter][12])
            rows[counter][12]=str(i[12])
            counter=counter+1
        return{
                'statusCode': 200,
                "headers": {"Access-Control-Allow-Origin":"*"},
                'body': json.dumps({
                    'data': rows
                })
            }
    else:
        return {
                'statusCode': 200,
                "headers": {"Access-Control-Allow-Origin":"*"},
                'body': json.dumps({
                    'data': 'Error: No payment.'
                })
            }