import tkinter 
from tkinter import * 
from time import * 
from stopwatch import Stopwatch
import re, random, datetime 
import time
import calc
import database 


class User:
    def __init__(self, username, gross_wpm, net_wpm, chpm, time_for_attempt, real_time, error_rate, score):
        self.username = username
        self.gross_wpm = gross_wpm
        self.net_wpm = net_wpm
        self.chpm = chpm
        self.time_for_attempt = time_for_attempt
        self.real_time = real_time
        self.error_rate = error_rate
        self.score = score 

    def add(self):
        database.add_user()
    
    def add_stats(self):
        database.add_one_stats(
                            self.username,
                            self.gross_wpm,
                            self.net_wpm,
                            self.chpm,
                            self.error_rate,
                            self.time_for_attempt,
                            self.real_time,
                            self.score
                                        )


class App():
    def __init__(self, master, text):
        self.master = master 
        self.text = text 
        self.score = 0 
        self.characters_correct = 0 
        self.errors = 0

        self.username = ""

        self.characters_correct_var = IntVar()
        self.errors_var = IntVar()
        self.stats_variable = StringVar()

        self.stopwatch = Stopwatch()

        # Set up menus
        self.menubar = Menu(self.master)  # Initiate menu template
        self.optionsmenu = Menu(self.menubar)  # Initiate options menu
        self.helpmenu = Menu(self.menubar, tearoff=0)  # Initiate help menu

        # Master Window Sizes
        self.x = 800
        self.y = 600 
        
        # User Monitor Resolution
        self.monitor_width = self.master.winfo_screenwidth()
        self.monitor_height = self.master.winfo_screenheight()

        # Centering window 
        self.window_placement(self.master, self.x, self.y)
        # Naming the window
        self.master.title("Speed Typing Test")

        # No-resizable master window 
        self.master.resizable(False, False)

        # Adding Background
        self.master.configure(background='#617D6F')

        # Setting up the default screen and labels 
        self.title_label = Label(self.master, text="SPEED TYPING GAME")
        self.title_label.place(width=200, height=35, relx=0.5, rely=0.09, anchor='center')

        self.score_label = Label(self.master, text="Highest Score: {}".format(self.score))
        self.score_label.place(width=200, height=35, relx=0.03, rely=0.9)

        self.stopwatch_label = Label(self.master, bg="#ffffff", fg="#000000")
        self.stopwatch_label.place(height=35, width=100, relx=0.07, rely=0.04, anchor='center')

        self.time_label = Label(self.master)
        self.time_label.place(height=35, width=100, relx=0.93, rely=0.04, anchor='center')

        # Creating interaction Boxes

        self.input_box = Entry(self.master, font=('Arial', 12), bg="#F8F8FF")
        self.input_box.place(height=30, width=300, relx=0.5, rely=0.5, anchor='center')

        self.input_box.bind("<FocusIn>", lambda x: self.stopwatch_on_typing()) 
        self.input_box.bind("<FocusOut>", lambda x: self.stopwatch_stop())
        self.input_box.bind("<BackSpace>", lambda x: self.backspace())

        self.text_box = Text(self.master, font=('Arial', 12), bg="#F8F8FF", wrap=WORD)
        self.text_box.place(height=130, width=300, relx=0.5, rely=0.3, anchor='center')
        self.text_box.insert(1.0, self.text)
        self.text_box.config(state=DISABLED)

        reg = self.master.register(self.correct_callback)
        self.input_box.config(validate="key", validatecommand=(reg, '%P', self.text))

        # Set up buttons
        self.start_button = Button(self.master, text="Press me to start", command=self.start_with_button)
        self.start_button.place(height=30, width=100, relx=0.37, rely=0.6, anchor='center')

        self.restart_button = Button(self.master, text="Restart", command = self.stopwatch_restart)
        self.restart_button.place(height=30, width=100, relx=0.5, rely=0.6, anchor='center')

        self.close_button = Button(self.master, text="Exit", command=self.master.destroy)
        self.close_button.place(height=30, width=60, relx=0.92, rely=0.92, anchor='center')


        OPTIONS = [ 
                    "Article",
                    "Paragraph",
                    "Data Entry"
        ]
        self.genre = StringVar(self.master)
        self.genre.set(OPTIONS[0])  # default value

        dropdown = OptionMenu(self.master, self.genre, *OPTIONS, command=lambda x: self.genre_chosen(self.genre.get()))
        dropdown.place(height=30, width=100, relx=0.63, rely=0.6, anchor='center')

        self.user_box()
        self.create_menu()
        self.username = self.set_username()
        self.update_clock()
        self.master.mainloop()

    
    def window_placement(self, window, x, y):
        """ Takes in a window name and sizes and places it in the middle of the screen """
        pos_horizontally = int((self.monitor_width / 2) - (x / 2))
        pos_vertically = int((self.monitor_height / 2) - (y / 2))
        window.geometry("%dx%d+%d+%d" % (x, y, pos_horizontally, pos_vertically))

    def raise_above_all(window):
        window.attributes('-topmost', 1)

    def genre_chosen(self, genre):
        """Call db to choose a random text with the given genre """
        text = database.get_text(genre)
        self.text_box.config(state=NORMAL)
        self.text_box.delete("1.0", END)
        self.text_box.insert(1.0, text)
        self.text_box.config(state=DISABLED)

        
    def update_clock(self):
            now = datetime.datetime.now()
            self.time_label.configure(text=now.strftime("%H:%M:%S"))
            self.master.after(1000, self.update_clock)
    
    def stopwatch_start(self):
        self.input_box.delete("0", END)
        self.current_time = datetime.datetime.now().strftime("%H:%M")
        self.stopwatch.start()
        self.stopwatch_update()

    def start_with_button(self):
        # waits 1 second until player puts their cursor in typing field
        self.stopwatch.reset()
        self.input_box.delete("0", END)
        self.current_time = datetime.datetime.now().strftime("%H:%M")
        time.sleep(1)
        self.stopwatch.start()
        self.stopwatch_update()

    def stopwatch_update(self): 
        self.stopwatch_label.configure(text=str(self.stopwatch))
        self.master.after(50, self.stopwatch_update)
    
    def stopwatch_restart(self):
        self.stopwatch.reset()
        self.input_box.delete("0", END)
        self.master.focus_set()
    
    def stopwatch_stop(self):
        stopped_time = str(self.stopwatch)
        self.stopwatch.stop()
        print(stopped_time)
        return stopped_time

    def stopwatch_on_typing(self):
        self.stopwatch.reset()
        self.current_time = datetime.datetime.now().strftime("%H:%M")
        self.input_box.delete("0", END)
        time.sleep(0.5)
        self.stopwatch.start()
        self.stopwatch_update()
    
    def correct_callback(self, input, text):
        self.characters_correct = self.characters_correct_var.get()
        self.errors = self.errors_var.get()
        
        if input == self.text_box.get(1.0, 'end-1c'): 
            self.stopped_time = self.stopwatch_stop()
            words = self.input_box.get().split(" ")
            words_len = len(words)
            total_characters = len(text)
            try: 
                attempt_time = eval(str(self.stopped_time).replace("s", ""))
            except SyntaxError:
                attempt_time = eval(str(self.stopped_time).replace("m", ""))


            gross_wpm = calc.wpm(words_len, attempt_time)
            net_wpm = calc.net_wpm(gross_wpm, self.errors)
            chpm = calc.chpm(attempt_time, self.characters_correct)
            error_rate = calc.error_rate(self.errors, self.characters_correct, total_characters)
        
            user = User(
                        self.username, 
                        gross_wpm, 
                        net_wpm, 
                        chpm, 
                        attempt_time, 
                        self.current_time, 
                        error_rate, 
                        self.score
                        )


            self.display_user_stats(attempt_time, self.current_time, gross_wpm, net_wpm, chpm, error_rate, self.score)
            print("End")

        if re.match(input, self.text):
            self.input_box.config(fg='green')
            self.characters_correct_var.set(self.characters_correct + 1)
            self.score += 10
        else:
            self.score -= 10
            self.errors_var.set(self.errors + 1)
            self.input_box.config(fg='red')
        return True
    
    def backspace(self):
        self.characters_correct_var.set(self.characters_correct - 1)

    def display_user_stats(self, attempt_time, current_time, gross_wpm, net_wpm, chpm, error_rate, score):
        self.string =  "Attempt Time: {}s\nTime of the attempt: {}\nGross words per minute: {}\nNet words per minute: {}\nCharacters per minute: {}\nAccuracy {}%\nScore: {}"
        
        self.stats_window = Toplevel(self.master) # create a window on top
        self.stats_window.title("Player Statistics")

        self.stats_variable.set(self.string.format(attempt_time, current_time, gross_wpm, net_wpm, chpm, error_rate, score))

        self.window_placement(self.stats_window, 400, 300)

        label = Label(self.stats_window, text="Statistics", font=('Arial', 12, 'bold'))
        label.place(width=100, height=30, relx=0.5, rely=0.2, anchor='center')

        stats_label = Label(self.stats_window, textvariable=self.stats_variable, font=('Arial', 11, 'bold'), justify='left')
        stats_label.place(width=250, height=150, relx=0.5, rely=0.5, anchor='center')
        self.stopwatch_restart()

    def user_box(self):
        self.username_box = Toplevel(self.master)
        self.username_box.title("Player Username")
        self.username_box.configure(background='#8cab9c')
        self.window_placement(self.username_box, 320, 400)
        self.master.lower()
        

        self.label_text = "Username must be between 3-15 characters \nValid characters: a-z 0-9 _&$£\nPlease enter your username:\n"
        self.label = Label(self.username_box, wraplength=180, justify="center", bg='#617D6F', fg="#ffffff", text=self.label_text)
        self.label.place(height=200, width=190, relx=0.5, rely=0.4, anchor='center')

        self.user_input_box = Entry(self.username_box, font=('Arial', 12), bg="#F8F8FF") # box where user enters their username
        self.user_input_box.place(height=25, width=140, relx=0.5, rely=0.5, anchor='center')

        self.user_exit_button = Button(self.username_box, text="Exit", command=self.username_box.destroy) # exits the program
        self.user_exit_button.place(height=30, width=60, relx=0.5, rely=0.7, anchor='center')

        self.enter_button = Button(self.username_box, text="Enter", command=self.username_enter) # creating a button to submit username
        self.enter_button.place(height=30, width=80, relx=0.5, rely=0.6, anchor='center')
        
        reg = self.username_box.register(self.user_validate)
        self.user_input_box.config(validate="key", validatecommand=(reg, '%P'))

    def username_enter(self):
        """ Hey new user! / Welcome back, <username>! Your last attempt was on... """
        self.username = self.user_input_box.get()
        
        exists = database.is_username(self.username)
        print(exists)
        
        print(self.username)

        if exists == True: 
            self.confirm_box(self.username) # if exists, then confirm
        else: 
            self.new_user_box() # if it doesn't exist welcome new user

    def new_user_box(self):
        box = Tk()
        box.title("Welcome!")
        
        self.window_placement(box, 300, 200)

        self.username = self.user_input_box.get()
        database.add_username(self.username)
        
        message = Label(
                        box,
                        text="Hey new user, {}! Here you can test your typing speed, just start typing in the box!".format(self.username),
                        wraplength=200)
        
        message.place(width=200, height=150, relx=0.5, rely=0.4, anchor='center')
        
        ok_button = Button(box, text="OK", command=lambda: self.ok(box))
        ok_button.place(width=100, height=30, relx=0.5, rely=0.7, anchor='center')
        self.username_box.destroy()


    def user_validate(self, inp):
        set_pat = ["$", "£", "_", "%"]

        if len(inp)>15:
            root.bell()
            return False

        if inp.isalnum():
            return True
                            
        elif any(char in set_pat for char in inp):

            return True
            
        elif inp == "":
            return True

        else:
            root.bell()
            print(inp)
            return False


    def confirm_box(self, username):
        confirm_dialog = Tk()  # placing the box
        
        self.username_box.destroy()
        self.window_placement(confirm_dialog, 300, 200)

        confirm_dialog.title("Confirmation") # titling the box
        message = Label(confirm_dialog, text="This username is already in use.\nIs this you coming back?")
        message.place(relx=0.5, rely=0.5, anchor='center')

        y_button = Button(confirm_dialog, text="Yes", command=lambda: self.confirm(username, confirm_dialog))
        n_button = Button(confirm_dialog, text="No", command=lambda: self.not_confirm(confirm_dialog))
        y_button.place(width=50, height=30, relx=0.3, rely=0.76, anchor='center')
        n_button.place(width=50, height=30, relx=0.7, rely=0.76, anchor='center')

    def confirm(self, username, dialog):
        dialog.destroy()
        confirm_box = Tk()
        confirm_box.title(username)

        self.window_placement(confirm_box, 300, 200)
    
        self.highest_score = database.get_highest_score(username)
        self.last_time = database.get_latest_time(username)
        
        text = "Welcome back, {}! Your last attempt was on {}, and your highest score is: {}"
        
        message = Label(
                    confirm_box,
                    text=text.format(username, self.last_time, self.highest_score),
                    wraplength=300
                    )

        message.place(relx=0.5, rely=0.4, anchor='center')

        ok_button = Button(confirm_box, text="OK", command=lambda: self.ok(confirm_box))
        ok_button.place(width=100, height=30, relx=0.5, rely=0.7, anchor='center')

    def not_confirm(self, dialog):
        dialog.destroy()
        self.master.lift()
        self.user_box()

    def ok(self, dialog):
        dialog.destroy()
        self.master.lift()

    def set_username(self):
        username = self.user_input_box.get()
        return username 

    def create_menu(self):
        def _optionsmenu_restart():
            """ Restarts the text, attempt time and clears input box and sets index to 0 """
            self.stopwatch_restart()

        def _optionsmenu_changeusername():
            """ Will allow user to switch username to either already existing user or
            a new one """

            self.user_box()

        def _helpmenu_helpindex():
            """ A new window that gives brief description about the program and how to use it"""
            self.helpindex = Toplevel(self.master)
            self.helpindex.title("Help Index")
            self.helpindex.geometry("300x500")

        def _helpmenu_about():
            """ A new window that gives a brief description about the program and its version, author and rights """
            self.helpindex = Toplevel(self.master)
            self.helpindex.title("About")
            self.helpindex.geometry("500x300")
            message = """VERSION 1.0.0\n© 2021 Ioana Koleva.  All rights reserved."""
            label = Label(self.helpindex, text=message, wraplength=300)
            label.place(relx=0.5, rely=0.5, anchor='center')

        self.optionsmenu.add_command(label="Restart", command=_optionsmenu_restart)
        self.optionsmenu.add_command(label="Change username", command=_optionsmenu_changeusername)
        self.optionsmenu.add_separator()
        self.optionsmenu.add_command(label="Exit", command=self.master.destroy)
        self.menubar.add_cascade(label="Options", menu=self.optionsmenu)

        self.helpmenu.add_command(label="Help Index", command=_helpmenu_helpindex)
        self.helpmenu.add_command(label="About...", command=_helpmenu_about)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.master.config(menu=self.menubar)


text = database.get_text("Article")
root = Tk()
app = App(root, text)


