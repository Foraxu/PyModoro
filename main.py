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
CLOCK_SPEED = 20

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


#################################### Manage the functionality #######################################

class Pomodoro(Timer):
    """
    Implement the GUI with Timer
    """
    def __init__(self):
        super().__init__()

        self.is_running = False #If the clock is working, recieve True
        self.reset_pressed = False #If the reset button is pressed, recieve True

        self.updateClock()

    def start(self):
        """
        Start the clock
        """
        # If reset button is pressed
        if self.reset_pressed:
            self.remove_reset()
            
        if self.is_running:
            return
        
        if self.current_rep != 0:
            self.nextStep()
            self.setStepSeconds()

        # Add a half rep for each time start method is called
        self.current_rep += 0.5

        self.is_running = True

        def clocking():
            """
            Event handled by the canvas.after method. Modify the text written in the canvas clock_text item.\n
            "clocking" is called repeatedly expect:
            - if the current rep is greater than the max reps;
            - if the amount of seconds of the current step is less than 0;
            - if the reset button is pressed;
            """

            if self.current_rep > self.reps or self.step_seconds < 0:

                self.is_running = False # Stop running

                play(notification)          # ------ Play the notification sound with pydub module
                
                self.showNextStep()
                
            elif self.reset_pressed:
                self.is_running = False
                return
            else:
                time = self.formatTime()
                canvas.itemconfig(clock_text, text=time)
                self.passSecond()

                canvas.after(CLOCK_SPEED, clocking)

        clocking()

    def reset(self):
        self.reset_pressed = True
        self.step = "working"
        self.current_rep = 0
        self.setStepSeconds()
        self.updateClock()

    def remove_reset(self):
        self.reset_pressed = False
        
    def updateClock(self):
        time=self.formatTime()
        canvas.itemconfig(clock_text, text=time)

    def showNextStep(self):
        #There's a little trick here: nextStep is called for printing the next step time on the screen and then, called one more time
        # to put it in the same step it was before - since there are only two steps that nextStep goes through(the working and the break).
        self.nextStep()
        self.setStepSeconds()
        self.updateClock()
        self.nextStep()

        
pomodoro = Pomodoro()

################################ ======= Buttons Logic ======== ########################################

# When the named button is pressed, call the funcion that follows the command parameter.
start_button.config(command=pomodoro.start)
reset_button.config(command=pomodoro.reset)


root.mainloop()
