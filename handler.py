import json
import sys
sys.path.append("cards/")
sys.path.append("db/")
sys.path.append("evaluation/")
from deck import Deck
from table import Table
from player import Player
import db.jsonobj as jsob



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


def getNextCard(event, context):
    deck = Deck()
    deck.shuffle()
    card = deck.deal()
    body = {
        "card": card.rank + " of " + card.suit
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response

def getATable(event, context):
    table = Table()
    table.players = buildPlayers(5)
    table.dealRound()
    table.dealRound()

    response = {
        "statusCode": 200,
        "body": json.dumps(table,default=jsob.convert_to_dict,indent=4, sort_keys=True)
    }
    return response


def buildPlayers(count):
    players = []
    for indx in range (1, count + 1):
        players.append(Player("player " + str(indx)))
    return players

