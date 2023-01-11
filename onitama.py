# Onitama game

import random
from time import sleep
from tkinter import *
from functools import partial
from tkinter import messagebox

import cards
import onitama_bot

global turn_counter
global all_cards, board, red_cards, blue_cards, extra_card, sign, play_bot, only_bots
global empty, emptyb, available, temple, templeb, bking, bkingb, bpawn, bpawnb, rking, rkingb, rpawn, rpawnb
only_bots = False
turn_counter = 0
red_cards = [" ", " "]
blue_cards = [" ", " "]
all_cards = ["tiger", "elephant", "monkey", "crab", "dragon"]
all_pieces = ["empty", "emptyb", "available", "temple", "templeb", "bking", "bkingb", "bpawn", "bpawnb", "rking", "rkingb", "rpawn", "rpawnb"]

def select_card(x, l1, l2, window):
	global sign, red_cards, blue_cards

	if (sign == 1 and (x == 2 or x == 3)) or (sign == -1 and (x == 0 or x == 1)):
		if sign == 1: available_moves = cards.getCardMoves(blue_cards[x % 2])
		else: available_moves = cards.getCardMoves(red_cards[x % 2])
		for ni in range (5):
			for nj in range (5):
				fieldp = partial(field_button, ni, nj, l1, l2, available_moves, x, window)
				buttons[ni][nj].config(command=fieldp)
		set_pieces()	

def field_button(i, j, l1, l2, moves, x, window):
	global sign

	# reset commands and images
	for ni in range (5):
		for nj in range (5):
			fieldp = partial(field_button, ni, nj, l1, l2, moves, x, window)
			buttons[ni][nj].config(command=fieldp)
	set_pieces()

	if (sign == 1 and (board[i][j] == "BK" or board[i][j] == "BP")) or (sign == -1 and (board[i][j] == "RK" or board[i][j] == "RP")):
		for move in moves:
			i_new = i+(sign*move[0])
			j_new = j+(sign*move[1])
			if i_new < 0 or j_new < 0 or i_new > 4 or j_new > 4: continue
			if sign == 1 and (board[i_new][j_new] == "BK" or board[i_new][j_new] == "BP"): continue
			if sign == -1 and (board[i_new][j_new] == "RK" or board[i_new][j_new] == "RP"): continue
			movep = partial(move_piece, i, j, i_new, j_new, l1, l2, x, window)
			buttons[i_new][j_new].config(command=movep, image=available)

def move_piece(i, j, new_i, new_j, l1, l2, x, window):
	global sign, extra_card, play_bot

	# move the piece
	old_f = board[new_i][new_j] 
	board[new_i][new_j] = board[i][j]
	board[i][j] = " "

	# switch the used card with extra card
	if sign == 1:
		tmp = blue_cards[x % 2]
		blue_cards[x % 2] = extra_card
		extra_card = tmp
	else: 
		tmp = red_cards[x % 2]
		red_cards[x % 2] = extra_card
		extra_card = tmp
	
	# disable field and card buttons
	for ni in range (5):
		for nj in range (5):
			buttons[ni][nj].config(command=False)

	bcard1.config(command=False)
	bcard2.config(command=False)
	rcard1.config(command=False)
	rcard2.config(command=False)

	set_cards()
	set_pieces()

	if (sign == -1 and play_bot):
		endTurn(l1, l2, window)
		return

	undop = partial(undoTurn, i, j, new_i, new_j, old_f, x, l1,l2,window)
	undo_b.config(bg='red', command=undop)

	endp = partial(endTurn, l1, l2, window)
	endturn_b.config(bg='blue', command=endp)


def undoTurn(i, j, new_i, new_j, old_field, x, l1,l2,window):
	global extra_card
	# move the piece back
	moved_piece = board[new_i][new_j]
	board[new_i][new_j] = old_field
	board[i][j] = moved_piece

	# switch the cards back
	if sign == 1:
		tmp = blue_cards[x % 2]
		blue_cards[x % 2] = extra_card
		extra_card = tmp
	else: 
		tmp = red_cards[x % 2]
		red_cards[x % 2] = extra_card
		extra_card = tmp

	undo_b.config(bg='gray', command=False)
	endturn_b.config(bg='gray', command=False)

	set_cards()
	set_pieces()
	setCardButtonsCommands(l1,l2,window)

def endTurn(l1, l2, window):
	global sign
	sign *= -1

	printboard(board)

	# invert the turn buttons
	if sign == 1:
		l1.config(bg='blue')
		l2.config(bg='gray')
	elif sign == -1:
		l1.config(bg='gray')
		l2.config(bg='red')

	# check win condition
	win_r = check_win()
	if win_r:
		if win_r == 1: winner = "Blue"
		else: winner = "Red"
		box = messagebox.showinfo("Game Over", "%s Player won the match." % winner)
		window.destroy()		
		play()
		return

	undo_b.config(bg='gray', command=False)
	endturn_b.config(bg='gray', command=False)
	setCardButtonsCommands(l1,l2,window)
	botTakeTurn(l1, l2, window)

