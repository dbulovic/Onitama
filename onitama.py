# Onitama game

import random
from time import sleep
from tkinter import *
from functools import partial
from tkinter import messagebox

import cards
import onitama_bot

global turn_counter, date_version
global all_cards, board, red_cards, blue_cards, extra_card, sign, play_bot, only_bots
global empty, emptyb, available, temple, templeb, bking, bkingb, bpawn, bpawnb, rking, rkingb, rpawn, rpawnb
global bot1_var, bot2_var, bot_diff_var, options_bd
global bot1_depth, bot2_depth, bot_diff_depth, depth_options
global rcardslabel1, rcardslabel2, bcardslabel1, bcardslabel2, ncardlabel

global tips_label

date_version = "29-Aug-2023"
depth_options = [1,2,3,4,5]
options_bd = ["Random", "CountPawns", "CountMoves", "ReachTemple", "Combination"]
game_mode = "PvP"
play_bot = False
only_bots = False
turn_counter = 0
red_cards = [" ", " "]
blue_cards = [" ", " "]
all_cards = ["tiger", "elephant", "monkey", "crab", "dragon", "mantis", "ox", "phoenix", "rabbit", "rooster", "boar", "cobra", "crane", "eel", "frog", "goose", "horse", "kirin"]
all_pieces = ["empty", "emptyb", "available", "temple", "templeb", "bking", "bkingb", "bpawn", "bpawnb", "rking", "rkingb", "rpawn", "rpawnb"]

def select_card(x, l1, l2, window):
	global sign, red_cards, blue_cards, tips_label

	if (sign == 1 and (x == 2 or x == 3)) or (sign == -1 and (x == 0 or x == 1)):
		if sign == 1: 
			available_moves = cards.getCardMoves(blue_cards[x % 2])
			if x%2 == 0: 
				bcard1.config(bd = 7)
				bcard2.config(bd = 2)
			elif x%2 == 1: 
				bcard1.config(bd = 2)
				bcard2.config(bd = 7)
			tips_label.config(text='Blue Player: select piece')
		else: 
			available_moves = cards.getCardMoves(red_cards[x % 2])
			if x%2 == 0: 
				rcard1.config(bd = 7)
				rcard2.config(bd = 2)
			elif x%2 == 1: 
				rcard1.config(bd = 2)
				rcard2.config(bd = 7)
			tips_label.config(text='Red Player: select piece')
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
	if sign == 1: tips_label.config(text='Blue Player: select piece')
	else: tips_label.config(text='Red Player: select piece')

	if (sign == 1 and (board[i][j] == "BK" or board[i][j] == "BP")) or (sign == -1 and (board[i][j] == "RK" or board[i][j] == "RP")):
		if sign == 1: tips_label.config(text='Blue Player: select move')
		else: tips_label.config(text='Red Player: select move')
		for move in moves:
			i_new = i+(sign*move[0])
			j_new = j+(sign*move[1])
			if i_new < 0 or j_new < 0 or i_new > 4 or j_new > 4: continue
			if sign == 1 and (board[i_new][j_new] == "BK" or board[i_new][j_new] == "BP"): continue
			if sign == -1 and (board[i_new][j_new] == "RK" or board[i_new][j_new] == "RP"): continue
			movep = partial(move_piece, i, j, i_new, j_new, l1, l2, x, window)
			buttons[i_new][j_new].config(command=movep, image=available)

def move_piece(i, j, new_i, new_j, l1, l2, x, window):
	global sign, extra_card, game_mode

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

	if game_mode != "BvB":
		if sign == 1: tips_label.config(text='Blue Player: select commit turn or undo')
		else: tips_label.config(text='Red Player: select commit turn or undo')

	if ((sign == -1 and game_mode == "PvB") or game_mode == "BvB"):
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

	if game_mode != "BvB":
		if sign == 1: tips_label.config(text='Blue Player: select card')
		else: tips_label.config(text='Red Player: select card')

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
		print("Game Over", "%s Player won the match." % winner)
		box = messagebox.showinfo("Game Over", "%s Player won the match." % winner)
		window.destroy()		
		play()
		return

	undo_b.config(bg='gray', command=False)
	endturn_b.config(bg='gray', command=False)
	setCardButtonsCommands(l1,l2,window)
	botTakeTurn(l1, l2, window)

