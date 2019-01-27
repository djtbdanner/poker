### This os environ here is to fix a bug on boto3
import os
os.environ["TZ"] = "UTC"  

import boto3

def createATable():
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
      
      
    table = dynamodb.create_table(
        TableName='PokerPlayer',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'player',
                'KeyType': 'RANGE'  #Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'player',
                'AttributeType': 'S'
            },
      
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
      
    print("Table status:", table.table_status)

    
def deleteATable():
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
    table = dynamodb.Table('Movies')
    table.delete()
     
   
 
ddb = boto3.client('dynamodb', endpoint_url='http://localhost:8000')
response = ddb.list_tables()
print(response)
# deleteATable()
createATable()
response = ddb.list_tables()
print(response)
