import tkinter as tk
import tkinter.messagebox
# You may import any submodules of tkinter here if you wish
# You may also import anything from the typing module
# All other additional imports will result in a deduction of up to 100% of your A3 mark

from a3_support import *

# Write your classes here
class Model:
	def __init__(self) -> None:
		"""
			Constructs a new 2048 model instance.
		"""
		self.score_added = 0
		self.un_do_remaining = 3
		self.prev_board = []
		self.prev_score = 0
		self.new_game()

	def new_game(self) -> None:
		"""
			Sets, or resets, the game state to an initial game state. Any information is set to its initial
			state, the tiles are all set to empty, and then two new starter tiles are randomly generated.
		"""
		i = 0
		self._board = [[None for _ in range(4)] for _ in range(4)] 	# 4x4 board ful of all None
		while i < 2:
			self.add_tile()		#Generates 2 random positions for 2 new tiles
			i += 1

	def get_tiles(self) -> list[list[Optional[int]]]:
		"""
			Return the current tiles matrix. Each internal list represents a row of the grid, ordered from top to bottom. 
			Each item in each row list is the integer value on the tile occupying that space, or None if no tile is occupying that space.
		"""
		return self._board

	def add_tile(self) -> None:
		"""
			Randomly generate a new tile at an empty location and add it to the current tiles matrix.
		"""
		random_tiles = generate_tile(self._board)
		position = random_tiles[0]		#row and col
		value = random_tiles[1]
		self._board[position[0]][position[1]] = value

	def move_left(self) -> None:
		"""
			Moves all tiles to their left extreme, merging where necessary. This involves stacking all tiles
			to the left, merging to the left, and then restacking to the left to fill in any gaps created.
		"""
		self.prev_board = self._board	#save the board before move
		self.prev_score = self.score_added	#save the score before move
		self._board = stack_left(self._board)
		self._board, value = combine_left(self._board)
		self._board = stack_left(self._board)
		self.score_added += value		#score added

	def move_right(self) -> None:
		"""
			Moves all tiles to their right extreme, merging where necessary.
		"""
		self.prev_board = self._board	#save the board before move
		self.prev_score = self.score_added	#save the score before move
		self._board = reverse(self._board)
		self._board = stack_left(self._board)
		self._board, value = combine_left(self._board)
		self._board = stack_left(self._board)
		
		self._board = reverse(self._board)	
		self.score_added += value			

	def move_up(self) -> None:
		"""
			Moves all tiles to their top extreme, merging where necessary
		"""
		self.prev_board = self._board	#save the board before move
		self.prev_score = self.score_added	#save the score before move
		self._board = transpose(self._board)
		self._board = stack_left(self._board)
		self._board, value = combine_left(self._board)
		self._board = stack_left(self._board)
		self._board = transpose(self._board)		
		self.score_added += value

	def move_down(self) -> None:
		"""
			Moves all tiles to their bottom extreme, merging where necessary.
		"""
		self.prev_board = self._board	#save the board before move
		self.prev_score = self.score_added	#save the score before move
		self._board = transpose(self._board)
		self._board = reverse(self._board)
		self._board = stack_left(self._board)
		self._board, value = combine_left(self._board)
		self._board = stack_left(self._board)
		self._board = reverse(self._board)	
		self._board = transpose(self._board)
		self.score_added += value
	
	def is_sanme(self, other: list[list[Optional[int]]]) -> bool:
		"""
			Returns True if the move resulted in a change to the game state, else False
		"""
		if self._board == other:
			return False
		else:
			return True

	def attempt_move(self, move:str) -> bool:
		"""
			Makes the appropriate move according to the move string provided. Returns True if the
			move resulted in a change to the game state, else False
		"""
		board_temp = self._board
		board_temp_prev = self.prev_board
		score_temp = self.score_added
		
		if move == 'w':
			self.move_up()
			result = self.is_sanme(board_temp)
		elif move == 'a':
			self.move_left()
			result = self.is_sanme(board_temp)
		elif move == 's':
			self.move_down()
			result = self.is_sanme(board_temp)
		elif move == 'd':
			self.move_right()
			result = self.is_sanme(board_temp)

		self.score_added = score_temp
		self._board = board_temp	#recover the board 
		self.prev_board = board_temp_prev	#recover the prev_board
		return result

	def has_won(self) -> bool:
		"""
			Returns True if the game has been won, else False. The game has been won if a 2048 tile exists on the grid.
		"""
		for row in self._board:
			for i in row:
				if i == 2048:
					return True
				else:
					return False

	def has_lost(self) -> bool:
		"""
			Returns True if the game has been lost, else False. The game has been lost if there are no remaining empty places
			in the grid, but no move would result in a change to the game state.
		"""
		result = 0
		result += self.attempt_move('w')
		result += self.attempt_move('a')
		result += self.attempt_move('s')
		result += self.attempt_move('d')
		if result == 0:
			return True
		else:
			return False
 
	def get_score(self) -> int:
		"""
			Returns the current score of the game.
		"""
		return self.score_added

	def get_undos_remaining(self) -> int:
		"""
			Get the number of undos the player has remaining. This should start at 3 at the beginning of a new game, 
			and reduce each time an undo is used.
		"""
		return self.un_do_remaining
	
	def is_board_initial(self) -> bool:
		"""
			Returns True if the board is in its initial state, else False.
		"""
		count = 0
		for row in self._board:
			for i in row:
				if i != None:
					count += 1
		if count == 2:
			return True
		else:
			return False

	def use_undo(self) -> None:
		"""
			Attempts to undo the previous move, returning the current tiles to the previous tiles state before the last move 
			that made changes to the tiles matrix.
		"""
		if self.un_do_remaining > 0:
			if self.is_board_initial() == False:
				self._board = self.prev_board
				self.score_added = self.prev_score
				self.un_do_remaining -= 1
			else:	#the board is in its initial state
				pass
		else:	#no undo remaining
			pass

