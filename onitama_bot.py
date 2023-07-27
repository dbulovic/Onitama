# Onitama bot

from math import sqrt
import random
import cards
import copy
import pickle

class GameStateNode:
	def __init__(self, board, blue_cards, red_cards, common_card, value : int, move, turn_sign: int):
		self.children = []
		self.board = board
		self.blue_cards = blue_cards
		self.red_cards = red_cards
		self.common_card = common_card
		self.value = value
		self.move = move
		self.turn_sign = turn_sign 

class Move:
	def __init__(self, i, j, i_n, j_n, c):
		self.i = i
		self.j = j
		self.i_n = i_n
		self.j_n = j_n
		self.c = c

def getRandomTurn(node: GameStateNode):
	sign = node.turn_sign
	pcs_coors = []
	if sign == 1:
		for i in range(5):
			for j in range(5):
				if node.board[i][j] == "BP" or node.board[i][j] == "BK":
					pcs_coors.append([i,j])

	elif sign == -1:
		for i in range(5):
			for j in range(5):
				if node.board[i][j] == "RP" or node.board[i][j] == "RK":
					pcs_coors.append([i,j])
	
	while (True):
		if sign == -1:
			cards_tmp = node.red_cards
		elif sign == 1:
			cards_tmp = node.blue_cards
		r_piece = random.choice(pcs_coors)
		r_card = random.choice(cards_tmp)
		
		moves = cards.getCardMoves(r_card)

		for move in moves:
			i_new = r_piece[0] + (sign*move[0])
			j_new = r_piece[1] + (sign*move[1])
			if i_new < 0 or j_new < 0 or i_new > 4 or j_new > 4: continue
			elif (node.board[i_new][j_new] == "RK" or node.board[i_new][j_new] == "RP") and sign == -1: continue
			elif (node.board[i_new][j_new] == "BK" or node.board[i_new][j_new] == "BP") and sign == 1: continue
			else:
				return r_piece[0], r_piece[1], i_new, j_new, cards_tmp.index(r_card)
			
def getTurn(evaluation_function, depth, board, blue_cards, red_cards, common_card, now_sign):
	nboard = copy.deepcopy(board)
	nblue_cards = blue_cards[:]
	nred_cards = red_cards[:]
	ncc = common_card
	zeroMove = Move(0,0,0,0,0)
	root = GameStateNode(nboard, nblue_cards, nred_cards, ncc, 0, zeroMove, now_sign)
	maximizer = True if now_sign == -1 else False
	if evaluation_function == "Random":
		return getRandomTurn(root)
	else:
		alpha_beta_pruning(root, depth, -1000, +1000, maximizer, evaluation_function)		
	
	for child in root.children:
		if child.value == root.value:
			print(root.value)
			return (child.move).i, (child.move).j, (child.move).i_n, (child.move).j_n, (child.move).c


