### This os environ here is to fix a bug on boto3
import os
os.environ["TZ"] = "UTC"  

import boto3

def createPokerTable(dynamodb):
    table = dynamodb.create_table(
        TableName='PokerTable',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  #Partition key
            }
            
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
      
    print("Table status:", table.table_status)
    
def createPokerPlayer(dynamodb):
    table = dynamodb.create_table(
        TableName='PokerPlayer',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  #Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
      
    print("Table status:", table.table_status)

    
def deleteATable(dynamodb, name):
    try:
        print ('Deleting table "'+name+'"...')
        table = dynamodb.Table(name)
        table.delete()
        print ('Table "'+name+'" successfully deleted. ')
    except ddbClient.exceptions.ResourceNotFoundException:
        print ('Table "'+name+'" does not exist ')
        pass
     
   
dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
ddbClient = boto3.client('dynamodb', endpoint_url='http://localhost:8000')
response = ddbClient.list_tables()
print(response)
deleteATable(dynamodb, 'PokerPlayer')
deleteATable(dynamodb, 'PokerTable')
deleteATable(dynamodb, 'test')

createPokerTable(dynamodb)
createPokerPlayer(dynamodb)
response = ddbClient.list_tables()
print(response)


playerTable = dynamodb.Table("PokerPlayer")
response = playerTable.scan()
print ("\nCounting all records (using table scan)")
print ("Real Item Count:" + str(response['Count']))

playerTable.put_item(
   Item={
        'id': 'bfr-549',
        'player': {
                'plot':"Nothing happens at all.",
                'rating': 'asd'
         }
    }
)
print("PutItem succeeded:")
playerTable.put_item(
   Item={
        'id': 'bfr-548',
        'player': 'bp'
        }
)
print("PutItem succeeded:")
playerTable.put_item(
   Item={
        'id': 'bfr-547',
        'player': 'bp'
        }
)
print("PutItem succeeded:")



response = playerTable.scan()
print ("\nCounting all records (using table scan)")
print ("Real Item Count:" + str(response['Count']))

response = playerTable.get_item(        
    Key={
        'id': 'bfr-549'
        }
)

print(response)
