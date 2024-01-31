#! ./.venv/bin/python3

from tkinter import Tk, Canvas, PhotoImage, Button, Label
from pydub import AudioSegment
from pydub.playback import play
from brain.timer import Timer

POMODORO_IMG = './resources/img/tomato.png'
NOTIFICATION_SOUND = './resources/sounds/notification.wav'
CANVAS_WIDTH = 200
CANVAS_HEIGHT = 300
FONT_NAME = "Courier"
BACKGROUND_COLOR = '#f7f5dd' # a type of yellow
CLOCK_SPEED = 1000

notification = AudioSegment.from_wav(file=NOTIFICATION_SOUND)

############################################### GUI ########################################################

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

pause_button = Button(text='pause')
pause_button.grid(column=1, row=2)


#################################### POMODORO'S LOGIC #######################################

class Pomodoro(Timer):
    """
    Implement the GUI with Timer
    """
    def __init__(self):
        super().__init__()

        self.is_running = False #If the clock is working, recieve True
        self.was_reseted = False #If the reset button is pressed, recieve True
        self.is_paused = False #If the pause button is pressed, recieve True
        self.changeAndSetStep()
        self.updateClock()

    def start(self):
        """
        
        """
        if self.is_running:
            return
        elif self.was_reseted == True:                    # If the reset button is pressed when the clock is stopped, the condition inside the clocking() will not/
                                                          #be triggered. Therefore, it is handled here.
            self.was_reseted = False
            
        if self.ongoing_step == 'working' and not self.is_paused:
            self.ongoing_rep += 1

        elif self.is_paused:
            self.is_paused = False

        self.is_running = True

        self.clocking()

    def clocking(self):
        """
        Event handled by the canvas.after method, being called repeatedly after a set amount of time.
         
        Manage the clock functionality.\n
        """
        def notifyReset():
            """
            Change the text in the clock to "Reseting..."
            """
            canvas.itemconfig(clock_text, text="Reseting...", font=(FONT_NAME, 20, 'bold'))

        if self.was_reseted:
            self.is_running = False
            self.was_reseted = False
            return
        
        elif self.is_paused:
            self.is_running = False
            return
        
        elif self.ongoing_rep == self.max_reps and self.step_seconds < 0 and self.ongoing_step == 'break':
            self.is_running = False
            play(notification)
            canvas.itemconfig(clock_text, text="Finished!", font=(FONT_NAME, 20, 'bold'))
            canvas.after(1000, notifyReset)
            canvas.after(3000, self.reset)

        elif self.step_seconds < 0:
            self.is_running = False # Stop running
            play(notification)          # ------ Play the notification sound with pydub module
            self.changeAndSetStep()
            self.updateClock()
        else:
            time = self.formatTime()
            canvas.itemconfig(clock_text, text=time)
            self.passSecond()
            canvas.after(CLOCK_SPEED, self.clocking)
        

    def pause(self):
        """
        - Only works if the Pomodoro is already working.\n
        Pauses the clock exactly on the point it was when the button pause is pressed.\n
        Does not affect the on going step.
        """
        if self.ongoing_rep != 0:      #The pause function only applies when the program is already running. 
            self.is_paused = True          #Therefore, if it's not running yet, "is_paused" will not receive True.


    def reset(self):
        """
        Reset all the Pomodoro's attributes to their default values.
        """
        self.was_reseted = True
        self.is_paused = False
        self.ongoing_step = None
        self.ongoing_rep = 0

        self.changeAndSetStep()
        canvas.itemconfig(clock_text, font=(FONT_NAME, 35, 'bold'))    # Reset clock style.
        self.updateClock()

        
    def updateClock(self):
        """
        Update the clock with the present time.
        """
        time=self.formatTime()
        canvas.itemconfig(clock_text, text=time)

        
pomodoro = Pomodoro()

################################ ======= Buttons Logic ======== ########################################

# When the named button is pressed, call the funcion that follows the command parameter.
start_button.config(command=pomodoro.start)
reset_button.config(command=pomodoro.reset)
pause_button.config(command=pomodoro.pause)

root.mainloop()
