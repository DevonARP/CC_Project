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
    card=event['queryStringParameters']['card']
    cursor=connection.cursor()
    
    cursor.execute("SELECT * FROM ProfileUsers WHERE ProfileUsers.Email=%s",(email))
    rows=cursor.fetchall() 
    print(rows[0])
    print(rows[0][2])
        
    query = "DELETE FROM Payments WHERE UID=%s AND Card=%s"
    cursor.execute(query,(rows[0][2],card))
    connection.commit()
    cursor.close()
    return {
            'statusCode': 200,
            "headers": {"Access-Control-Allow-Origin":"*"},
            'body': json.dumps({
                'data': 'Deleted successfully!'
            })
        }