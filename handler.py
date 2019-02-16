import json
import sys
sys.path.append("cards/")
sys.path.append("db/")
sys.path.append("evaluation/")
import db.jsonobj as jsob
import db.datalayer as datalayer
import logging

def hello(event, context):
    body = {
         "message": "Go Serverless v1.0! Your function executed successfully!",
         "input": event
     }

    response = {
         "statusCode": 200,
         "body": json.dumps(body)
     }

    return response


def createOrFindPlayer(event, context):
    try:
        playerId = event['playerId']
        playerName = event['name']
        logging.debug("Looking for player: " + playerId + " , "+ playerName)
        player = datalayer.getOrCreateSavedPlayer(playerId, playerName)
        status = 200
        body = json.dumps(player,default=jsob.convert_to_dict,indent=4, sort_keys=True)

    except Exception as error:
        logging.exception("Unable to find or create player." + str(error))
        status = 500
        body = str(error)
 
    response = {
        "statusCode": status,
        "body": body
    }
    return response

def findTable(event, context):
    try:
        playerId = event['playerId']
        playerName = event['name']
        player = datalayer.getOrCreateSavedPlayer(playerId)
        logging.debug("Looking for table for player: " + str(player))
        
        
        player = datalayer.getOrCreateSavedPlayer(playerId, playerName)
        table = datalayer.findATableForPlayer(player)
        status = 200
        body = json.dumps(table,default=jsob.convert_to_dict,indent=4, sort_keys=True)

    except Exception as error:
        logging.exception("Unable to find or create player." + str(error))
        status = 500
        body = str(error)
 
    response = {
        "statusCode": status,
        "body": body
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
#         logging.debug("Attempting to create a table")
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
#         logging.exception("Unable to process table." + str(error))
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
