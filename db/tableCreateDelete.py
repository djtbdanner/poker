### This os environ here is to fix a bug on boto3
import os
os.environ["TZ"] = "UTC"  
import boto3
import logging
import platform

if (platform.system() == "Windows"):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")
    ddbClient = boto3.client('dynamodb', endpoint_url='http://localhost:8000')
else:
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    ddbClient = boto3.client('dynamodb')

def createATable(tableName, tableId):
    logging.debug("Attempting to create table: " + tableName)
    try:
        dynamodb.create_table(
            TableName=tableName,
            KeySchema=[
                {
                    'AttributeName': tableId,
                    'KeyType': 'HASH'  #Partition key
                }
                
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': tableId,
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        logging.info('Table "'+tableName+'" successfully created. ')
    except ddbClient.exceptions.ResourceInUseException:
        logging.warn ('Table "'+tableName+'" need not be created as it already exist ')
        pass
    
def deleteATable(name):
    try:
        logging.debug('Deleting table "'+name+'"...')
        table = dynamodb.Table(name)
        table.delete()
        logging.info('Table "'+name+'" successfully deleted. ')
    except ddbClient.exceptions.ResourceNotFoundException:
        logging.warn ('Table "'+name+'" does not exist ')
        pass
    
createATable("PokerPlayer", 'playerId')
createATable("PokerTable", 'pokerTableId')
