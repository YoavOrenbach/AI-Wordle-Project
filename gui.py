import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from factory import *
from common import Placing, AlgorithmType, GameType

WORD_LEN = 5
MAX_TRIES = 6
COLOR_BORDER_HIGHLIGHT = "#565758"
COLOR_BLANK = "#121213"
COLOR_INCORRECT = "#3a3a3c"
COLOR_HALF_CORRECT = "#b59f3b"
COLOR_CORRECT = "#538d4e"
BOX_SIZE = 55
PADDING = 3
APP_ICON = "assets/wordle_logo_32x32.png"


class WordleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # load game and algorithm objects, and set all class members:
        secret_words, legal_words = load_word_lists()
        self.secret_words = secret_words
        self.games_dictionary = get_game_dictionary(secret_words, legal_words)
        self.algorithms_dictionary = get_algorithms_dictionary(self.games_dictionary[GameType.BasicWordle.value])
        self.game = self.games_dictionary[GameType.BasicWordle.value]
        self.game_variable = tk.StringVar(self)
        self.algorithm = self.algorithms_dictionary[AlgorithmType.Random.value]
        self.algorithm_variable = tk.StringVar(self)
        self.secret_word = self.game.generate_secret_word()
        self.secret_word_variable = tk.StringVar()
        self.absurdle = False

        # heading:
        self.heading()

        # game frame:
        self.game_frame = tk.Frame(self, bg=COLOR_BLANK)
        self.game_frame.pack(padx=5, pady=10)
        self.game_options()

        # algorithm frame:
        self.algorithm_frame = tk.Frame(self, bg=COLOR_BLANK)
        self.algorithm_frame.pack(padx=5, pady=10)
        self.algorithm_options()

        # secret_word_frame:
        self.secret_frame = tk.Frame(self, bg=COLOR_BLANK)
        self.secret_frame.pack(padx=5, pady=10)
        self.secret_word_options()

        # play frame:
        self.play_frame = tk.Frame(self, bg=COLOR_BLANK)
        self.play_frame.pack(padx=5, pady=10)
        self.play_area()

        # board frame:
        self.board_frame = tk.Frame(self, bg=COLOR_BLANK)
        self.board_frame.pack(padx=5, pady=10)
        self.init_board()

        # final message frame:
        self.board_full = False
        self.final_frame = tk.Frame(self, bg=COLOR_BLANK)
        self.final_frame.pack(padx=5, pady=10)

        center(self)

    def heading(self):
        self.title("Wordle Agents")
        app_icon = tk.PhotoImage(file=APP_ICON)
        self.iconphoto(False, app_icon)
        self.configure(bg=COLOR_BLANK)
        heading_frame = tk.Frame(self, bg=COLOR_BLANK)
        heading_frame.pack(fill=tk.BOTH, padx=50, pady=10)
        title = tk.Label(heading_frame, text="All Over The WORDLE", fg="#d7dadc", bg=COLOR_BLANK,
                         font=("Helvetica Neue", 28, "bold"))
        title.pack()
        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(fill=tk.X, padx=20)

    def game_options(self):
        game_label = tk.Label(self.game_frame, text="Please choose your desired Wordle game:", fg="#d7dadc",
                              bg=COLOR_BLANK, font=12)
        game_label.pack(side=tk.LEFT, padx=5)
        game_options = [game_type.value for game_type in GameType if game_type != GameType.FakeVocabularyWordle
                        and game_type != GameType.RealVocabularyWordle]
        game_menu = ttk.OptionMenu(self.game_frame, self.game_variable, game_options[0],
                                   *game_options, command=self.change_game)
        game_menu.pack(side=tk.RIGHT, padx=5)
        self.game_variable.set(game_options[0])

    def algorithm_options(self):
        algorithm_label = tk.Label(self.algorithm_frame, text="Please choose your desired Algorithm agent:",
                                   fg="#d7dadc", bg=COLOR_BLANK, font=12)
        algorithm_label.pack(side=tk.LEFT, padx=5)
        algorithm_options = [algorithm_type.value for algorithm_type in AlgorithmType]
        algorithm_menu = ttk.OptionMenu(self.algorithm_frame, self.algorithm_variable, algorithm_options[0],
                                        *algorithm_options, command=self.change_algorithm)
        algorithm_menu.pack(side=tk.RIGHT, padx=5)
        self.algorithm_variable.set(algorithm_options[0])

    def secret_word_options(self):
        secret_label = tk.Label(self.secret_frame, text="Please choose a word for the agent to guess or randomize a word:",
                                fg="#d7dadc", bg=COLOR_BLANK, font=12)
        secret_label.pack(padx=5, pady=5)
        combox = ttk.Combobox(self.secret_frame, textvariable=self.secret_word_variable)
        combox['values'] = self.secret_words
        combox.pack(side=tk.LEFT, expand=True)
        generator_button = tk.Button(self.secret_frame, text="Randomize word", fg="#d7dadc", bg=COLOR_HALF_CORRECT,
                                     highlightbackground=COLOR_BORDER_HIGHLIGHT, font=("Helvetica Neue", 11, "bold"),
                                     activebackground=COLOR_INCORRECT, activeforeground="#d7dadc",
                                     command=self.randomize_secret_word, padx=5)
        bind_button(generator_button, COLOR_HALF_CORRECT)
        generator_button.pack(side=tk.RIGHT, expand=True)
        self.secret_word_variable.set(self.secret_word)

    def change_game(self, *args):
        self.game = self.games_dictionary[self.game_variable.get()]

        if not self.absurdle and self.game_variable.get() == GameType.Absurdle.value:
            for slave in self.secret_frame.pack_slaves():
                slave.pack_forget()
            absrud_msg = "Absurdle game does not have a secret word, but considers all secret words!" \
                         "\nWe only show the first 6 guesses (for consistency)."
            absurd_label = tk.Label(self.secret_frame, text=absrud_msg, fg="#d7dadc", bg=COLOR_BLANK, font=12)
            absurd_label.pack()
            self.absurdle = True

        elif self.absurdle and self.game_variable.get() != GameType.Absurdle.value:
            for slave in self.secret_frame.pack_slaves():
                slave.pack_forget()
            self.secret_word_options()
            self.absurdle = False

    def change_algorithm(self, *args):
        self.algorithm = self.algorithms_dictionary[self.algorithm_variable.get()]

    def randomize_secret_word(self):
        self.secret_word = self.game.generate_secret_word()
        self.secret_word_variable.set(self.secret_word)

    def play_area(self):
        play_lbl = tk.Label(self.play_frame, text="Press play to watch the agent guesses to solve the game:",
                            fg="#d7dadc", bg=COLOR_BLANK, font=12)
        play_lbl.pack(pady=5)
        play_button = tk.Button(self.play_frame, text="play", fg="#d7dadc", bg=COLOR_CORRECT,
                                highlightbackground=COLOR_BORDER_HIGHLIGHT, font=("Helvetica Neue", 11, "bold"),
                                activebackground=COLOR_INCORRECT, activeforeground="#d7dadc", command=self.simulate_game, padx=10)
        bind_button(play_button, COLOR_CORRECT)
        play_button.pack(pady=5)

    def init_board(self):
        # ==> main game grid ==>
        # if there is extra space then give it to main game grid
        self.rowconfigure(3, weight=1)

        container = tk.Frame(self.board_frame, bg=COLOR_BLANK, height=25)
        container.grid()

        self.labels = []
        for i in range(MAX_TRIES):
            row = []
            for j in range(WORD_LEN):
                cell = tk.Frame(
                    container,
                    width=BOX_SIZE,
                    height=BOX_SIZE,
                    highlightthickness=1,
                    highlightbackground=COLOR_INCORRECT,
                )
                cell.grid_propagate(0)
                cell.grid_rowconfigure(0, weight=1)
                cell.grid_columnconfigure(0, weight=1)
                cell.grid(row=i, column=j, padx=PADDING, pady=PADDING)
                t = tk.Label(
                    cell,
                    text="",
                    justify="center",
                    font=("Helvetica Neue", 24, "bold"),
                    bg=COLOR_BLANK,
                    fg="#d7dadc",
                    highlightthickness=1,
                    highlightbackground=COLOR_BLANK,
                )
                t.grid(sticky="nswe")
                row.append(t)
            self.labels.append(row)
        # <== main game grid <==

    def play(self):
        if self.current_guess < MAX_TRIES and not self.game.get_done():
            guess = self.algorithm.get_action(self.game)
            pattern, done, is_win = self.game.step(guess, self.secret_word)
            self.update_board(guess, pattern)
            self.track_play = self.after(10, self.play)
        else:
            self.after_cancel(self.track_play)

    def simulate_game(self):
        if self.secret_word_variable.get() not in self.secret_words:
            messagebox.showwarning("secret word warning", "secret word is not in the list of possible secret words.\n "
                                                          "Please choose a word from the list or generate one randomly")
            return
        self.secret_word = self.secret_word_variable.get()
        self.new_game()
        #self.play()
        #self.current_guess = 0
        is_win = False
        done = False
        while self.current_guess < MAX_TRIES and not done:
            guess = self.algorithm.get_action(self.game)
            pattern, done, is_win = self.game.step(guess, self.secret_word)
            self.update_board(guess, pattern)
        self.game.reset()
        self.game_over(is_win)

    def new_game(self):
        # reset the grid
        for i in range(MAX_TRIES):
            self.current_guess = i
            self.update_labels()
        self.current_guess = 0

    def update_board(self, guess, pattern):
        colors = []
        for placing in pattern:
            if placing == int(Placing.correct):
                colors.append(COLOR_CORRECT)
            elif placing == int(Placing.misplaced):
                colors.append(COLOR_HALF_CORRECT)
            else:
                colors.append(COLOR_INCORRECT)
        self.update_labels(guess, colors)
        self.current_guess += 1

    def update_labels(self, guess="", colors=None):
        for i, label in enumerate(self.labels[self.current_guess]):
            try:
                letter = guess[i]
            except IndexError:
                letter = ""

            label["text"] = letter
            if colors:
                label["bg"] = colors[i]
                label["highlightbackground"] = colors[i]
            else:
                label["bg"] = COLOR_BLANK
                label["highlightbackground"] = (
                    COLOR_BORDER_HIGHLIGHT if letter else COLOR_BLANK
                )

    def game_over(self, is_win):
        if self.board_full:
            for slave in self.final_frame.pack_slaves():
                slave.pack_forget()
        if is_win:
            game_over_msg = f"{self.algorithm_variable.get()} agent won in {self.current_guess} " \
                            f"guesses at {self.game_variable.get()} game!"
        else:
            game_over_msg = f"{self.algorithm_variable.get()} agent Lost at {self.game_variable.get()} game."

        game_over_label = tk.Label(self.final_frame, text=game_over_msg, fg="#d7dadc", bg=COLOR_BLANK, font=12)
        game_over_label.pack(side=tk.LEFT, padx=5)
        reset_button = tk.Button(self.final_frame, text="reset board", fg="#d7dadc", bg=COLOR_HALF_CORRECT,
                                 highlightbackground=COLOR_BORDER_HIGHLIGHT, font=("Helvetica Neue", 11, "bold"),
                                 activebackground=COLOR_INCORRECT, activeforeground="#d7dadc", command=self.reset_board,
                                 padx=5)
        bind_button(reset_button, COLOR_HALF_CORRECT)
        reset_button.pack(side=tk.RIGHT, padx=5)
        self.board_full = True

    def reset_board(self):
        self.board_full = False
        self.new_game()
        for slave in self.final_frame.pack_slaves():
            slave.pack_forget()


def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(int(width*1.1), int(height*1.1), x, y))
    win.deiconify()


def on_hover(button):
    button.config(bg=COLOR_INCORRECT)


def on_leave(button, color):
    button.config(bg=color)


def bind_button(button, color):
    button.bind('<Enter>', lambda event, x=button: on_hover(x))
    button.bind('<Leave>', lambda event, x=button, y=color: on_leave(x, y))


if __name__ == "__main__":
    WordleApp().mainloop()

