from time import sleep 
from pydub import AudioSegment
from pydub.playback import play
from os import system

song = AudioSegment.from_wav("notification.wav")

#Set the speed of the timer in seconds
TIME_PASSING_SPEED = 0.01

TOMATO = """
   ,--./,-.
  /         \
 |           |
  \         /
   `._,._,_'
"""

class PyModoro:
    """
    Handle the logic of a Pomodoro Timer.
    """
    def __init__(self):
        """Set up default configs for Pomodoro"""

        self.stages_amount = 3 #Number of stages. Each stage is composed by a work time and a short break, expect\
        self.short_break_min = 5                              #for the last one which is followed by a long break           
        self.long_break_min = 20
        self.work_time_min = 25
        self.is_over = False #When a step of a stage is completed

        self.setTimer(self.stages_amount, self.work_time_min, self.short_break_min, self.long_break_min)

    def setTimer(self, stages=int, work_time=int, short_break=int, long_break=int):
        """  Set configs: 
           - The amount of stages - Number of Working times followed by a break;
           - The duration of the short and the long breaks in minutes;
           - The working time duration in minutes;
        """
        self.stages_amount = stages
        self.short_break_min = short_break
        self.long_break_min = long_break
        self.work_time_min = work_time

        #A dictionary composed by numeric keys that start with 1 and go until the max number of stages
        #Each key is composed by another dict filled with two keys, "work_min" - set the duration of the current working time,
        #                                                               and "break_min" - set the durtion of the current break time
        self.stages = {}

        #Create and send the items for self.stages dict
        for stage in range(1, stages+1):
            
            #If the current stage is the last one, then set the break minutes to the long_break_min amount.
            if stage == stages:
                self.stages[stage] = {"work_min": work_time,
                                      "break_min": long_break}
            else:
                self.stages[stage] = {"work_min": work_time,
                                      "break_min": short_break}

    def return_clock(self):
        """
        Return a formated string that shows the current Pomodoro time in minutes and seconds
        """
        values = [str(i) for i in [self.minutes, self.seconds]]
        for i, e in enumerate(values):
            if len(e) < 2:
                values[i]=f"0{e}"
        return f"{values[0]}:{values[1]}"

    def passTime(self):
        """
        Subtract 1 from self.seconds and convert self.minutes to seconds when self.seconds is equal to zero
        and self.minutes is not zero.
        """
        if self.seconds != 0:
            self.seconds -= 1
        elif self.minutes != 0:
            self.minutes -= 1
            self.seconds += 59
        else:
            self.is_over = True
        sleep(TIME_PASSING_SPEED)


class PomodoroCommandLine(PyModoro):
    """
    Run PyModoro in the Command Line
    """
    def __init__(self):
        super().__init__()

    def startupMessage(self):
        """
        Send a simple 'Welcome' message and ask if the user wants to change the default config.
        """
        print(TOMATO)
        print("Hey, fella! That's the PyModoro. Your lovely Pomodoro Timer.")
        answer = input("Would you like to run this using default configuration? Type anything but 'n' to confirm.\n").lower()

        if answer == 'n':

            timers_answers = []
            print("Ok! Let's configure this out!")
            stages = int(input("How much stages would you like to add?   "))

            [timers_answers.append(int(input(f"How much minutes would you like to put in {i}?    ")))\
            for i in ['work time', 'short break', 'long break']] #It works exactly as the code bellow

            # for i in ['work time', 'short break', 'long break']:
            #     timers_answers.append(int(input(f"How much minutes would you like to put in {i}?  ")))
            
            self.setTimer(stages, timers_answers[0], timers_answers[1], timers_answers[2])

    def start(self):
        
        self.startupMessage()

        system("clear") #Clear the command line

        input(f"{TOMATO}\nType ENTER to start")

        for stage in range(1, self.stages_amount+1):
            """
            "Run two while loops for each stage: one to execute the working step and the other to manage the break step."
            """

            self.seconds = 0
            self.minutes = int(self.stages[stage]['work_min'])                

            while not self.is_over:
                system("clear")
                print(self.return_clock())
                self.passTime()
                sleep(TIME_PASSING_SPEED)

            self.minutes = int(self.stages[stage]['break_min'])
            self.is_over = False

            play(song)
            input("Press ENTER to continue")

            while not self.is_over:
                system("clear")
                print(self.return_clock())
                self.passTime()
                sleep(TIME_PASSING_SPEED)

            self.is_over = False

            play(song)
            input("Press ENTER to continue")

        want_again = input("\nThe long break is over. Do you like to run PyModoro again? Type 'y' to confirm:    ").lower()

        if want_again == "y":
            self.start()
        else:
            print("Alright. Have a good one!")


if __name__ == "__main__":
    PomodoroCommandLine().start()
