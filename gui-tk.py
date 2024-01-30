from tkinter import Tk, Canvas, PhotoImage, Button, Label

POMODORO_IMG = 'tomato.png'
CANVAS_WIDTH = 200
CANVAS_HEIGHT = 300
FONT_NAME = "Courier"
BACKGROUND_COLOR = '#f7f5dd' # a type of yellow

class PomodoroGUI:
    def __init__(self):

        # create main screen from Tk class
        self.root = Tk()
        self.root.title('PyModoro')
        self.root.config(padx=50, pady=10, bg=BACKGROUND_COLOR)

        # create and set canvas
        self.canvas = Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.grid(column=1, row=1)

        # add title
        self.title = Label(text="PyModoro", foreground="green", font=(FONT_NAME, 45, 'bold'), bg=BACKGROUND_COLOR).grid(column=1, row=0)

        # add the tomato image by creating an object from PhotoImage
        self.tomato = PhotoImage(file=POMODORO_IMG)
        self.canvas.create_image(100, 150, image=self.tomato) # put the image on canvas at the given coords

        # add 'clock'
        clock_text = self.canvas.create_text(100, 180, text="00:00", fill='white', font=(FONT_NAME, 35, 'bold'))


        # create and put the buttons on their positions
        self.start_button = Button(text='start')
        self.reset_button = Button(text='reset')

        self.start_button.grid(column=0, row=2)
        self.reset_button.grid(column=2, row=2)

        #TODO implement the logic of it and put it where you find ok
        self.pause_button = Button(text='pause')
