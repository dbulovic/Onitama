# Onitama bot

import random
import cards

def getTurn(board, red_cards):
	sign = -1
	pcs_coors = []
	for i in range(5):
		for j in range(5):
			if board[i][j] == "RP" or board[i][j] == "RK":
				pcs_coors.append([i,j])

	while (True):
		r_piece = random.choice(pcs_coors)
		r_card = random.choice(red_cards)
		
		moves = cards.getCardMoves(r_card)

		for move in moves:
			i_new = r_piece[0] + (sign*move[0])
			j_new = r_piece[1] + (sign*move[1])
			if i_new < 0 or j_new < 0 or i_new > 4 or j_new > 4: continue
			elif board[i_new][j_new] == "RK" or board[i_new][j_new] == "RP": continue
			else:
				return r_piece[0], r_piece[1], i_new, j_new, red_cards.index(r_card)
