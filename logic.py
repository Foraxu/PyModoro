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

class Pomodoro:
    def __init__(self):
        self.stages_amount = 3
        self.short_break_min = 5
        self.long_break_min = 20
        self.work_time_min = 25
        self.is_over = False

        self.setTimer(self.stages_amount, self.work_time_min, self.short_break_min, self.long_break_min)

    def setTimer(self, stages, work_time, short_break, long_break):
        self.stages_amount = stages
        self.short_break_min = short_break
        self.long_break_min = long_break
        self.work_time_min = work_time

        self.stages = {}

        for stage in range(1, stages+1):
            
            #If the current stage is the last one, then set the break minutes to the long_break_min amount.
            if stage == stages:
                self.stages[stage] = {"work_min": work_time,
                                      "break_min": long_break}
            else:
                self.stages[stage] = {"work_min": work_time,
                                      "break_min": short_break}
                
    def startupMessage(self):
        print(TOMATO)
        print("Hey, fella! That's the PyModoro. Your lovely Pomodoro Timer.")
        answer = input("Would you like to run this using default configuration? Type anything but 'n' to confirm.\n").lower()

        if answer == 'n':
            timers = ['work time', 'short break', 'long break']
            timers_answers = []

            print("Ok! Let's configure this out!")
            stages = int(input("How much stages would you like to add?   "))
            
            for i in timers:
                timers_answers.append(int(input(f"How much minutes would you like put in {i} stage?   ")))

            self.setTimer(stages, timers_answers[0], timers_answers[1], timers_answers[2])

    def start(self):

        self.startupMessage()

        def run():

            def countdown():
                if self.seconds != 0:
                    self.seconds -= 1
                elif self.minutes != 0:
                    self.minutes -= 1
                    self.seconds += 59
                else:
                    sleep(TIME_PASSING_SPEED)
                    self.is_over = True
                sleep(TIME_PASSING_SPEED)

            def print_clock():
                values = [str(i) for i in [self.minutes, self.seconds]]
                for i, e in enumerate(values):
                    if len(e) < 2:
                        values[i]=f"0{e}"
                print(f"{values[0]}:{values[1]}")

            system("clear")

            input(f"{TOMATO}\nType ENTER to start")

            for stage in range(1, self.stages_amount+1):
                self.seconds = 0
                self.minutes = int(self.stages[stage]['work_min'])

                if stage != 1:
                    play(song)
                    input("Press ENTER to continue")

                while not self.is_over:
                    system("clear")
                    print_clock()
                    countdown()

                self.minutes = int(self.stages[stage]['break_min'])
                self.is_over = False

                play(song)
                input("Press ENTER to continue")

                while not self.is_over:
                    system("clear")
                    print_clock()
                    countdown()

                self.is_over = False

            want_again = input("\nThe long break is over. Do you like to run PyModoro again? Type 'y' to confirm:    ").lower()

            if want_again == "y":
                run()
            else:
                print("Alright. Have a good one!")
        
        run()


Pomodoro().start()