def addChildrenToNode(node : GameStateNode):
	if node.board[0][2] == "BK" or not any("RK" in subl for subl in node.board) or node.board[4][2] == "RK" or not any("BK" in subl for subl in node.board): return
	if node.turn_sign == 1:		
		for i in range(5):
			for j in range(5):
				if node.board[i][j] == "BP" or node.board[i][j] == "BK":
					#print(node.blue_cards)
					for card in node.blue_cards:
						moves = cards.getCardMoves(card)
						for move in moves:
							i_new = i + (node.turn_sign*move[0])
							j_new = j + (node.turn_sign*move[1])
							if i_new < 0 or j_new < 0 or i_new > 4 or j_new > 4: continue
							elif node.board[i_new][j_new] == "BK" or node.board[i_new][j_new] == "BP": continue
							else:
								new_board = copy.deepcopy(node.board)
								new_board[i_new][j_new] = node.board[i][j]
								new_board[i][j] = " "
								new_blue_cards = copy.deepcopy(node.blue_cards)
								new_red_cards = copy.deepcopy(node.red_cards)
								index_of_card = (node.blue_cards).index(card)
								new_blue_cards[index_of_card] = node.common_card
								new_common_card = card
								node_move = Move(i,j,i_new,j_new,index_of_card)
								nn_sign = -node.turn_sign
								new_node = GameStateNode(new_board, new_blue_cards, new_red_cards, new_common_card, 0, node_move, nn_sign)
								node.children.append(new_node)								
	
	elif node.turn_sign == -1:
		for i in range(5):
			for j in range(5):
				if node.board[i][j] == "RP" or node.board[i][j] == "RK":
					for card in node.red_cards:
						moves = cards.getCardMoves(card)
						for move in moves:
							i_new = i + (node.turn_sign*move[0])
							j_new = j + (node.turn_sign*move[1])
							if i_new < 0 or j_new < 0 or i_new > 4 or j_new > 4: continue
							elif node.board[i_new][j_new] == "RK" or node.board[i_new][j_new] == "RP": continue
							else:
								new_board = copy.deepcopy(node.board)
								new_board[i_new][j_new] = node.board[i][j]
								new_board[i][j] = " "
								new_blue_cards = copy.deepcopy(node.blue_cards)
								new_red_cards = copy.deepcopy(node.red_cards)
								index_of_card = (node.red_cards).index(card)
								new_red_cards[index_of_card] = node.common_card								
								new_common_card = card
								node_move = Move(i,j,i_new,j_new,index_of_card)
								nn_sign = -node.turn_sign
								new_node = GameStateNode(new_board, new_blue_cards, new_red_cards, new_common_card, 0, node_move, nn_sign)
								node.children.append(new_node)								

def alpha_beta_pruning(node : GameStateNode, depth, alpha, beta, maximizing, ev_func):
	addChildrenToNode(node)
	if depth == 0 or node.children == []:
		if ev_func == "CountPawns": node.value = evaluatePawns(node)
		elif ev_func == "CountMoves": node.value = evaluateMoves(node)
		elif ev_func == "ReachTemple": node.value = evaluateReach(node)
		elif ev_func == "Combination": node.value = evaluateCombination(node)
		return node.value 
	
	if maximizing:
		value = -10000
		for child in node.children:
			value = max(value, alpha_beta_pruning(child, depth-1, alpha, beta, False, ev_func))
			alpha = max(alpha, value)
			if value >= beta: break
		node.value = value
		return value 
	
	else:
		value = 10000
		for child in node.children:
			value = min(value, alpha_beta_pruning(child, depth-1, alpha, beta, True, ev_func))
			beta = min(beta, value)
			if value <= alpha: break
		node.value = value
		return value
	
def evaluatePawns(node : GameStateNode):
	if node.board[0][2] == "BK" or not any("RK" in subl for subl in node.board):
		return -10000
	
	if node.board[4][2] == "RK" or not any("BK" in subl for subl in node.board):
		return 10000

	score = 0
	for i in range(5):
			for j in range(5):
				if node.board[i][j] == "BP" or node.board[i][j] == "BK": 
					score -= 10
				elif node.board[i][j] == "RP" or node.board[i][j] == "RK": 
					score += 10
	return score

def evaluateMoves(node : GameStateNode):
	if node.board[0][2] == "BK" or not any("RK" in subl for subl in node.board):
		return -10000
	
	if node.board[4][2] == "RK" or not any("BK" in subl for subl in node.board):
		return 10000

	score = 0
	if node.turn_sign == 1:
		for i in range(5):
				for j in range(5):
					if node.board[i][j] == "BP" or node.board[i][j] == "BK":
						for card in node.blue_cards:
							moves = cards.getCardMoves(card)
							for move in moves:
								i_new = i + (node.turn_sign*move[0])
								j_new = j + (node.turn_sign*move[1])
								if i_new < 0 or j_new < 0 or i_new > 4 or j_new > 4: continue
								elif node.board[i_new][j_new] == "BK" or node.board[i_new][j_new] == "BP": continue
								else:
									score -= 10
								
	elif node.turn_sign == -1:
		for i in range(5):
				for j in range(5):
					if node.board[i][j] == "RP" or node.board[i][j] == "RK":
						for card in node.red_cards:
							moves = cards.getCardMoves(card)
							for move in moves:
								i_new = i + (node.turn_sign*move[0])
								j_new = j + (node.turn_sign*move[1])
								if i_new < 0 or j_new < 0 or i_new > 4 or j_new > 4: continue
								elif node.board[i_new][j_new] == "RK" or node.board[i_new][j_new] == "RP": continue
								else:
									score += 10	

	return score