class GameGrid(tk.Canvas):	
	"""
		The GameGrid is a view class which inherits from tk.Canvas and represents the 4x4 grid. 
	"""
	def __init__(self, master: tk.Tk, **kwargs) -> None:
		"""
			Sets up a new GameGrid in the master window. The canvas should be 400 pixels wide and 400 pixels tall.
		"""
		self.box_side = 95			# The length of each side of a tile box
		self.padding = 10			# The padding around the edge of the grid
		canvas_side = 400			# The length of each side of the canvas
		
		super().__init__(
			master,
			width=canvas_side, 
			height=canvas_side, 
			bg = BACKGROUND_COLOUR,
			**kwargs)

	def _flash(self, board: list[list[Optional[int]]]) -> None:
		"""
			Redraw the screen
		"""	
		for row in range(4):
			for col in range(4):
				self.draw_box(row, col, board)
	
	def box_coordinate(self, row: int, col: int) -> tuple[tuple[int, int], tuple[int, int]]:
		"""
			Returns the bounding box for the given row and column.
		"""
		# NW corner
		x_min = col * self.box_side + self.padding
		y_min = row * self.box_side + self.padding

		# SE corner
		x_max = x_min + self.box_side
		y_max = y_min + self.box_side

		return (x_min, y_min), (x_max, y_max)

	def draw_box(self, row: int, col: int, board:list[list[Optional[int]]]) -> None:
		"""
			Draws a box at the given row and column.
		"""
		(x_min, y_min), (x_max, y_max) = self.box_coordinate(row, col)

		self.create_rectangle(
			x_min + 5, y_min + 5, 
			x_max, y_max, 
			fill= "#ccc0b3" if board[row][col] == None 
			else "#fcefe6" if board[row][col] == 2
			else "#f2e8cb" if board[row][col] == 4
			else "#f5b682" if board[row][col] == 8
			else "#f29446" if board[row][col] == 16
			else "#ff775c" if board[row][col] == 32
			else "#e64c2e" if board[row][col] == 64
			else "#ede291" if board[row][col] == 128
			else "#fce130" if board[row][col] == 256
			else "#ffdb4a" if board[row][col] == 512
			else "#f0b922" if board[row][col] == 1024
			else "#fad74d",
			width = 1)
		self.draw_number(row, col, board)
		
	def draw_number(self, row: int, col: int, board:list[list[Optional[int]]]) -> None:
		"""
			Draws the given number in the cell at the given position.
		"""
		if board[row][col] == 2:
			color = DARK
		elif board[row][col] == 4:
			color = DARK
		else:
			color = LIGHT

		x_mid, y_mid = self._get_midpoint((row, col))
		if board[row][col] != None:
			self.create_text(
				x_mid+5, y_mid+5, 
				text=str(board[row][col]), 
				font=TILE_FONT,
				fill=color) 

	def _get_bbox(self, position: tuple[int, int]) -> tuple[int, int, int, int]:
		"""
			Return the bounding box for the (row, column) position, in the form (x_min, y_min, x_max, y_max).
		"""
		(x_min, y_min), (x_max, y_max) = self.box_coordinate(position[0], position[1])	
		comb = (x_min, y_min, x_max, y_max)	
		return comb

	def _get_midpoint(self, position: tuple[int, int]) -> tuple[int, int]:
		"""
			Return the graphics coordinates for the center of the cell at the given (row, col) position
		"""
		(x_min, y_min), (x_max, y_max) = self.box_coordinate(position[0], position[1])
		x_mid = (x_min + x_max) // 2
		y_mid = (y_min + y_max) // 2
		return x_mid, y_mid

	def clear(self) -> None:
		"""
			Clears all items.
		"""
		self.delete(tk.ALL)

	def redraw(self, tiles: list[list[Optional[int]]]) -> None:
		"""
			Clears and redraws the entire grid based on the given tiles.
		"""
		self.clear()
		self._flash(tiles)
		

