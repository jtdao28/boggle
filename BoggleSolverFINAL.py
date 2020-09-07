# Boggle Solver
# Justin Dao
# 8/25/20

# This script runs a GUI that assists the user in the game Boggle.
# Run the script and follow the instructions to use the tool.  Enjoy!

from nltk.corpus import words
from nltk.corpus import wordnet
from colour import Color
import tkinter as tk
from tkinter import messagebox

flag = []
Q_vec = []
word_list = []
check_list = []
final_list = []
letter_str = []
word_count = 0
word_index = dict()
mapping = dict()
scores = dict()
ngrams = dict()

def isadjacent(number):

	# PURPOSE: This function determines adjacent tiles and defines the game board.

	# INPUTS: number: An integer value representing the tile in the Boggle grid to be defined.

	# OUTPUTS: A list containing integer values of all the adjacent tiles.

	switch = {
		1: [2, 5, 6],
		2: [1, 3, 5, 6, 7],
		3: [2, 4, 6, 7, 8],
		4: [3, 7, 8],
		5: [1, 2, 6, 9, 10],
		6: [1, 2, 3, 5, 7, 9, 10, 11],
		7: [2, 3, 4, 6, 8, 10, 11, 12],
		8: [3, 4, 7, 11, 12],
		9: [5, 6, 10, 13, 14],
		10: [5, 6, 7, 9, 11, 13, 14, 15],
		11: [6, 7, 8, 10, 12, 14, 15, 16],
		12: [7, 8, 11, 15, 16],
		13: [9, 10, 14],
		14: [9, 10, 11, 13, 15],
		15: [10, 11, 12, 14, 16],
		16: [11, 12, 15]
		}
	return switch.get(number,'invalid')
def import_dict():

	# PURPOSE: This function imports the dictionary from the nltk words corpus.
	# 		   It also provides a list of n-grams, which is defined as all possible
	#		   word beginnings that start with the first n letters. The list of n-grams
	#		   ranges from 1-grams to 16-grams.

	# INPUTS: None.

	# OUTPUTS: A list containing all words, as well was all n-grams from length 1 to 16.

	# Import dictionary
	dict_list = words.words()

	
	keylist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
	ngrams = {key: set() for key in keylist}  # Initialize ngrams dict with set values

	for word in dict_list:
		if len(word) > 16:  # Skip words larger than 16 letters
			continue
		else:
			for ii in range(1,len(word)+1):
				ngrams[ii].add(word[0:ii])

	import_dict.dict = dict_list
	import_dict.ngrams = ngrams
def loop_adjacent(number, start_tile):

	# PURPOSE: This function searches the Boggle grid recursively and finds all
	#		   words of length 2 to 16.  The words are then stored into a list.

	# INPUTS: number: An integer value specifying the tile currently being searched.
	#		  start_tile: An integer value which specifies the origin of the word being searched.

	# OUTPUTS: word_list: A list containing all words found in the Boggle grid.
	#		   word_index: A dictionary whose key is the word and value is the corresponding word position.

	for index, adjacents in enumerate(isadjacent(number), start = 1):
		if start_tile not in check_list:  # always include the start tile
			check_list.append(start_tile)
		if adjacents in check_list:  # stops double counting numbers
			continue
		else:
			check_list.append(adjacents)  # "counts" the letter
			current_string = [mapping[ii] for ii in check_list]
			current_string = "".join(current_string)
		if len(current_string) > 16:  # For edge case where "qu" pushes length > 16
			continue
		else:	
			if current_string in import_dict.ngrams[len(current_string)]:  # check if n-gram
				if current_string in import_dict.dict:  # Exact word -> added to final word list
					word_list.append(current_string)
					word_index.update({current_string:tuple(check_list)})
				loop_adjacent(adjacents, start_tile)  # recurse into next tile if n-gram
				check_list.pop()
			else:
				check_list.pop()  # remove tile from consideration after completing word branch
				continue  # Not an n-gram, will never be a word -> prune branch
