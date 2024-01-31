from math import floor as roundfloor

class Timer:
    def __init__(self):
        self.workingstep_seconds = 25*60
        self.shortbreakstep_seconds = 5*60
        self.longbreakstep_seconds = 15*60

        self.max_reps = 3

        self.ongoing_step = None 

        self.step_seconds = None

        self.ongoing_rep = 0


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
        The last working step is defined when the going rep is equal to the max number of reps.
        """
        if self.ongoing_step == 'working':
            self.step_seconds = self.workingstep_seconds
        elif self.ongoing_step == 'break' and self.ongoing_rep == self.max_reps:
            self.step_seconds = self.longbreakstep_seconds
        elif self.ongoing_step == 'break':
            self.step_seconds = self.shortbreakstep_seconds
        

    def changeStep(self):
        if self.ongoing_step == "working":
            self.ongoing_step = "break"
        elif self.ongoing_step == 'break':
            self.ongoing_step = "working"
            
    
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
    
    def setFirstStep(self, step:str):
        """
        'step' parameter must be whether 'working' or 'break' only.\n
        By default, the first step is defined as 'working'. To modify it, call this function before calling changeAndSetStep.
        """
        self.ongoing_step = step
        return
    
    def changeAndSetStep(self):
        """
        Change and set the seconds of a step, calling both the changeStep and setStepSeconds methods.
        If ongoing_step is defined as None, define it as 'working'.
        """
        if self.ongoing_step == None:
            self.setFirstStep('working')
        else:
            self.changeStep()
        self.setStepSeconds()