class Game:
	"""
		You must implement a class for the controller, called Game. This class is instantiated in
 		your main function to cause the game to be created and run.
	"""
	def __init__(self, master: tk.Tk) -> None:
		"""
			Constructs a new 2048 game. This method should create a Model instance, set the window
			title, create the title label and create instances of any view classes packed into master. It
			should also bind key press events to an appropriate handler, and cause the initial GUI to be drawn.
		"""
		self.master = master
		self.master.title('CSSE1001/7030 2022 Semester 2 A3')
		title_frame = tk.Frame(
			bg = 'yellow',
			pady = 5
			)
		title_frame.pack(
			side = tk.TOP,
			fill = tk.BOTH)
		display_2048 = tk.Label(
			title_frame,
			text = '2048',
			font = TITLE_FONT,
			bg = 'yellow',
			fg = 'white')
		display_2048.pack()

		self.model = Model()
		self.view = GameGrid(master)
		self.view.pack()
		self.view2 = StatusBar(master)
		self.view2.pack()

		self.master.bind("<Key>", self.attempt_move)		

		self.view2.set_callbacks(self.start_new_game, self.undo_previous_move)
			
		self.view.redraw(self.model._board)
		self.master.mainloop()
	
	def draw(self) -> None:
		"""
			Redraws the entire GUI.
		"""
		self.view.redraw(self.model._board)

	def attempt_move(self, event: tk.Event) -> None:
		"""
			Attempt a move if the event represents a key press on character 'a', 'w', 's', or 'd'. Once a move has been made,
			this method should redraw the view, display the appropriate messagebox if the game has been won, or create a
			new tile after 150ms if the game has not been won.
		"""
		if event.keysym == 'w':
			self.model.move_up()
			self.view.redraw(self.model._board)	
			self.view2.redraw_infos(self.model.get_score(), self.model.get_undos_remaining())
		elif event.keysym == 's':
			self.model.move_down()
			self.view.redraw(self.model._board)	
			self.view2.redraw_infos(self.model.get_score(), self.model.get_undos_remaining())
		elif event.keysym == 'a':
			self.model.move_left()
			self.view.redraw(self.model._board)
			self.view2.redraw_infos(self.model.get_score(), self.model.get_undos_remaining())
		elif event.keysym == 'd':
			self.model.move_right()
			self.view.redraw(self.model._board)	
			self.view2.redraw_infos(self.model.get_score(), self.model.get_undos_remaining())
		if self.model.has_won():
			tkinter.messagebox.showinfo('2048', WIN_MESSAGE)
		else:
			if event.keysym == 'w' or event.keysym == 's' or event.keysym == 'a' or event.keysym == 'd':
				self.master.after(150, self.new_tile)	
	
	def new_tile(self) -> None:
		"""
			None: Adds a new tile to the model and redraws. If the game has
			been lost with the addition of the new tile, then the player should be prompted with the
			appropriate messagebox displaying the LOSS_MESSAGE.

		"""
		self.model.add_tile()
		self.view.redraw(self.model._board)
		if self.model.has_lost() == True:
			tkinter.messagebox.showinfo('2048', LOSS_MESSAGE)

	def undo_previous_move(self) -> None:
		"""
			A handler for when the 'Undo' button is pressed in the status bar. This method should 
			attempt to undo the last action, and then redraw the view classes with the updated model information.
		"""
		self.model.use_undo()
		self.view2.redraw_infos(self.model.get_score(), self.model.get_undos_remaining())
		self.view.redraw(self.model._board)

	def start_new_game(self) -> None:
		"""
			A handler for when the 'New Game' button is pressed in the status bar. This method should 
			cause the model to set its state to that of a new game, and redraw the view classes to reflect these changes.
		"""
		self.model.new_game()
		self.view.redraw(self.model._board)