def score_word(word):
	# PURPOSE: This function calculates the word score, which is a combination of 
	# 		   individual word points and the word length bonus.

	# INPUTS: The word to be scored, entered as a string.

	# OUTPUTS: word_value: The total point value for the word

	# Boggle point values - individual letter
	# 1: a e i o s r t
	# 2: n l d u
	# 3: y g h
	# 4: c m p b f w j
	# 5: k v
	# 8: x
	# 10: qu z 

	# bonus points, word length:
	# letters : points
	# 2: 1 (always forced 1 point)
	# 5: 3
	# 6: 6
	# 7: 10
	# 8: 15
	# 9: 20
	# 10+: 25

	letter_value = 0
	length_bonus = 0
	word_value = 0
	
	#  Word length bonus points
	if len(word) == 2:
		word_value = 1
	elif len(word) == 5:
		length_bonus = 3
	elif len(word) == 6:
		length_bonus = 6
	elif len(word) >= 7 and len(word) < 10:
		length_bonus = (len(word) - 5) * 5
	elif len(word) > 10:
		length_bonus = 25

	#  Individual letter values
	for letter in word:
		if letter in ['a', 'e', 'i', 'o', 's', 'r', 't']:
			letter_value = letter_value + 1
		elif letter in ['n', 'l', 'd', 'u']:
			letter_value = letter_value + 2
		elif letter in ['y', 'g', 'h']:
			letter_value = letter_value + 3
		elif letter in ['c', 'm', 'p', 'b', 'f', 'w', 'j']:
			letter_value = letter_value + 4
		elif letter in ['k', 'v']:
			letter_value = letter_value + 5
		elif letter  == 'x':
			letter_value = letter_value + 8
		elif letter in ['qu', 'z']:
			letter_value = letter_value + 10

	word_value = letter_value + length_bonus
	return word_value
def solve_boggle(input_str):

	# PURPOSE: This function is the main function that searches every grid position
	#		   and every word length from 2 to 16 letters long.  It will return a dictionary
	#		   whose key is the word and value is the point value.

	# INPUTS: input_str: A string containing all sequential letters from Boggle tiles 1-16.
	#		  This function handles the exception of the Qu tile.

	# OUTPUTS: scores: A sorted dictionary whose key is the word and value is the point value.
	#		   The dictionary is sorted by point value from highest to lowest.

	global check_list
	import_dict()
	# Check for instances of "Q" in input string to account for "Qu" tile exception
	input_str.lower()
	Q_vec = [i for i, x in enumerate(input_str) if x == "q"]
	if len(input_str) - len(Q_vec) != 16 or not input_str.isalpha():
		pass
	else:	
		input_iter = iter(input_str)
		for tile, value in enumerate(input_iter, start = 1):
			# Have to shift indices by number of Qs counted in flag
			if input_str[tile-1 + len(flag)] == "q":
				mapping[tile] = input_str[(tile-1 + len(flag)):(tile+1 + len(flag))]
				flag.append(tile)
				next(input_iter)
			else:
				mapping[tile] = input_str[tile-1 + (len(flag))]
		# Start looping and pruning branches of Boggle tree
		for start_tile in range(1,17):
			loop_adjacent(start_tile,start_tile)
			check_list = []  # This is the reason why check_list must be global
		sorted(word_list)
		
		for word in word_list:  # Remove duplicates
			if word not in final_list:
				final_list.append(word)
				scores[word] = score_word(word)

		# return scores
		return sorted(scores.items(), key = lambda item: item[1], reverse = True)

# Beginning of the GUI portion of the Boggle solver.
window = tk.Tk()

def get_input_Callback():
	# PURPOSE: This function callback triggers when the user clicks the "Submit" button.
	#		   The solve_boggle function is called, taking the user input string. The letters 
	#		   are populated onto the Boggle grid, then the word list is shown in the listbox.

	# INPUTS: A string taken from the user input box.

	# OUTPUTS: Populated Boggle grid and word list, sorted by point value.


	global grid_frame
	global label_list
	user_input = input_box.get()

	Q_vec = [i for i, x in enumerate(user_input) if x == "q"]
	if len(user_input) - len(Q_vec) != 16 or not user_input.isalpha():
		messagebox.showwarning('Invalid String','Please enter a valid 16 tile string! \nExample: \"abcdefghijklnmop\"')
	else:
		# Boggle main grid
		letter_str = []
		letter_iter = iter(user_input)
		for index, letter in enumerate(letter_iter, start = 1):  # Handle "Qu" tile exception
			if letter == 'q':
				letter_str.append(user_input[(index-1 + len(flag)):(index+1 + len(flag))])
				flag.append(index)
				next(letter_iter)
			else:
				letter_str.append(user_input[index-1 + len(flag)])

		master_frame = tk.Frame(master = window)
		master_frame.grid(row = 1, column = 0)

		grid_frame = []
		label_list = []


		for tile in range(16):  # Populate Boggle grid
			col = tile + 1
			row = 1
			if col in [1, 2, 3, 4]:
				pass
			elif col in [5, 6, 7, 8]:
				row = 2
				col = col - 4
			elif col in [9, 10, 11, 12]:
				row = 3
				col = col - 8
			elif col in [13, 14, 15, 16]:
				row = 4
				col = col - 12
			if col % 4 == 0:
				col = 4
			else:
				col = col % 4
			
			grid_dummy = tk.Frame(
				master = master_frame,
				relief = tk.RIDGE,
				width = 100,
				height = 100,
				borderwidth = 10)
			grid_frame.append(grid_dummy)
			grid_dummy.grid(row = row, column = col)
			label = tk.Label(
				master = grid_dummy, 
				text = letter_str[(col-1) + 4*(row-1)].upper(),
				width = 3,
				height = 2,
				font = ('Arial 20 bold')
				)
			label_list.append(label)
			label.pack()
	words = solve_boggle(user_input)

	side_list.delete(0,'end')
	try:
		for ii in words:
			side_list.insert('end', ii)
	except:
		pass

