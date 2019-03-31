### This os environ here is to fix a bug on boto3
import os
from boto3.dynamodb.conditions import Attr
os.environ["TZ"] = "UTC"  
import boto3
import logging
from player import Player
from table import Table
import json
import db.jsonobj as jsob
import platform
from datetime import datetime
from datetime import timedelta
logger = logging.getLogger()

playerTableName="PokerPlayer"
tableTableName="PokerTable"

if (platform.system() == "Windows"):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")
    ddbClient = boto3.client('dynamodb', endpoint_url='http://localhost:8000')
else:
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    ddbClient = boto3.client('dynamodb')

playerTable = dynamodb.Table(playerTableName)
pokerTable = dynamodb.Table(tableTableName)


def getOrCreateSavedPlayer(playerId, playerName="Poker Player"):
    try:
        logger.debug("Attempting to retrieve player")
        response = playerTable.get_item(Key={'playerId':playerId})
        if 'Item' in response:
            playerJSON = response['Item']['player']
            logger.info("From Database: " + playerJSON)
            player = json.loads(playerJSON, object_hook=jsob.dict_to_obj)              
        else:
            player = Player(playerName)
            logger.debug("Created Player :" + str(player) + " and saving to database!")
            jsondata = json.dumps(player,default=jsob.convert_to_dict,indent=None, sort_keys=False)
            logger.info("Player JSON: " + jsondata)
            playerTable.put_item(
                Item={
                     'playerId': player.playerId,
                     'player': jsondata
                 }
            )             
        return player
    except Exception as error:
        logger.exception("Unable to process player." + str(error))
        

def updatePlayer(player):
    try:
        logger.debug("Attempting to update player ")
        jsondata = json.dumps(player,default=jsob.convert_to_dict,indent=None, sort_keys=False)
        playerTable.put_item(
                Item={
                     'playerId': player.playerId,
                     'player': jsondata
                 }
            )  
        return player
    except Exception as error:
        logger.exception("Unable to update player." + str(error))
        
        
def deletePlayer(player):
    try:
        logger.debug("Attempting to delete player.")
        playerTable.delete_item(
            Key={
                'playerId': player.playerId
                }
        )
        logger.debug("Player deleted.")
    except Exception:
        logger.exception("Unable to delete player.")
        
        
def getOrCreateSavedTable(tableId):
    try:
        logger.debug("Attempting to retrieve table :")
        response = pokerTable.get_item(Key={'pokerTableId':tableId})
        if 'Item' in response:
            tableJSON = response['Item']['pokerTable']
            logger.info("From Database: " + tableJSON)
            table = json.loads(tableJSON, object_hook=jsob.dict_to_obj)              
        else:
            table = Table()
            logger.debug("Created Poker Table and saving to database!")
            jsondata = json.dumps(table,default=jsob.convert_to_dict,indent=None, sort_keys=False)
            logger.info("Table JSON: " + jsondata)
            pokerTable.put_item(
                Item={
                     'pokerTableId': table.tableId,
                     'pokerTable': jsondata
                 }
            )             
        return table
    except Exception:
        logger.exception("Unable to process table.")
        

def updateTable(table):
    try:
        logger.info("Attempting to update table :" + str(table.tableId))
        table.updateTs = datetime.now().strftime(table.TIME_FORMAT)
        jsondata = json.dumps(table,default=jsob.convert_to_dict,indent=None, sort_keys=False)
        pokerTable.put_item(
                Item={
                     'pokerTableId': table.tableId,
                     'pokerTable': jsondata
                 }
            )  
        return table
    except Exception as error:
        logger.exception("Unable to update table." + str(error))
        
        
def deleteTable(table):
    try:
        logger.info("Attempting to delete table :" + str(table.tableId))
        pokerTable.delete_item(
            Key={
                'pokerTableId': table.tableId
                }
        )
        logger.info("Table deleted.")
    except Exception as error:
        logger.exception("Unable to delete Table." + str(error))

def resetUnusedTables(secondsToLiveWithNoAction=60):
    logger.info("Checking for tables that should be cleared....")
    response = pokerTable.scan()
    if 'Items' in response and len(response["Items"]) > 0:
        for i in response['Items']:
            table = json.loads(i["pokerTable"], object_hook=jsob.dict_to_obj)
            logger.info("Found a table to clear :" + str(table))
            if table.updateTs is not None and len(table.players) > 1:
                startTime = datetime.strptime(table.updateTs, table.TIME_FORMAT)
                timeLimit = startTime + timedelta(seconds=secondsToLiveWithNoAction)
                now = datetime.now()
                if now > timeLimit:
                    logger.info("Table has not seen action for 60 seconds, resetting table...")
                    table.resetTable()
                    updateTable(table)
                
                
def findATableForPlayer(player):
    try:
        #TODO - see if there is a more elegant way to search tables
        logger.debug("finding a table for player.")
        fe = Attr('pokerTable').exists()
        pe = "pokerTable"
        response = pokerTable.scan(
           FilterExpression=fe,
           ProjectionExpression=pe
        )
        
        foundATable = False
        if 'Items' in response and len(response["Items"]) > 0:
            for i in response['Items']:
                tableTry = json.loads(i["pokerTable"], object_hook=jsob.dict_to_obj)
                logger.info("Found a table for player :" + str(tableTry))
                if (len(tableTry.players) < 7):
                    logger.info("Table has less than 7 players :" + str(tableTry))
                    table = tableTry
                    foundATable = True
                    break
                
        if not foundATable:
            table = getOrCreateSavedTable('x')
            logger.info("Couldn't find a table, created one :" + str(table))

        table.addPlayer(player)
        updateTable(table)
        return table
    except Exception as error:
        logger.exception("Unable to find table." + str(error))
        raise
        
