import pymysql

def lambda_handler(event,context):

    endpoint='project-db.cr5lq0ndldt3.us-east-1.rds.amazonaws.com'
    username='admin'
    password=''
    database_name='Project'

    connection=pymysql.connect(host=endpoint,user=username,
    password=password,db=database_name)
    
    cursor=connection.cursor()
    cursor.execute('SELECT * from ProfileUsers')
    rows=cursor.fetchall()
    cursor.close()

    for row in rows:
        print(row)