def setCardButtonsCommands(l1, l2, window):
	p_card = partial(select_card, 2, l1, l2, window)
	bcard1.config(command=p_card)
	p_card = partial(select_card, 3, l1, l2, window)
	bcard2.config(command=p_card)
	if not play_bot:
		p_card = partial(select_card, 0, l1, l2, window)
		rcard1.config(command=p_card)
		p_card = partial(select_card, 1, l1, l2, window)
		rcard2.config(command=p_card)

# Create the GUI of game board
def set_board(window, l1, l2):
	global board, buttons, rcard1, rcard2, bcard1, bcard2, ecard, sign, endturn_b, undo_b
	global blue_cards, red_cards, extra_card

	# setting up the back-end board:
	board = [[" " for x in range(5)] for y in range(5)]
	board[0] = ["RP", "RP", "RK", "RP", "RP"]
	board[4] = ["BP", "BP", "BK", "BP", "BP"]

	global turn_counter
	turn_counter = 0
	
	# setting up the images for the pieces
	for piece in all_pieces:
		exec('global %s; %s = PhotoImage(file = r"imgs/%s.png")' % (piece, piece, piece))

	# initialize images for cards
	for card in all_cards:
		exec('global %s; %s = PhotoImage(file = r"imgs/%s.png")' % (card, card, card))

	buttons = []
	for i in range(5):
		m = 5+i
		buttons.append([])
		for j in range(5):
			n = j
			buttons[i].append(Button(window, bd=5, image=empty, height=64, width=64))
			buttons[i][j].grid(row=m, column=n)

	set_pieces()	

	p_card = partial(select_card, 0, l1, l2, window)
	rcard1 = Button(window, image=empty, height=128, width=128)
	rcard1.grid(row=5, column=6, rowspan=2, columnspan=2)
	if not play_bot:
		rcard1.config(command=p_card)

	p_card = partial(select_card, 1, l1, l2, window)
	rcard2 = Button(window, image=empty, height=128, width=128)
	rcard2.grid(row=5, column=8, rowspan=2, columnspan=2)
	if not play_bot:
		rcard2.config(command=p_card)

	p_card = partial(select_card, 2, l1, l2, window)
	bcard1 = Button(window, command=p_card, image=empty, height=128, width=128)
	bcard1.grid(row=8, column=6, rowspan=2, columnspan=2)

	p_card = partial(select_card, 3, l1, l2, window)
	bcard2 = Button(window, command=p_card, image=empty, height=128, width=128)
	bcard2.grid(row=8, column=8, rowspan=2, columnspan=2)

	ecard = Button(window, image=empty, height=128, width=128)
	ecard.grid(row=7, column=12, rowspan=2, columnspan=2)

	endturn_b = Button(window, text="End Turn", bg='gray')
	endturn_b.grid(row=7, column=14)
	undo_b = Button(window, text="UNDO", bg='gray')
	undo_b.grid(row=7, column=16)

	pick_random_cards()
	set_cards()

	printboard(board)

	botTakeTurn(l1,l2,window)

	window.mainloop()

def pick_random_cards():
	global all_cards, red_cards, blue_cards, extra_card

	indices = []
	for i in range(len(all_cards)):
		indices.append(i)

	choices = random.sample(indices, k=5)

	red_cards[0] = all_cards[choices[0]]
	red_cards[1] = all_cards[choices[1]]
	blue_cards[0] = all_cards[choices[2]]
	blue_cards[1] = all_cards[choices[3]]
	extra_card = all_cards[choices[4]]


def set_cards():
	global red_cards, blue_cards, extra_card
	
	exec("rcard1.config(image=%s)" % red_cards[0])
	exec("rcard2.config(image=%s)" % red_cards[1])
	exec("bcard1.config(image=%s)" % blue_cards[0])
	exec("bcard2.config(image=%s)" % blue_cards[1])
	exec("ecard.config(image=%s)" % extra_card)

def set_pieces():
	global board, buttons

	for ni in range (5):
		for nj in range (5):
			if (ni % 2 == 0) == (nj % 2 == 0): 
				if board[ni][nj] == "BP": 
					buttons[ni][nj].config(image=bpawnb)
				elif board[ni][nj] == "RP": 
					buttons[ni][nj].config(image=rpawnb)
				elif board[ni][nj] == "BK": 
					buttons[ni][nj].config(image=bkingb)
				elif board[ni][nj] == "RK": 
					buttons[ni][nj].config(image=rkingb)
				elif (ni == 0 and nj == 2) or (ni == 4 and nj == 2):
					buttons[ni][nj].config(image=templeb)
				else:
					buttons[ni][nj].config(image=emptyb)
			else:
				if board[ni][nj] == "BP": 
					buttons[ni][nj].config(image=bpawn)
				elif board[ni][nj] == "RP": 
					buttons[ni][nj].config(image=rpawn)
				elif board[ni][nj] == "BK": 
					buttons[ni][nj].config(image=bking)
				elif board[ni][nj] == "RK": 
					buttons[ni][nj].config(image=rking)
				else:
					buttons[ni][nj].config(image=empty)
	