def setCardButtonsCommands(l1, l2, window):
	global game_mode 
	if game_mode == "BvB": return
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
def play():
	global board, buttons, rcard1, rcard2, bcard1, bcard2, ecard, sign, endturn_b, undo_b
	global blue_cards, red_cards, extra_card, play_bot, bot1_depth, bot2_depth, bot1_var, bot2_var, options_bd, bot_diff_depth, bot_diff_var

	window = Tk()
	window.title("Onitama")

	possible_signs = [-1, 1]
	sign = random.choice(possible_signs)

	l1 = Button(window, text = "Player 1 : Blue", width = 10, bg='gray', fg='white')
	
	l1.grid(row = 1, column = 1, columnspan=2)
	l2 = Button(window, text = "Player 2 : Red", width = 10, bg='gray')

	if sign == 1: l1.config(bg = 'blue')
	elif sign == -1: l2.config(bg = 'red')
	
	l2.grid(row = 2, column = 1, columnspan=2)

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
		exec('global %s_rot; %s_rot = PhotoImage(file = r"imgs/%s_rot.png")' % (card, card, card))

	buttons = []
	for i in range(5):
		m = 5+i
		buttons.append([])
		for j in range(5):
			n = j
			buttons[i].append(Button(window, bd=5, image=empty, height=64, width=64))
			buttons[i][j].grid(row=m, column=n)

	set_pieces()

	global rcardslabel1, rcardslabel2, bcardslabel1, bcardslabel2, ncardlabel
	rcardslabel1 = Label(window, text="Red card1", bg="red")
	rcardslabel1.grid(row=4,column=6)
	rcardslabel2 = Label(window, text="Red card2", bg="red")
	rcardslabel2.grid(row=4,column=8)
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

	bcardslabel1 = Label(window, text="Blue card1", bg="blue", fg="white")
	bcardslabel1.grid(row=10,column=6)
	bcardslabel2 = Label(window, text="Blue card2", bg="blue", fg="white")
	bcardslabel2.grid(row=10,column=8)

	ncardlabel = Label(window, text="neutral card:\ntmp", bg="gray")
	ncardlabel.grid(row=8,column=14)

	p_card = partial(select_card, 2, l1, l2, window)
	bcard1 = Button(window, command=p_card, image=empty, height=128, width=128)
	bcard1.grid(row=8, column=6, rowspan=2, columnspan=2)

	p_card = partial(select_card, 3, l1, l2, window)
	bcard2 = Button(window, command=p_card, image=empty, height=128, width=128)
	bcard2.grid(row=8, column=8, rowspan=2, columnspan=2)

	ecard = Button(window, image=empty, height=128, width=128)
	ecard.grid(row=7, column=12, rowspan=2, columnspan=2)

	endturn_b = Button(window, text="Commit Turn", bg='gray', fg='white')
	endturn_b.grid(row=7, column=14)
	undo_b = Button(window, text="UNDO", bg='gray')
	undo_b.grid(row=7, column=16)

	global options_bd

	mode_label = Label(window, text="Game Mode:")
	mode_label.grid(row = 5, column=17)
	global game_mode
	options_gm = ["PvP", "PvB", "BvB"]
	game_mode_var = StringVar()
	game_mode_var.set(game_mode)
	resetpar = partial(restart, window)
	play_bot_drop = OptionMenu(window, game_mode_var, *options_gm, command=resetpar)
	play_bot_drop.grid(row = 5, column=18)

	diff_label = Label(window, text="Bot Mode:")
	diff_label.grid(row = 5, column=19)

	bot_diff_var = StringVar()
	bot_diff_var.set("Combination")
	
	play_bot_drop = OptionMenu(window, bot_diff_var, *options_bd)
	play_bot_drop.grid(row = 5, column=20)

	global bot_diff_depth
	depth_label = Label(window, text="Bot Depth:")
	depth_label.grid(row = 5, column=21)
	bot_diff_depth = IntVar()
	bot_diff_depth.set(4)
	bot_depth_drop = OptionMenu(window, bot_diff_depth, *depth_options)
	bot_depth_drop.grid(row = 5, column=22)

	bot1_var = StringVar()
	bot2_var = StringVar()

	b1_label = Label(window, text="Red Bot:", bg="red")
	b1_label.grid(row = 6, column=17)
	bot1_var.set("Combination")
	bot1_drop = OptionMenu(window, bot1_var, *options_bd)
	bot1_drop.grid(row = 6, column=18)

	b2_label = Label(window, text="Blue Bot:", bg="blue", fg='white')
	b2_label.grid(row = 7, column=17)
	bot2_var.set("Combination")
	bot2_drop = OptionMenu(window, bot2_var, *options_bd)
	bot2_drop.grid(row = 7, column=18)

	depth_label = Label(window, text="Red Bot Depth:")
	depth_label.grid(row = 6, column=19)
	bot1_depth = IntVar()
	bot1_depth.set(4)
	bot1_depth_drop = OptionMenu(window, bot1_depth, *depth_options)
	bot1_depth_drop.grid(row = 6, column=20)

	depth2_label = Label(window, text="Blue Bot Depth:")
	depth2_label.grid(row = 7, column=19)
	bot2_depth = IntVar()
	bot2_depth.set(4)
	bot2_depth_drop = OptionMenu(window, bot2_depth, *depth_options)
	bot2_depth_drop.grid(row = 7, column=20)

	partial_bvb = partial(play_bvb, window)
	play_bvb_button = Button(window ,text="Whole Game", command=partial_bvb)
	play_bvb_button.grid(row=8, column=18)

	partial_single_bvb = partial(single_bvb, l1,l2,window)
	single_bvb_button = Button(window ,text="Single Move", command=partial_single_bvb)
	single_bvb_button.grid(row=8, column=20)

	help_button = Button(window, text="?", command=helpButton, bg='yellow')
	help_button.grid(row=1, column=22)

	if game_mode != "BvB":
		global tips_label
		tips_label = Label(window, text='initial', bg='yellow')
		tips_label.grid(row=1, column=6, columnspan=3)
		if sign == 1: tips_label.config(text='Blue Player: select card')
		else: tips_label.config(text='Red Player: select card')

	if game_mode == "PvP":
		play_bot_drop.config(state=DISABLED)
		bot_depth_drop.config(state=DISABLED)
		bot1_drop.config(state=DISABLED)
		bot1_depth_drop.config(state=DISABLED)
		bot2_drop.config(state=DISABLED)
		bot2_depth_drop.config(state=DISABLED)
		play_bvb_button.config(state=DISABLED)
		single_bvb_button.config(state=DISABLED)
		play_bot = False
	elif game_mode == "PvB":
		bot1_drop.config(state=DISABLED)
		bot1_depth_drop.config(state=DISABLED)
		bot2_drop.config(state=DISABLED)
		bot2_depth_drop.config(state=DISABLED)
		play_bvb_button.config(state=DISABLED)
		single_bvb_button.config(state=DISABLED)
		rcard1.config(command=False)
		rcard2.config(command=False)
		play_bot = True
	elif game_mode == "BvB":
		play_bot_drop.config(state=DISABLED)
		bot_depth_drop.config(state=DISABLED)
		bcard1.config(command=False)
		bcard2.config(command=False)
		rcard1.config(command=False)
		rcard2.config(command=False)
		play_bot = False

	pick_random_cards()
	set_cards()

	printboard(board)

	botTakeTurn(l1,l2,window)

	window.mainloop()

