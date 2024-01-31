from math import floor as roundfloor

class Timer:
    def __init__(self):
        self.working_seconds = 25*60
        self.shortbreak_seconds = 5*60
        self.longbreak_seconds = 15*60

        self.reps = 3

        self.step = 'working'

        self.step_seconds = self.working_seconds

        self.current_rep = 0.5


    def passSecond(self):
        """
        Subtract one second from the time that setStepSeconds method has set.
        """
        self.step_seconds -= 1

    def setStepSeconds(self):
        """
        Set the time for each step based on the current rep.
        There are only 2 possible steps: The 'working' step and the 'break' step.

        All the working steps are followed by a short break, except for the last one which is followed by a long break.\n
        The last working step is defined when its break step is set in the same moment that the current rep is equal to the max
        number of reps - defined in self.reps.
        """
        if self.step == 'working':
            self.step_seconds = self.working_seconds
        elif self.step == 'break' and self.current_rep == self.reps:
            self.step_seconds = self.longbreak_seconds
        elif self.step == 'break':
            self.step_seconds = self.shortbreak_seconds
        
    def nextStep(self):
        if self.step == "working":
            self.step = "break"
        elif self.step == 'break':
            self.step = "working"
    
    def formatTime(self):
        """
        Return a formatted string with the current time written as the following template:\n
        MINUTES:SECONDS
        """
        minutes = roundfloor(self.step_seconds/60)
        seconds = self.step_seconds%60

        if minutes < 10:
            minutes = f'0{minutes}'
        if seconds < 10:
            seconds = f'0{seconds}'
        
        return f"{minutes}:{seconds}"
    