### This os environ here is to fix a bug on boto3
import os
os.environ["TZ"] = "UTC"  
import boto3
import logging
from player import Player
from table import Table
import json
import db.jsonobj as jsob

playerTableName="PokerPlayer"
tableTableName="PokerTable"

dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
ddbClient = boto3.client('dynamodb', endpoint_url='http://localhost:8000')

playerTable = dynamodb.Table(playerTableName)
pokerTable = dynamodb.Table(tableTableName)


def getOrCreateSavedPlayer(playerId, playerName="Poker Player"):
    try:
        logging.debug("Attempting to retrieve player :" + str(playerId))
        response = playerTable.get_item(Key={'playerId':playerId})
        if 'Item' in response:
            playerJSON = response['Item']['player']
            logging.info("From Database: " + playerJSON)
            player = json.loads(playerJSON, object_hook=jsob.dict_to_obj)              
        else:
            player = Player(playerName)
            logging.debug("Created Player :" + str(player) + " and saving to database!")
            jsondata = json.dumps(player,default=jsob.convert_to_dict,indent=None, sort_keys=False)
            logging.info("Player JSON: " + jsondata)
            playerTable.put_item(
                Item={
                     'playerId': player.playerId,
                     'player': jsondata
                 }
            )             
        return player
    except Exception as error:
        logging.exception("Unable to process player." + str(error))
        

def updatePlayer(player):
    try:
        logging.debug("Attempting to update player :" + str(player.playerId))
        jsondata = json.dumps(player,default=jsob.convert_to_dict,indent=None, sort_keys=False)
        playerTable.put_item(
                Item={
                     'playerId': player.playerId,
                     'player': jsondata
                 }
            )  
        return player
    except Exception as error:
        logging.exception("Unable to update player." + str(error))
        
        
def deletePlayer(player):
    try:
        logging.debug("Attempting to delete player :" + str(player.playerId))
        playerTable.delete_item(
            Key={
                'playerId': player.playerId
                }
        )
        logging.debug("Player deleted.")
    except Exception as error:
        logging.exception("Unable to delete player." + str(error))
        
        
def getOrCreateSavedTable(tableId):
    try:
        logging.debug("Attempting to retrieve table :" + str(tableId))
        response = pokerTable.get_item(Key={'pokerTableId':tableId})
        if 'Item' in response:
            tableJSON = response['Item']['pokerTable']
            logging.info("From Database: " + tableJSON)
            table = json.loads(tableJSON, object_hook=jsob.dict_to_obj)              
        else:
            table = Table()
            logging.debug("Created Poker Table :" + str(table) + " and saving to database!")
            jsondata = json.dumps(table,default=jsob.convert_to_dict,indent=None, sort_keys=False)
            logging.info("Table JSON: " + jsondata)
            pokerTable.put_item(
                Item={
                     'pokerTableId': table.tableId,
                     'pokerTable': jsondata
                 }
            )             
        return table
    except Exception as error:
        logging.exception("Unable to process table." + str(error))
        

def updateTable(table):
    try:
        logging.debug("Attempting to update table :" + str(table.tableId))
        jsondata = json.dumps(table,default=jsob.convert_to_dict,indent=None, sort_keys=False)
        pokerTable.put_item(
                Item={
                     'pokerTableId': table.tableId,
                     'pokerTable': jsondata
                 }
            )  
        return table
    except Exception as error:
        logging.exception("Unable to update table." + str(error))
        
        
def deleteTable(table):
    try:
        logging.debug("Attempting to delete table :" + str(table.tableId))
        pokerTable.delete_item(
            Key={
                'pokerTableId': table.tableId
                }
        )
        logging.debug("Table deleted.")
    except Exception as error:
        logging.exception("Unable to delete Table." + str(error))