class StatusBar(tk.Frame):
	def __init__(self, master: tk.Tk, **kwargs):
		"""
			Sets up self to be an instance of tk.Frame and sets up inner frames, labels and buttons in this status bar.
		"""
		super().__init__(
			master, 
			**kwargs)
		
		frame_score = tk.Frame(self, bg = BACKGROUND_COLOUR)
		frame_score.pack(side = tk.LEFT, fill = tk.BOTH, padx=15)
		frame_undo = tk.Frame(self, bg = BACKGROUND_COLOUR)
		frame_undo.pack(side = tk.LEFT, fill = tk.BOTH)

		self._undo = tk.Button(self, text = 'Undo Move',bg = 'white', 
							   font = ('Arial bold', 10), fg = 'black')
		self._new_game = tk.Button(self, text = 'New Game', bg = 'white', 
								   font = ('Arial bold', 10), fg = 'black')

		self._undo.pack(side = tk.TOP, anchor=tk.E, padx = 10, pady = 10)						   
		self._new_game.pack(side = tk.TOP, anchor=tk.E, padx = 10, pady = 10)
		

		self._score_title_label = tk.Label(frame_score, text = 'SCORE', bg = BACKGROUND_COLOUR, font = ('Arial bold', 20), fg = '#ccc0b3')
		self._score_label = tk.Label(frame_score, 
									text = '0', 
									bg = BACKGROUND_COLOUR, 
									font = ('Arial bold', 15),fg = '#f5ebe4')
		self._undo_title_label = tk.Label(frame_undo, text = 'UNDOS', bg = BACKGROUND_COLOUR, font = ('Arial bold', 20), fg = '#ccc0b3')							
		self._undo_label = tk.Label(frame_undo,  
									text = '3',
									bg = BACKGROUND_COLOUR,
									font = ('Arial bold', 15),fg = '#f5ebe4')

		self._score_title_label.pack(side = tk.TOP, anchor=tk.W, padx = 10)
		self._score_label.pack(side = tk.TOP, padx = 10)
		self._undo_title_label.pack(side = tk.TOP, anchor=tk.CENTER, padx=10)
		self._undo_label.pack(side = tk.TOP, padx=10)

	def redraw_infos(self, score: int, undos: int) -> None:	
		"""
			Updates the score and undos labels to reflect the information given.
		"""	

		self._score_label.config(text = score)
		self._undo_label.config(text = undos)

	def set_callbacks(self, new_game_command: callable, undo_command: callable) -> None:
		"""
			Sets the commands for the new game and undo buttons to the given commands. 
			The arguments here are references to functions to be called when the buttons are pressed.
		"""
		self._new_game.config(command = new_game_command)
		self._undo.config(command = undo_command)

def play_game(root):
	"""
		Create an instance of your Game class that uses the given root window as the master argument.
	"""
	#random.seed(10017030)
	Game(root)

if __name__ == '__main__':
	root = tk.Tk()
	play_game(root)
	root.mainloop()






