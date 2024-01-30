#! ./.venv/bin/python3

from tkinter import Tk, Canvas, PhotoImage, Button, Label
from pydub import AudioSegment
from pydub.playback import play
from pomodoro import Timer

POMODORO_IMG = 'tomato.png'
NOTIFICATION_SOUND = 'notification.wav'
CANVAS_WIDTH = 200
CANVAS_HEIGHT = 300
FONT_NAME = "Courier"
BACKGROUND_COLOR = '#f7f5dd' # a type of yellow
CLOCK_SPEED = 1000

notification = AudioSegment.from_wav(file=NOTIFICATION_SOUND)

######## GUI

# create main screen from Tk class
root = Tk()
root.title('PyModoro')
root.config(padx=50, pady=10, bg=BACKGROUND_COLOR)

# create and set canvas
canvas = Canvas(width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=1, row=1)

# add title
title = Label(text="PyModoro", foreground="green", font=(FONT_NAME, 45, 'bold'), bg=BACKGROUND_COLOR).grid(column=1, row=0)

# add the tomato image by creating an object from PhotoImage
tomato = PhotoImage(file=POMODORO_IMG)
canvas.create_image(100, 150, image=tomato) # put the image on canvas at the given coords

# add 'clock'
clock_text = canvas.create_text(100, 180, text="00:00", fill='white', font=(FONT_NAME, 35, 'bold'))


# create and put the buttons on their positions
start_button = Button(text='start')
reset_button = Button(text='reset')

start_button.grid(column=0, row=2)
reset_button.grid(column=2, row=2)

#TODO implement the logic of it and put it where you find ok
pause_button = Button(text='pause')


####### Logic

class Pomodoro(Timer):
    def __init__(self):
        super().__init__()
        self.is_running = False
        self.reset_pressed = False
        self.initialPrint()

    def start(self):
        if self.reset_pressed:
            self.remove_reset()
        if self.is_running:
            return
        self.current_rep += 0.5
        self.setStepTime()
        self.is_running = True

        def clocking():
            if self.current_rep > self.reps or self.step_seconds < 0:
                self.is_running = False
                play(notification)
                self.setStepTime()
                text = self.formatTime()
                canvas.itemconfig(clock_text, text=text)
                self.setStepTime()
                
            elif self.reset_pressed:
                self.is_running = False                
            else:
                time = self.formatTime()
                canvas.itemconfig(clock_text, text=time)
                self.passSecond()

                canvas.after(CLOCK_SPEED, clocking)

        clocking()

    def reset(self):
        self.reset_pressed = True
        self.step = 1
        self.current_rep = 0
        self.initialPrint()

    def remove_reset(self):
        self.reset_pressed = False
        
    def initialPrint(self):
        self.setStepTime()
        text = self.formatTime()
        canvas.itemconfig(clock_text, text=text)
        self.setStepTime()


pomodoro = Pomodoro()
            
start_button.config(command=pomodoro.start)
reset_button.config(command=pomodoro.reset)

root.mainloop()
