import pymysql
import json

def lambda_handler(event,context):

    endpoint='project-db.cr5lq0ndldt3.us-east-1.rds.amazonaws.com'
    username='admin'
    password=''
    database_name='Project'

    connection=pymysql.connect(host=endpoint,user=username,
    password=password,db=database_name)
    
    pick=event['queryStringParameters']['pick']
    drop=event['queryStringParameters']['drop']
    cursor=connection.cursor()
    print(pick)
    print(drop)
    print(format(drop))
    ins = "SELECT `" + drop + "` from Price where PLID=%s"
    print(ins)
    cursor.execute(ins,(pick))
    rows=cursor.fetchone()
    cursor.close()
    print(rows)
    transactionresponse={}
    transactionresponse['message']='Got the Price'
    transactionresponse['data']=rows
    
    
    
    responseObject={}
    responseObject['statusObject']=200
    responseObject['headers']={}
    responseObject['headers']['Content-Type']='application/json'
    responseObject['body']=json.dumps(transactionresponse)
    print(responseObject)
    
    # for row in rows:
    #     print(row)
    return{
            'statusCode': 200,
            "headers": {"Access-Control-Allow-Origin":"*"},
            'body': json.dumps({
                'data':transactionresponse
            })
        }