def evaluateReach(node: GameStateNode):
	if node.board[0][2] == "BK" or not any("RK" in subl for subl in node.board):
		return -10000
	
	if node.board[4][2] == "RK" or not any("BK" in subl for subl in node.board):
		return 10000

	for i in range(5):
			for j in range(5):
				if node.board[i][j] == "RK":
					for card in node.red_cards:
						moves = cards.getCardMoves(card)
						for move in moves:
							i_new = i + (node.turn_sign*move[0])
							j_new = j + (node.turn_sign*move[1])
							if i_new < 0 or j_new < 0 or i_new > 4 or j_new > 4: continue
							elif node.board[i_new][j_new] == "RK" or node.board[i_new][j_new] == "RP": continue
							elif i_new == 4 and j_new == 2: return 50
					
					moves1 = cards.getCardMoves(node.red_cards[0])
					moves2 = cards.getCardMoves(node.red_cards[1])

					for move1 in moves1:
						for move2 in moves2:
							i_tot = i + node.turn_sign*move1[0] + node.turn_sign*move2[0]
							j_tot = j + node.turn_sign*move1[1] + node.turn_sign*move2[1]
							if i_tot < 0 or j_tot < 0 or i_tot > 4 or j_tot > 4: continue
							elif node.board[i_tot][j_tot] == "RK" or node.board[i_tot][j_tot] == "RP": continue
							elif i_tot == 4 and j_tot == 2: return 25

					extra_moves = cards.getCardMoves(node.common_card)	
					for move1 in moves1:
						for move2 in moves2:
							for emove in extra_moves:
								i_tot = i + node.turn_sign*move1[0] + node.turn_sign*move2[0] + node.turn_sign*emove[0]
								j_tot = j + node.turn_sign*move1[1] + node.turn_sign*move2[1] + node.turn_sign*emove[1]
								if i_tot < 0 or j_tot < 0 or i_tot > 4 or j_tot > 4: continue
								elif node.board[i_tot][j_tot] == "RK" or node.board[i_tot][j_tot] == "RP": continue
								elif i_tot == 4 and j_tot == 2: return 13
					break
			
	return 0

def evaluateCombination(node : GameStateNode):
	if node.board[0][2] == "BK" or not any("RK" in subl for subl in node.board):
		return -10000
	
	if node.board[4][2] == "RK" or not any("BK" in subl for subl in node.board):
		return 10000
	
	return evaluateMoves(node)/3 + evaluatePawns(node)/3 + evaluateReach(node)/3




# def evaluate3(node : GameStateNode):
# 	if node.board[0][2] == "BK" or not any("RK" in subl for subl in node.board):
# 		return -100
	
# 	if node.board[4][2] == "RK" or not any("BK" in subl for subl in node.board):
# 		return 100

# 	for i in range(5):
# 		for j in range(5):	
# 			if node.board[i][j] == "RK":
# 				score = -sqrt((4-i)**2 + (2-j)**2)

# 				return mapToEvalRange(score)

# def mapToEvalRange(value):
#     leftSpan = 4.472
#     rightSpan = 200

#     # Convert the left range into a 0-1 range (float)
#     valueScaled = float(value - (-4.472)) / float(leftSpan)

#     # Convert the 0-1 range into a value in the right range.
#     return -100 + (valueScaled * rightSpan)	


