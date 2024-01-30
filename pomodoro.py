from math import floor as roundfloor

class Timer:
    def __init__(self):
        self.working_seconds = 25*60
        self.shortbreak_seconds = 5*60
        self.longbreak_seconds = 15*60

        self.reps = 3

        self.step = 1

        self.step_seconds = 0

        self.current_rep = 0


    def passSecond(self):
        self.step_seconds -= 1

    def setStepTime(self):
        if self.step == 1:
            self.step_seconds = self.working_seconds
        elif self.step == 2 and self.current_rep == self.reps:
            self.step_seconds = self.longbreak_seconds
        elif self.step == 2:
            self.step_seconds = self.shortbreak_seconds
        
        if self.step > 1:
            self.step -= 1
        else:
            self.step += 1
    
    def formatTime(self):
        minutes = roundfloor(self.step_seconds/60)
        seconds = self.step_seconds%60

        if minutes < 10:
            minutes = f'0{minutes}'
        if seconds < 10:
            seconds = f'0{seconds}'
        
        return f"{minutes}:{seconds}"
    