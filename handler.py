import json
import sys
sys.path.append("cards/")
sys.path.append("db/")
sys.path.append("evaluation/")
import db.jsonobj as jsob
import db.datalayer as datalayer
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def hello(event, context):
    
    logger.debug("Hello called " + str(event) + " " + str(context))
    body = {
         "message": "Go Serverless v1.0! Your function executed successfully!",
         "input": event
     }

    return createResponse(200, body)


def createOrFindPlayer(event, context):
    logger.debug("createOrFindPlayer called " + str(event) + " " + str(context))
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
    logger.debug("findTable called " + str(event))
    try:
        logger.debug("Hey Dude, gonna try anbd get the id : " )
        playerId = event['playerId']
        logger.debug("PlayerID : " + str(playerId))
        player = datalayer.getOrCreateSavedPlayer(playerId)
        logger.debug("Looking for table for player: " + str(player))
        player = datalayer.getOrCreateSavedPlayer(playerId)
        table = datalayer.findATableForPlayer(player)
        status = 200
        table.deck.cards = []
        body = json.dumps(table,default=jsob.convert_to_dict,indent=4, sort_keys=True)

    except Exception as error:
        logger.exception("Unable to find or create player." + str(error))
        status = 500
        body = str(error)

    return createResponse(status, body)

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
