#! ./.venv/bin/python3

###TODO complete adding the comments

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
CLOCK_SPEED = 10

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
        self.is_paused = False
        self.changeAndSetStep()
        self.updateClock()

    def start(self):
        """
        Start the clock
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
        print(f'{self.ongoing_rep}, {self.ongoing_step}')

        def clocking():
            """
            Event handled by the canvas.after method. Modify the text written in the canvas clock_text item.\n
            "clocking" is called repeatedly expect:
            - if the current rep is greater than the max reps;
            - if the amount of seconds of the current step is less than 0;
            - if the reset button is pressed;
            """

            def resetingWarn():
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

                canvas.after(1000, resetingWarn)
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

                canvas.after(CLOCK_SPEED, clocking)

        clocking()
        

    def pause(self):
        self.is_paused = True

    def reset(self):
        self.was_reseted = True
        self.is_paused = False
        self.ongoing_step = None
        self.ongoing_rep = 0

        self.changeAndSetStep()
        canvas.itemconfig(clock_text, font=(FONT_NAME, 35, 'bold'))
        self.updateClock()

    def remove_reset(self):
        self.was_reseted = False
        
    def updateClock(self):
        time=self.formatTime()
        canvas.itemconfig(clock_text, text=time)

        
pomodoro = Pomodoro()

################################ ======= Buttons Logic ======== ########################################

# When the named button is pressed, call the funcion that follows the command parameter.
start_button.config(command=pomodoro.start)
reset_button.config(command=pomodoro.reset)
pause_button.config(command=pomodoro.pause)

root.mainloop()