def check_win():
	global board

	if board[0][2] == "BK": return 1
	if not any("RK" in subl for subl in board): return 1

	if board[4][2] == "RK": return 2
	if not any("BK" in subl for subl in board): return 2

	return 0

def botTakeTurn(l1,l2,window):
	if sign == -1 and play_bot:
		b_i, b_j, bi_new, bj_new, b_x = onitama_bot.getTurn(board, blue_cards, red_cards, extra_card, -1)
		move_piece(b_i, b_j, bi_new, bj_new, l1, l2, b_x, window)

# Initial setup
def game_window(window, bot):
	global play_bot, sign

	window.destroy()
	window = Tk()
	window.title("Onitama")

	possible_signs = [-1, 1]
	sign = random.choice(possible_signs)

	l1 = Button(window, text = "Player 1 : Blue", width = 10, bg='gray')
	
	l1.grid(row = 1, column = 1, columnspan=2)
	l2 = Button(window, text = "Player 2 : Red", width = 10, bg='gray')

	if sign == 1: l1.config(bg = 'blue')
	elif sign == -1: l2.config(bg = 'red')
	
	l2.grid(row = 2, column = 1, columnspan=2)

	play_bot = bot

	set_board(window, l1, l2)

def botVbot(window):
	window.destroy()
	global sign, board, blue_cards, red_cards, extra_card

	# setting up the back-end board:
	board = [[" " for x in range(5)] for y in range(5)]
	board[0] = ["RP", "RP", "RK", "RP", "RP"]
	board[4] = ["BP", "BP", "BK", "BP", "BP"]

	global turn_counter
	turn_counter = 0

	pick_random_cards()

	possible_signs = [-1, 1]
	sign = random.choice(possible_signs)

	printboard(board)

	while(True):
		if sign == -1:
			i, j, new_i, new_j, x = onitama_bot.getTurn(board, blue_cards, red_cards, extra_card, -1)
		else:
			i, j, new_i, new_j, x = onitama_bot.getTurn(board, blue_cards, red_cards, extra_card, 1)

		# move the piece
		board[new_i][new_j] = board[i][j]
		board[i][j] = " "

		# switch the used card with extra card
		if sign == 1:
			tmp = blue_cards[x % 2]
			blue_cards[x % 2] = extra_card
			extra_card = tmp
		else: 
			tmp = red_cards[x % 2]
			red_cards[x % 2] = extra_card
			extra_card = tmp

		sign *= -1
		printboard(board)

		win_r = check_win()
		if win_r:
			if win_r == 1: winner = "Blue"
			else: winner = "Red"
			print("Game Over", "%s Player won the match." % winner)
			return


# main function
def play():
	menu = Tk()
	menu.geometry("480x480")
	menu.title("Onitama")
	gwindow = partial(game_window, menu, False)
	
	head = Button(menu, text = "Onitama: Strategy Game",
				activeforeground = 'red',
				activebackground = "yellow", bg = "yellow",
				fg = "red", width = 500, font = 'summer', bd = 5)
	
	B1 = Button(menu, text = "Play", command = gwindow, activeforeground = 'red',
				activebackground = "yellow", bg = "red", fg = "yellow",
				width = 500, font = 'summer', bd = 5)

	gwindow = partial(game_window, menu, True)
	B2 = Button(menu, text = "Play Bot", command = gwindow, activeforeground = 'red',
				activebackground = "yellow", bg = "red", fg = "yellow",
				width = 500, font = 'summer', bd = 5)

	botvbotp = partial(botVbot, menu)
	B3 = Button(menu, text = "Bot v Bot", command = botvbotp, activeforeground = 'red',
				activebackground = "yellow", bg = "red", fg = "yellow",
				width = 500, font = 'summer', bd = 5)
	
	B4 = Button(menu, text = "Exit", command = menu.destroy, activeforeground = 'red',
				activebackground = "yellow", bg = "red", fg = "yellow",
				width = 500, font = 'summer', bd = 5)
	head.pack(side = 'top')
	B1.pack(side = 'top')
	B2.pack(side = 'top')
	B3.pack(side = 'top')
	B4.pack(side = 'top')
	menu.mainloop()
	
def printboard(board):
	global turn_counter, red_cards, blue_cards, extra_card
	if sign == 1: print("Turn #%d -- Blue to move" %turn_counter)
	elif sign == -1: print("Turn #%d -- Red to move" %turn_counter)
	turn_counter += 1
	print("========================== Red cards: ", red_cards)
	for i in range(5):
		print("|", end="")
		for j in range(5):
			if(board[i][j] == " "): print("   ", end=" |")
			else: print(" " + board[i][j], end=" |")
		if i == 2: print(" Extra card: ", extra_card, end="")
		print()
		if i == 4: print("========================== Blue cards: ", blue_cards)
		else: print("--------------------------")
	print()

# Call main function
if __name__ == '__main__':
	play()
