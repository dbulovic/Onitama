# Onitama game

import random
import tkinter
from tkinter import *
from functools import partial
from tkinter import messagebox

import cards

global all_cards, board, red_cards, blue_cards, extra_card, sign
sign = 1
red_cards = [" ", " "]
blue_cards = [" ", " "]
all_cards = ["tiger", "elephant", "monkey", "crab", "dragon"]

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
			buttons[i_new][j_new].config(command=movep, image=avb)

def move_piece(i, j, new_i, new_j, l1, l2, x, window):
	global sign, extra_card
	board[new_i][new_j] = board[i][j]
	board[i][j] = " "
	if l1['state'] == DISABLED: l1.config(state=ACTIVE)
	elif l1['state'] == ACTIVE: l1.config(state=DISABLED)
	if l2['state'] == DISABLED: l2.config(state=ACTIVE)
	elif l2['state'] == ACTIVE: l2.config(state=DISABLED)
	
	for ni in range (5):
		for nj in range (5):
			buttons[ni][nj].config(command=False)

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

	win_r = check_win()
	if win_r == 1:
		box = messagebox.showinfo("Winner", "Blue Player won the match")
		window.destroy()		
		play()

	if win_r == 2:
		box = messagebox.showinfo("Winner", "Red Player won the match")
		window.destroy()		
		play()

# Create the GUI of game board
def set_board(window, l1, l2):
	global board, buttons, bpwn, bkng, rpwn, rkng, empty, temple, avb, rcard1, rcard2, bcard1, bcard2, ecard
	global tiger, monkey, dragon, elephant, crab

	# setting up the back-end board:
	board = [[" " for x in range(5)] for y in range(5)]
	board[0] = ["RP", "RP", "RK", "RP", "RP"]
	board[4] = ["BP", "BP", "BK", "BP", "BP"]
	
	# setting up the images for the pieces and the cards
	bpwn = PhotoImage(file = r"imgs\bpawn.png")
	rpwn = PhotoImage(file = r"imgs\rpawn.png")
	bkng = PhotoImage(file = r"imgs\bking.png")
	rkng = PhotoImage(file = r"imgs\rking.png")
	empty = PhotoImage(file = r"imgs\empty.png")
	temple = PhotoImage(file = r"imgs\temple.png")
	avb = PhotoImage(file = r"imgs\available.png")
	tiger = PhotoImage(file = r"imgs\tiger.png")
	monkey = PhotoImage(file = r"imgs\monkey.png")
	dragon = PhotoImage(file = r"imgs\dragon.png")
	elephant = PhotoImage(file = r"imgs\elephant.png")
	crab = PhotoImage(file = r"imgs\crab.png")

	buttons = []
	for i in range(5):
		m = 5+i
		buttons.append([])
		for j in range(5):
			n = j
			#field = partial(field_button, i, j, l1, l2)
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
			if board[ni][nj] == "BP": 
				buttons[ni][nj].config(image=bpwn)
			elif board[ni][nj] == "RP": 
				buttons[ni][nj].config(image=rpwn)
			elif board[ni][nj] == "BK": 
				buttons[ni][nj].config(image=bkng)
			elif board[ni][nj] == "RK": 
				buttons[ni][nj].config(image=rkng)
			elif (ni == 0 and nj == 2) or (ni == 4 and nj == 2):
				buttons[ni][nj].config(image=temple)
			else: buttons[ni][nj].config(image=empty)
	

def check_win():
	global board

	if board[0][2] == "BK": return 1
	if not any("RK" in subl for subl in board): return 1

	if board[4][2] == "RK": return 2
	if not any("BK" in subl for subl in board): return 2

	return 0

# Initial setup
def game_window(window):
	window.destroy()
	window = Tk()
	window.title("Onitama")
	l1 = Button(window, activebackground = "blue", text = "Player 1 : Blue", width = 10, state=ACTIVE)
	
	l1.grid(row = 1, column = 1)
	l2 = Button(window, activebackground = "red", text = "Player 2 : Red",
				width = 10, state = DISABLED)
	
	l2.grid(row = 2, column = 1)
	set_board(window, l1, l2)

# main function
def play():
	menu = Tk()
	menu.geometry("480x480")
	menu.title("Onitama")
	gwindow = partial(game_window, menu)
	
	head = Button(menu, text = "Onitama: Strategy Game",
				activeforeground = 'red',
				activebackground = "yellow", bg = "red",
				fg = "yellow", width = 500, font = 'summer', bd = 5)
	
	B1 = Button(menu, text = "Play", command = gwindow, activeforeground = 'red',
				activebackground = "yellow", bg = "red", fg = "yellow",
				width = 500, font = 'summer', bd = 5)
	
	B2 = Button(menu, text = "Exit", command = menu.quit, activeforeground = 'red',
				activebackground = "yellow", bg = "red", fg = "yellow",
				width = 500, font = 'summer', bd = 5)
	head.pack(side = 'top')
	B1.pack(side = 'top')
	B2.pack(side = 'top')
	menu.mainloop()

# Call main function
if __name__ == '__main__':
	play()
