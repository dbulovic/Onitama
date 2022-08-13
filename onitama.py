# Onitama game

import random
import tkinter
from tkinter import *
from functools import partial
from tkinter import messagebox

import cards
import onitama_bot

global all_cards, board, red_cards, blue_cards, extra_card, sign, play_bot
sign = 1
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
	board[new_i][new_j] = board[i][j]
	board[i][j] = " "

	# invert the turn buttons
	if l1['state'] == DISABLED: l1.config(state=ACTIVE)
	elif l1['state'] == ACTIVE: l1.config(state=DISABLED)
	if l2['state'] == DISABLED: l2.config(state=ACTIVE)
	elif l2['state'] == ACTIVE: l2.config(state=DISABLED)
	
	# disable field buttons
	for ni in range (5):
		for nj in range (5):
			buttons[ni][nj].config(command=False)

	# switch the used card with extra card
	if sign == 1:
		tmp = blue_cards[x % 2]
		blue_cards[x % 2] = extra_card
		extra_card = tmp
	else: 
		tmp = red_cards[x % 2]
		red_cards[x % 2] = extra_card
		extra_card = tmp

	set_cards()
	set_pieces()
	sign *= -1

	# check win condition
	win_r = check_win()
	if win_r:
		if win_r == 1: winner = "Blue"
		else: winner = "Red"
		box = messagebox.showinfo("Game Over", "%s Player won the match." % winner)
		window.destroy()		
		play()
		return
	
	if play_bot and sign == -1:
		b_i, b_j, bi_new, bj_new, b_x = onitama_bot.getTurn(board, red_cards)
		move_piece(b_i, b_j, bi_new, bj_new, l1, l2, b_x, window)

# Create the GUI of game board
def set_board(window, l1, l2):
	global board, buttons, rcard1, rcard2, bcard1, bcard2, ecard, sign

	sign = 1

	# setting up the back-end board:
	board = [[" " for x in range(5)] for y in range(5)]
	board[0] = ["RP", "RP", "RK", "RP", "RP"]
	board[4] = ["BP", "BP", "BK", "BP", "BP"]
	
	# setting up the images for the pieces
	for piece in all_pieces:
		exec('global %s; %s = PhotoImage(file = r"imgs\%s.png")' % (piece, piece, piece))

	# initialize images for cards
	for card in all_cards:
		exec('global %s; %s = PhotoImage(file = r"imgs\%s.png")' % (card, card, card))

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
	rcard1 = Button(window, command=p_card, image=empty, height=128, width=128)
	rcard1.grid(row=5, column=6, rowspan=2, columnspan=2)

	p_card = partial(select_card, 1, l1, l2, window)
	rcard2 = Button(window, command=p_card, image=empty, height=128, width=128)
	rcard2.grid(row=5, column=8, rowspan=2, columnspan=2)

	p_card = partial(select_card, 2, l1, l2, window)
	bcard1 = Button(window, command=p_card, image=empty, height=128, width=128)
	bcard1.grid(row=8, column=6, rowspan=2, columnspan=2)

	p_card = partial(select_card, 3, l1, l2, window)
	bcard2 = Button(window, command=p_card, image=empty, height=128, width=128)
	bcard2.grid(row=8, column=8, rowspan=2, columnspan=2)

	ecard = Button(window, image=empty, height=128, width=128)
	ecard.grid(row=7, column=12, rowspan=2, columnspan=2)

	pick_random_cards()
	set_cards()

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

# Initial setup
def game_window(window, bot):
	global play_bot

	window.destroy()
	window = Tk()
	window.title("Onitama")
	l1 = Button(window, activebackground = "blue", text = "Player 1 : Blue", width = 10, state=ACTIVE)
	
	l1.grid(row = 1, column = 1)
	l2 = Button(window, activebackground = "red", text = "Player 2 : Red",
				width = 10, state = DISABLED)
	
	l2.grid(row = 2, column = 1)

	if bot: play_bot = True
	else: play_bot = False

	set_board(window, l1, l2)

# main function
def play():
	menu = Tk()
	menu.geometry("480x480")
	menu.title("Onitama")
	gwindow = partial(game_window, menu, False)
	
	head = Button(menu, text = "Onitama: Strategy Game",
				activeforeground = 'red',
				activebackground = "yellow", bg = "red",
				fg = "yellow", width = 500, font = 'summer', bd = 5)
	
	B1 = Button(menu, text = "Play", command = gwindow, activeforeground = 'red',
				activebackground = "yellow", bg = "red", fg = "yellow",
				width = 500, font = 'summer', bd = 5)

	gwindow = partial(game_window, menu, True)
	B2 = Button(menu, text = "Play Bot", command = gwindow, activeforeground = 'red',
				activebackground = "yellow", bg = "red", fg = "yellow",
				width = 500, font = 'summer', bd = 5)
	
	B3 = Button(menu, text = "Exit", command = menu.destroy, activeforeground = 'red',
				activebackground = "yellow", bg = "red", fg = "yellow",
				width = 500, font = 'summer', bd = 5)
	head.pack(side = 'top')
	B1.pack(side = 'top')
	B2.pack(side = 'top')
	B3.pack(side = 'top')
	menu.mainloop()

# Call main function
if __name__ == '__main__':
	play()