def buildCompleteTree(node, depth):
	if node.turn_sign == 1:		
		for i in range(5):
			for j in range(5):
				if node.board[i][j] == "BP" or node.board[i][j] == "BK":
					#print(node.blue_cards)
					for card in node.blue_cards:
						moves = cards.getCardMoves(card)
						for move in moves:
							i_new = i + (node.turn_sign*move[0])
							j_new = j + (node.turn_sign*move[1])
							if i_new < 0 or j_new < 0 or i_new > 4 or j_new > 4: continue
							elif node.board[i_new][j_new] == "BK" or node.board[i_new][j_new] == "BP": continue
							else:
								new_board = copy.deepcopy(node.board)
								new_board[i_new][j_new] = node.board[i][j]
								new_board[i][j] = " "
								new_blue_cards = copy.deepcopy(node.blue_cards)
								new_red_cards = copy.deepcopy(node.red_cards)
								index_of_card = (node.blue_cards).index(card)
								new_blue_cards[index_of_card] = node.common_card
								new_common_card = card
								node_move = Move(i,j,i_new,j_new,index_of_card)
								nn_sign = -node.turn_sign
								new_node = GameStateNode(new_board, new_blue_cards, new_red_cards, new_common_card, 0, node_move, nn_sign)
								node.children.append(new_node)	
								if depth > 0 and new_node.board[0][2] != "BK" and any("RK" in subl for subl in new_node.board) and new_node.board[4][2] != "RK" and any("BK" in subl for subl in new_node.board):
									buildCompleteTree(new_node, depth-1)
							
	
	elif node.turn_sign == -1:
		for i in range(5):
			for j in range(5):
				if node.board[i][j] == "RP" or node.board[i][j] == "RK":
					for card in node.red_cards:
						moves = cards.getCardMoves(card)
						for move in moves:
							i_new = i + (node.turn_sign*move[0])
							j_new = j + (node.turn_sign*move[1])
							if i_new < 0 or j_new < 0 or i_new > 4 or j_new > 4: continue
							elif node.board[i_new][j_new] == "RK" or node.board[i_new][j_new] == "RP": continue
							else:
								new_board = copy.deepcopy(node.board)
								new_board[i_new][j_new] = node.board[i][j]
								new_board[i][j] = " "
								new_blue_cards = copy.deepcopy(node.blue_cards)
								new_red_cards = copy.deepcopy(node.red_cards)
								index_of_card = (node.red_cards).index(card)
								new_red_cards[index_of_card] = node.common_card								
								new_common_card = card								
								node_move = Move(i,j,i_new,j_new,index_of_card)
								nn_sign = -node.turn_sign
								new_node = GameStateNode(new_board, new_blue_cards, new_red_cards, new_common_card, 0, node_move, nn_sign)
								node.children.append(new_node)
								if depth > 0 and new_node.board[0][2] != "BK" and any("RK" in subl for subl in new_node.board) and new_node.board[4][2] != "RK" and any("BK" in subl for subl in new_node.board):
									buildCompleteTree(new_node, depth-1)


def completeTree():
	board = [[" " for x in range(5)] for y in range(5)]
	board[0] = ["RP", "RP", "RK", "RP", "RP"]
	board[4] = ["BP", "BP", "BK", "BP", "BP"]

	red_cards = ["tiger", "dragon"]
	blue_cards = ["crab", "elephant"]
	c_card = "monkey"
	zeroMove = Move(0,0,0,0,0)
	root = GameStateNode(board, blue_cards, red_cards, c_card, 0, zeroMove, 1)

	buildCompleteTree(root, 4)
	f = open("gametree.pkl", "wb")

	pickle.dump(root, f, pickle.HIGHEST_PROTOCOL)

	f.close()

def loadTreeFromFile():
	file_tree = open("gametree.pkl", "rb")

	obj = pickle.load(file_tree)

	while(obj.children != []):
		printboardBOT(obj)
		obj = obj.children[0]

def printboardBOT(obj):
	global turn_counter
	if obj.turn_sign == 1: print("Blue to move")
	elif obj.turn_sign == -1: print("Red to move")
	print("==========================")
	for i in range(5):
		print("|", end="")
		for j in range(5):
			if(obj.board[i][j] == " "): print("   ", end=" |")
			else: print(" " + obj.board[i][j], end=" |")
		print()
		if i == 4: print("==========================")
		else: print("--------------------------")
	print()


# completeTree()
# loadTreeFromFile()
