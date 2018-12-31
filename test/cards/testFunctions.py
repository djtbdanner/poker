from player import Player

def buildPlayers(count):
    players = []
    for indx in range (0, count):
        players.append(Player("player " + str(indx)))
    return players



if __name__ == '__main__':
    print(buildPlayers(100))