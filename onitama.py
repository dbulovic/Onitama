# Onitama game

import random
import tkinter
from tkinter import *
from functools import partial

# turn
sign = 1

global old_board, board, bpwn, rpwn, empty, avb
board = [[" " for x in range(5)] for y in range(5)]

def field_button(i, j, l1, l2):
	global sign

	# reset commands and images
	for ni in range (5):
		for nj in range (5):
			fieldp = partial(field_button, ni, nj, l1, l2)
			buttons[ni][nj].config(command=fieldp)
			if board[ni][nj] == "BK" or board[ni][nj] == "BP": 
				buttons[ni][nj].config(image=bpwn)
			elif board[ni][nj] == "RK" or board[ni][nj] == "RP": 
				buttons[ni][nj].config(image=rpwn)
			else: buttons[ni][nj].config(image=empty)

	if sign == 1 and (board[i][j] == "BK" or board[i][j] == "BP"):
		movep = partial(moveb, i, j, i-sign, j, l1, l2)	
		buttons[i-sign][j].config(command=movep, image=avb)

	elif sign == -1 and (board[i][j] == "RK" or board[i][j] == "RP"):
		movep = partial(mover, i, j, i-sign, j, l1, l2)	
		buttons[i-sign][j].config(command=movep, image=avb)			


def moveb(i, j, new_i, new_j, l1, l2):
	global sign
	fieldp = partial(field_button, new_i, new_j, l1, l2)
	buttons[new_i][new_j].config(command=fieldp, image=bpwn)
	board[new_i][new_j] = "BP"
	buttons[i][j].config(image=empty)
	board[i][j] = " "
	l1.config(state=DISABLED)
	l2.config(state=ACTIVE)
	sign *= -1	

def mover(i, j, new_i, new_j, l1, l2):
	global sign
	fieldp = partial(field_button, new_i, new_j, l1, l2)
	buttons[new_i][new_j].config(command=fieldp, image=rpwn)
	board[new_i][new_j] = "RP"
	buttons[i][j].config(image=empty)
	board[i][j] = " "
	l1.config(state=ACTIVE)
	l2.config(state=DISABLED)
	sign *= -1


# Create the GUI of game board
def set_board(window, l1, l2):
	global board, old_board, buttons, bpwn, rpwn, empty, avb

	# setting up the back-end board:
	board[0] = ["RP", "RP", "RK", "RP", "RP"]
	board[4] = ["BP", "BP", "BK", "BP", "BP"]

	old_board = board
	
	bpwn = PhotoImage(file = r"imgs\bpawn.png")
	rpwn = PhotoImage(file = r"imgs\rpawn.png")
	empty = PhotoImage(file = r"imgs\empty.png")
	avb = PhotoImage(file = r"imgs\available.png")
	buttons = []
	for i in range(5):
		m = 5+i
		buttons.append([])
		for j in range(5):
			n = j
			field = partial(field_button, i, j, l1, l2)
			buttons[i].append(Button(window, bd=5, command=field, image=empty, height=64, width=64))
			buttons[i][j].grid(row=m, column=n)
			if(i == 0): buttons[i][j].config(image=rpwn, height=64, width=64)
			if(i == 4): buttons[i][j].config(image=bpwn, height=64, width=64)
	window.mainloop()

# Initial setup
def pvp(window):
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
	wpl = partial(pvp, menu)
	
	head = Button(menu, text = "Onitama: Strategy Game",
				activeforeground = 'red',
				activebackground = "yellow", bg = "red",
				fg = "yellow", width = 500, font = 'summer', bd = 5)
	
	B1 = Button(menu, text = "Play", command = wpl, activeforeground = 'red',
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