def helpButton():
	global date_version
	messagebox.showinfo("Help", "Onitama strategy game\n Version from "+date_version+"\nGame modes:\n PvP = Player versus Player\n PvB = Player versus Bot\n BvB = Bot vs Bot")

def restart(window, pb):
	window.destroy()
	global play_bot, game_mode
	game_mode = pb
	if pb == "PvB": play_bot = True
	else: play_bot = False
	play()

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
	global rcardslabel1, rcardslabel2, bcardslabel1, bcardslabel2, ncardlabel
	
	exec("rcard1.config(image=%s_rot, bd = 2)" % red_cards[0])
	exec("rcard2.config(image=%s_rot, bd = 2)" % red_cards[1])
	exec("bcard1.config(image=%s, bd = 2)" % blue_cards[0])
	exec("bcard2.config(image=%s, bd = 2)" % blue_cards[1])
	exec("ecard.config(image=%s)" % extra_card)

	rcardslabel1.config(text=red_cards[0])
	rcardslabel2.config(text=red_cards[1])
	bcardslabel1.config(text=blue_cards[0])
	bcardslabel2.config(text=blue_cards[1])
	ncardlabel.config(text="neutral card:\n%s" % extra_card)

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
	global game_mode, bot_diff_var, bot_diff_depth
	if sign == -1 and game_mode == "PvB":
		bot_diff = bot_diff_var.get()
		b_i, b_j, bi_new, bj_new, b_x = onitama_bot.getTurn(bot_diff, bot_diff_depth.get(), board, blue_cards, red_cards, extra_card, -1)
		move_piece(b_i, b_j, bi_new, bj_new, l1, l2, b_x, window)

