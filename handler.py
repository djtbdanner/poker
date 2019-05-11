import json
import sys
sys.path.append("cards/")
sys.path.append("db/")
sys.path.append("evaluation/")
import evaluation.playProcessor as playProcessor
import db.jsonobj as jsob
import db.datalayer as datalayer
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def createOrFindPlayer(event, context):
    logger.info("createOrFindPlayer called " + str(event) + " " + str(context))
    try:
        playerId = event['playerId']
        playerName = event['name']
        logger.debug("Looking for player: " + playerId + " , "+ playerName)
        player = datalayer.getOrCreateSavedPlayer(playerId, playerName)
        status = 200
        body = json.dumps(player,default=jsob.convert_to_dict,indent=4, sort_keys=True)
 
    except Exception as error:
        logger.exception("Unable to find or create player." + str(error))
        status = 500
        body = str(error)
 
    return createResponse(status, body)

def findTable(event, context):
    logger.info("findTable called " + str(event))
    try:
        playerId = event['playerId']
        logger.debug("PlayerID : " + str(playerId))
        ## TODO? put to default 
        datalayer.resetUnusedTables(100)
        player = datalayer.getOrCreateSavedPlayer(playerId)
        table = datalayer.findATableForPlayer(player)
        status = 200
        table.deck.cards = []
        body = json.dumps(table,default=jsob.convert_to_dict,indent=4, sort_keys=True)

    except Exception as error:
        logger.exception("Unable to find or create table." + str(error))
        status = 500
        body = str(error)

    return createResponse(status, body)

def makePlay(event, context):
    logger.info("makePlay called " + str(event))
    try:
        playerId = event['playerId']
        playerAction = event['playerAction']
        tableId = event['tableId']
        tableStatusId = event['tableStatusId']
        actionAmount = event['actionAmount']
        table =  datalayer.getOrCreateSavedTable(tableId)
        logger.info("retrieved table: " + table.tableId)
        player = table.findPlayerById(playerId)
        logger.info("retrieved player from table: " + player.playerId)
        if table.statusId != int(tableStatusId):
            status = 500
            body = {"message": "Play is out of turn."}
            raise  ValueError ("Play is out of turn.")
        else:
            table = playProcessor.makePlay(player, table, playerAction, actionAmount, tableStatusId)
            status = 200
            body = buildTableResult(table)

    except Exception as error:
        logger.exception("Unable to make play." + str(error))
        status = 500
        body = str(error)

    return createResponse(status, body)

def checkForUpdates(event, context):
    logger.info("checkForUpdates called " + str(event))
    try:
        tableId = event['tableId']
        tableStatusId = event['tableStatusId']
        playerId = event['playerId']
        logger.info("tableID: {0}, tableStatusId: {1}, playerId{2}".format(tableId, tableStatusId, playerId))
        table =  datalayer.getOrCreateSavedTable(tableId)
        logger.info("retrieved table: " + table.tableId)
        player = table.findPlayerById(playerId)
        if player is None:
            logger.info("Player not on table raising error... " )
            raise Exception("Player not found at table.")
        else:
            logger.info("retrieved player from table: " + player.playerId)
        table = playProcessor.checkForUpdates(table, player, tableStatusId)
        status = 200
        body = buildTableResult(table)
    except Exception as error:
        logger.exception("Unable to check for updates." + str(error))
        status = 500
        body = str(error)

    return createResponse(status, body)

def removePlayer(event, context):
    logger.info("removePlayer called " + str(event))
    try:
        tableId = event['tableId']
        playerId = event['playerId']
        logger.info("tableID: {0}, playerId{1}".format(tableId, playerId))
        table =  datalayer.getOrCreateSavedTable(tableId)
        logger.info("retrieved table: " + table.tableId)
        player = table.findPlayerById(playerId)
        logger.info("retrieved player from table: " + player.playerId)
        table.removePlayer(player)
        datalayer.deletePlayer(player)
        datalayer.updateTable(table)
        status = 200
        body = buildTableResult(table)
    except Exception as error:
        logger.exception("Unable to remove player." + str(error))
        status = 500
        body = str(error)

    return createResponse(status, body)

def buildTableResult(table):
    table.deck.cards = []
    body = json.dumps(table,default=jsob.convert_to_dict,indent=0, sort_keys=False)
    return body


def createResponse(status, body):
    response = {
        "statusCode": status,
        "body": body,
        "headers": {
               'Access-Control-Allow-Origin': '*'
        }
    }
    return response     
    
    
       
# def getNextCard(event, context):
#     deck = Deck()
#     deck.shuffle()
#     card = deck.deal()
#     body = {
#         "card": card.rank + " of " + card.suit
#     }
#     response = {
#         "statusCode": 200,
#         "body": json.dumps(body)
#     }
#     return response
# 
# def getATable(event, context):
#     table = Table()
#     table.players = buildPlayers(5)
#     table.dealRound()
#     table.dealRound()
# 
#     response = {
#         "statusCode": 200,
#         "body": json.dumps(table,default=jsob.convert_to_dict,indent=4, sort_keys=True)
#     }
#     return response
# 
# 
# def createTableTest(event, context):
#     try:
#         logger.debug("Attempting to create a table")
# #         tableCreateDelete.createATable('test', 'pokerTableId')
# #         tableCreateDelete.createATable('PokerPlayer', 'playerId')
# #         tableCreateDelete.createATable('PokerTable', 'pokerTableId')
#         table = Table()
#         table.players = buildPlayers(5)
#         table.dealRound()
#         table.dealRound()
#         datalayer.updateTable(table)
#         
#         tableII = datalayer.getOrCreateSavedTable(table.tableId)
#         
#         
#     except Exception as error:
#         logger.exception("Unable to process table." + str(error))
# 
#     response = {
#         "statusCode": 200,
#         "body": json.dumps(tableII,default=jsob.convert_to_dict,indent=4, sort_keys=True)
#     }
#     return response
# 
# 
# def buildPlayers(count):
#     players = []
#     for indx in range (1, count + 1):
#         players.append(Player("player " + str(indx)))
#     return players
