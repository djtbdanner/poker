import evaluation.processor as processor
import db.datalayer as datalayer
import logging
logger = logging.getLogger()


def makePlay(player, table, playerAction, actionAmount, currentStatus):
    try:
        if playerAction.lower() == "fold":
            logger.info("Player {0} will fold.".format(player.name))
            table.playerFold(player)
        else:
            actionAmount = int(actionAmount)
            currentTableBet = table.currentBet
            playerCurrentBet = player.currentBet
            logger.info("Making play of actionAmount {0}, currentTableBet {1}, playerCurrentBet{2} for player {3}".format(actionAmount, currentTableBet, playerCurrentBet, player))
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

        logger.info("check to see if hand is complete") 
        if table.isHandComplete():
            logger.info("hand is complete, now processing")
            table.prepareForNextHand()
            while not table.doAllPlayersHaveTwoCards():
                table.dealRound()
                         
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


def checkForUpdates(table, player, currentStatus):
    if len(table.players) > 2:
        if not table.hasDealer():
            table.setDealerAtRandom()
        while not table.doAllPlayersHaveTwoCards():
            table.dealRound()
    datalayer.updateTable(table)
    return table