def single_bvb(l1,l2,window):
	global sign, board, blue_cards, red_cards, extra_card, bot1_var, bot2_var

	red_strategy = bot1_var.get()
	blue_strategy = bot2_var.get()

	if sign == -1:
		i, j, new_i, new_j, x = onitama_bot.getTurn(red_strategy, bot1_depth.get(), board, blue_cards, red_cards, extra_card, -1)
	else:
		i, j, new_i, new_j, x = onitama_bot.getTurn(blue_strategy, bot1_depth.get(), board, blue_cards, red_cards, extra_card, 1)

	move_piece(i, j, new_i, new_j, l1, l2, x, window)

def play_bvb(window):
	global sign, board, blue_cards, red_cards, extra_card, bot1_var, bot2_var

	red_strategy = bot1_var.get()
	blue_strategy = bot2_var.get()

	# # setting up the back-end board:
	# board = [[" " for x in range(5)] for y in range(5)]
	# board[0] = ["RP", "RP", "RK", "RP", "RP"]
	# board[4] = ["BP", "BP", "BK", "BP", "BP"]

	# global turn_counter
	# turn_counter = 0

	# pick_random_cards()

	# possible_signs = [-1, 1]
	# sign = random.choice(possible_signs)

	# print("============")
	# print("New BvB Game")
	# print("Red player: ", red_strategy, " || Blue player: ", blue_strategy)
	# print("============")
	# printboard(board)

	while(True):
		if sign == -1:
			i, j, new_i, new_j, x = onitama_bot.getTurn(red_strategy, bot1_depth.get(), board, blue_cards, red_cards, extra_card, -1)
		else:
			i, j, new_i, new_j, x = onitama_bot.getTurn(blue_strategy, bot1_depth.get(), board, blue_cards, red_cards, extra_card, 1)

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
			set_cards()
			set_pieces()
			if win_r == 1: winner = "Blue"
			else: winner = "Red"
			print("Game Over", "%s Player won the match." % winner)
			box = messagebox.showinfo("Game Over", "%s Player won the match." % winner)
			window.destroy()		
			play()
			return
	
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
			elif (board[i][j] == "BK"): print(" BM", end=" |")
			elif (board[i][j] == "RK"): print(" RM", end=" |")
			else: print(" " + board[i][j], end=" |")
		if i == 2: print(" Extra card: ", extra_card, end="")
		print()
		if i == 4: print("========================== Blue cards: ", blue_cards)
		else: print("--------------------------")
	print()

# Call main function
if __name__ == '__main__':
	play()

