import json
from deck import Deck, Card


# def hello(event, context):
    # body = {
        # "message": "Go Serverless v1.0! Your function executed successfully!",
        # "input": event
    # }

    # response = {
        # "statusCode": 200,
        # "body": json.dumps(body)
    # }

    # return response


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
