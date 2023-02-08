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
    elif name == "mantis":
        return [[1,0],[-1,1],[-1,-1]]
    elif name == "ox":
        return [[-1,0],[0,1],[1,0]]
    elif name == "phoenix":
        return [[0,-2],[0,2],[-1,-1],[-1,1]]
    elif name == "rabbit":
        return [[1,-1],[-1,1],[0,2]]
    elif name == "rooster":
        return [[0,-1],[0,1],[-1,1],[1,-1]]
    elif name == "boar":
        return [[-1,0],[0,1],[0,-1]]
    elif name == "cobra":
        return [[0,-1],[1,1],[-1,1]]
    elif name == "crane":
        return [[-1,0],[1,1],[1,-1]]
    elif name == "eel":
        return [[-1,-1],[1,-1],[0,1]]
    elif name == "frog":
        return [[0,-2],[-1,-1],[1,1]]
    elif name == "goose":
        return [[0,-1],[0,1],[-1,-1],[1,1]]
    elif name == "horse":
        return [[0,-1],[1,0],[-1,0]]
    elif name == "kirin":
        return [[-2,-1],[-2,1],[2,0]]

    else: print("[ERROR] ", name, " is not a Card!" )
