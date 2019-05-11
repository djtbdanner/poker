import evaluation.processor as processor
import db.datalayer as datalayer
import logging
from player import PlayerAction
from datetime import datetime
from datetime import timedelta
logger = logging.getLogger()


def makePlay(player, table, playerAction, actionAmount, currentStatus):
    try:
        if playerAction.lower() == "fold":
            logger.info("Player  will fold.")
            table.playerFold(player)
        else:
            actionAmount = int(actionAmount)
            currentTableBet = table.currentBet
            playerCurrentBet = player.currentBet
            logger.info("Making play ")
            if ((actionAmount + playerCurrentBet) < currentTableBet):
                logger.warn("Player must call or bet more than current table bet.")
                raise ValueError("Player must call or bet more than current table bet.")
            if actionAmount > 0:
                logger.info("Player will call or bet")
                table.playerBetOrCall(player, actionAmount)
            else:
                logger.info("Player will check")
                table.playerCheck(player)
                
        if not table.haveAllButOnePlayerFolded():        
            logger.info("checking to see if round is complete (not everyone has folded)")   
            if (table.isRoundComplete()):
                logger.info("round is complete, now processing")
                if len(table.cards) == 0:
                    table.dealToTable(3)
                    table.prepareForNextRound()
                elif len(table.cards) < 5:
                    table.dealToTable(1)
                    table.prepareForNextRound()
                else:
                    processWinners(table)
        else:
            logger.info("Every one has folded, processing winners")   
            processWinners(table)
#                          
        datalayer.updateTable(table)
        logger.info("make Play - table updated and returning.")
        return table
    except Exception as error:
        logger.exception("Failure making play for player.", error)

def processWinners(table):
    winnerList = processor.getWinners(table)
    winTotal = table.pot / len(winnerList)
    for player in winnerList:
        player.chips = player.chips + winTotal
    table.winners = winnerList

def checkForAndRemoveMissingPlayers(table):
    
    for player in table.players:
        if player.turn:
            startTime = datetime.strptime(player.turnStartTime, table.TIME_FORMAT)
            timeLimit = startTime + timedelta(seconds=table.PLAYER_TURN_LIMIT)
            logger.info("checking player " + player.name + " start time " + str(startTime) + " time limit " + str(timeLimit))
            now = datetime.now()
            if now > timeLimit:
                logger.info("player removed from table after timeout")
                table.removePlayer(player)
            else:
                logger.info("player kept")

def checkForUpdates(table, player, currentStatus):
    
    checkForAndRemoveMissingPlayers(table)
    
    if len(table.players) == 1:
        logger.info("only one player at table")
        for player in table.players:
            player.currentBet = 0
            player.currentAction = PlayerAction.NONE
            player.hand.cards = []
            player.folded = False
            player.dealer = False
            player.isInformedHandComplete = False
            if table.pot > 0:
                player.chips + table.pot
                table.pot = 0
                table.currentBet = 0
            table.winners = []
            table.cards =[]
    
    if len(table.players) > 1:
        if not table.hasDealer():
            table.setDealerAtRandom()
        while not table.doAllPlayersHaveTwoCards():
            table.dealRound()
            
        logger.info("check to see if hand is complete") 
        if table.isHandComplete():
          
            if table.allPlayersKnowHandIsComplete():
                table.prepareForNextHand()
                while not table.doAllPlayersHaveTwoCards():
                    table.dealRound()
            logger.info("hand is complete, now adding player to list that knows it is complete")
            player.isInformedHandComplete = True

    datalayer.updateTable(table)
    return table
