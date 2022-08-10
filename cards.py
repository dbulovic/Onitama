def getCardMoves(name):
    if name == "tiger":
        return [[-2,0],[1,0]]
    elif name == "dragon":
        return [[-1,-2],[-1,2],[1,-1],[1,1]]
    elif name == "crab":
        return [[-1,0],[0,-2],[0,2]]
    elif name == "elephant":
        return [[-1,1],[-1,-1],[0,1],[0,-1]]
    elif name == "monkey":
        return [[-1,-1],[-1,1],[1,-1],[1,1]]