def cur_select_Callback(event):

	# PURPOSE: This function callback occurs after the user clicks on a word
	#		   in the word list.  The word is highlighted in the grid, with 
	#		   the first letter highlighted in green and the last in red.
	#		   The definition of the word is also highlighted, if found in
	#		   the nltk wordnet definitions.

	# INPUTS: Current selection in words listbox.

	# OUTPUTS: The word is highlighted

	try:
		value = side_list.get(side_list.curselection())
		sn = wordnet.synsets(value[0])
		x = 50
		y = 50

		if sn:		
			word_def = sn[0].definition()
			def_text = value[0] + ": (" + sn[0].pos() + ") " + word_def
			master_frame = tk.Frame(master = window, padx = x, pady = y)
			master_frame.grid(row = 2, column = 0)
			definition = tk.Message(master = master_frame)
			definition.config (text = "")
			definition.config(text = def_text)
			definition.pack()

		else:
			master_frame = tk.Frame(master = window, padx = x, pady = y)
			master_frame.grid(row = 2, column = 0)
			definition = tk.Message(master = master_frame)
			definition.config (text = "")
			definition.config(text = 'Definition not found!')
			definition.pack()

		for num in range(16):
			grid_frame[num].config(bg = 'white')

		user_input = input_box.get()
		green = Color('green')
		linear_colors = list(green.range_to(Color('red'),len(value[0])))  # Create green -> red linear space
		for index, letter in enumerate(word_index[value[0]]):
			grid_frame[letter-1].config(bg = linear_colors[index])
	except:
		pass


# Input box for user to enter string
master_frame = tk.Frame(master = window)
master_frame.grid(row = 0, column = 0)
input_box = tk.Entry(master = master_frame)
input_box.pack()

# "Go push button to submit input box"
master_frame = tk.Frame(master = window)
master_frame.grid(row = 0, column = 1)
go_button = tk.Button(master = master_frame, text = 'Submit', command = get_input_Callback)
go_button.pack()

# Letter grid
master_frame = tk.Frame(master = window)
master_frame.grid(row = 1, column = 0)

# Initialize empty Boggle grid
grid_frame = []
label_list = []

for tile in range(16):		
	col = tile + 1
	row = 1
	if col in [1, 2, 3, 4]:
		pass
	elif col in [5, 6, 7, 8]:
		row = 2
		col = col - 4
	elif col in [9, 10, 11, 12]:
		row = 3
		col = col - 8
	elif col in [13, 14, 15, 16]:
		row = 4
		col = col - 12
	if col % 4 == 0:
		col = 4
	else:
		col = col % 4
	
	grid_dummy = tk.Frame(
		master = master_frame,
		relief = tk.RIDGE,
		width = 100,
		height = 100,
		borderwidth = 10)
	grid_frame.append(grid_dummy)
	grid_dummy.grid(row = row, column = col)
	label = tk.Label(
		master = grid_dummy, 
		width = 3,
		height = 2,
		font = ('Arial 20 bold')
		)
	label_list.append(label)
	label.pack()


# Word list
master_frame = tk.Frame(master = window)
master_frame.grid(row = 1, column = 1)

side_list = tk.Listbox(
	master = master_frame,
	selectmode = 'Single')
side_list.bind('<<ListboxSelect>>', cur_select_Callback)
side_list.pack(side = 'left', fill = 'both')
scrollbar = tk.Scrollbar(master = master_frame, command = side_list.yview)
scrollbar.pack(side = 'right', fill = 'both')
side_list.config(yscrollcommand = scrollbar.set)

master_frame = tk.Frame(master = window)
master_frame.grid(row = 2, column = 1)
instructions = tk.Message(
	master = master_frame,
	text = 'INSTRUCTIONS: Enter a 16-letter string starting with the top left-most position' + 
	' in your Boggle grid.  \"Qu\" tiles count as one tile and can be entered as such.' +
	' Click "Submit" to populate grid and word list. When populated, click on a word in the' + 
	' list to see the location of the word. Green tile is the first letter, red tile is the last.')
instructions.pack()

window.mainloop()